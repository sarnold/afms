# -*- coding: latin-1  -*-

# -------------------------------------------------------------------
# Copyright 2008 Achim Köhler
#
# This file is part of AFMS.
#
# AFMS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation, either version 2 of the License, 
# or (at your option) any later version.
#
# AFMS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AFMS.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------

import logging, time
import wx
import afmodel
import afresource, afconfig
from _afimportartefactdlg import ImportArtefactDialog

class afImporter():
    def __init__(self, parentwin, basemodel, importpath):
        self.parentwin = parentwin
        self.basemodel = basemodel
        self.importpath = importpath
        
        
    def Run(self):
        self.model = afmodel.afModel(self)
        self.model.requestOpenProduct(self.importpath)
        self.dlg = ImportArtefactDialog(self.parentwin, -1)
        self.dlg.Bind(wx.EVT_CHECKLISTBOX, self.OnListItemChecked)
        self.dlg.InitContent(self.model.getFeatureList(), self.model.getRequirementList(),
            self.model.getUsecaseList(), self.model.getTestcaseList(), self.model.getTestsuiteList())
        if self.dlg.ShowModal() == wx.ID_OK:
            self.ImportArtefacts()
        self.dlg.Destroy()
        

    def OnListItemChecked(self, evt):
        """Event handler called when list item is checked/unchecked
           Client data returns tuple with list object, list index and check state
        """
        if not self.dlg.GetAutoSelectRelated():
            # nothing to do if related artefacts should not be checked automatically
            return
        (listobj, itemindex, state) = evt.GetClientData()
        if state == False:
            # nothing to do if artefact becomes unchecked
            return
        
        (listkind, ID) = listobj.GetSelectionID()
        if listkind == 'FEATURES':
            related_requirements = self.model.getFeature(ID)[1][0]
            related_requirements_ids = [item[0] for item in related_requirements]
            logging.debug("_afimporter.OnListItemChecked(): auto checking requirements %s" % str(related_requirements_ids))
            self.dlg.CheckArtefacts('REQUIREMENTS', related_requirements_ids)
            
        elif listkind == 'REQUIREMENTS':
            (testcases, usecases) = self.model.getRequirement(ID)[1:3]
            related_testcases_ids = [item[0] for item in testcases[0]]
            related_usecases_ids = [item[0] for item in usecases[0]]
            logging.debug("_afimporter.OnListItemChecked(): auto checking testcases %s" % str(related_testcases_ids))
            logging.debug("_afimporter.OnListItemChecked(): auto checking usecases  %s" % str(related_usecases_ids))
            self.dlg.CheckArtefacts('TESTCASES', related_testcases_ids)
            self.dlg.CheckArtefacts('USECASES', related_usecases_ids)
            
        elif listkind == 'TESTSUITES':
            related_testcases = self.model.getTestsuite(ID)[1]
            related_testcases_ids = [item[0] for item in related_testcases]
            logging.debug("_afimporter.OnListItemChecked(): auto checking testcases %s" % str(related_testcases_ids))
            self.dlg.CheckArtefacts('TESTCASES', related_testcases_ids)


    def ImportArtefacts(self):
        (ftlist, rqlist, uclist, tclist, tslist) = self.dlg.GetCheckedArtefacts()
        (new_ftlist, new_rqlist, new_uclist, new_tclist, new_tslist) = ([], [], [], [], [])
        changelog = (time.strftime(afresource.TIME_FORMAT), afconfig.CURRENT_USER, '')
        for ft_id in ftlist:
            basedata = list(self.model.getFeature(ft_id)[0])
            # indicate new requirement
            basedata[0] = -1  
            r = self.basemodel.saveFeature((basedata, ([], []), changelog))
            # save new ID of the imported feature
            new_ftlist.append(r[0][0][0]) 
            
        for rq_id in rqlist:
            basedata = list(self.model.getRequirement(rq_id)[0])
            # indicate new requirement
            basedata[0] = -1
            r = self.basemodel.saveRequirement((basedata, ([], []), ([], []), changelog))
            # save new ID of the imported requirement
            new_rqlist.append(r[0][0][0])

        for uc_id in uclist:
            basedata = list(self.model.getUsecase(uc_id)[0])
            # indicate new use case
            basedata[0] = -1
            r = self.basemodel.saveUsecase((basedata, changelog))
            # save new ID of the imported use case
            new_uclist.append(r[0][0][0])

        for tc_id in tclist:
            basedata = list(self.model.getTestcase(tc_id)[0])
            # indicate new test case
            basedata[0] = -1
            r = self.basemodel.saveTestcase((basedata, changelog))
            # save new ID of the imported test case
            new_tclist.append(r[0][0][0])
            
        for ts_id in tslist:
            basedata = list(self.model.getTestsuite(ts_id)[0])
            # indicate new testsuite
            basedata[0] = -1
            r = self.basemodel.saveTestsuite((basedata, [], []))
            # save new ID of the imported testsuite
            new_tslist.append(r[0][0][0])
            
        # now we have import all checked artefacts. Next step is
        # to import the corresponding artefact relations

        for ft_id, new_ft_id in zip(ftlist, new_ftlist):
            related_requirement_ids = self.model.getRequirementIDsReleatedToFeature(ft_id)
            for rq_id, new_rq_id in zip(rqlist, new_rqlist):
                if rq_id in related_requirement_ids:
                    self.basemodel.addFeatureRequirementRelation(new_ft_id, new_rq_id)

        for rq_id, new_rq_id in zip(rqlist, new_rqlist):
            related_testcase_ids = self.model.getTestcaseIDsRelatedToRequirement(rq_id)
            for tc_id, new_tc_id in zip(tclist, new_tclist):
                if tc_id in related_testcase_ids:
                    self.basemodel.addRequirementTestcaseRelation(new_rq_id, new_tc_id)
            related_usecase_ids = self.model.getUsecaseIDsRelatedToRequirement(rq_id)
            for uc_id, new_uc_id in zip(uclist, new_uclist):
                if uc_id in related_usecase_ids:
                    self.basemodel.addRequirementUsecaseRelation(new_rq_id, new_uc_id)

        for ts_id, new_ts_id in zip(tslist, new_tslist):
            related_testcase_ids = self.model.getTestcaseIDsRelatedToTestsuite(ts_id)
            for tc_id, new_tc_id in zip(tclist, new_tclist):
                if tc_id in related_testcase_ids:
                    self.basemodel.addTestsuiteTestcaseRelation(new_ts_id, new_tc_id)


