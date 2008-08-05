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

# $Id$

import logging, time
import wx
import afmodel
import afresource, afconfig
from _afimportartefactdlg import ImportArtefactDialog
from _afartefact import *


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
            self.model.getUsecaseList(), self.model.getTestcaseList(),
            self.model.getTestsuiteList(), self.model.getSimpleSectionList(),
            self.model.getGlossaryEntryList())
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
            feature = self.model.getFeature(ID)
            related_requirements_ids = [item['ID'] for item in feature.getRelatedRequirements()]
            logging.debug("_afimporter.OnListItemChecked(): auto checking requirements %s" % str(related_requirements_ids))
            self.dlg.CheckArtefacts('REQUIREMENTS', related_requirements_ids)

        elif listkind == 'REQUIREMENTS':
            requirement = self.model.getRequirement(ID)
            related_testcases_ids = [item['ID'] for item in requirement.getRelatedTestcases()]
            related_usecases_ids = [item['ID'] for item in requirement.getRelatedUsecases()]
            related_requirements_ids = [item['ID'] for item in requirement.getRelatedRequirements()]
            logging.debug("_afimporter.OnListItemChecked(): auto checking testcases %s" % str(related_testcases_ids))
            logging.debug("_afimporter.OnListItemChecked(): auto checking usecases  %s" % str(related_usecases_ids))
            logging.debug("_afimporter.OnListItemChecked(): auto checking requirements  %s" % str(related_requirements_ids))
            self.dlg.CheckArtefacts('TESTCASES', related_testcases_ids)
            self.dlg.CheckArtefacts('USECASES', related_usecases_ids)
            self.dlg.CheckArtefacts('REQUIREMENTS', related_requirements_ids)

        elif listkind == 'TESTSUITES':
            testsuite = self.model.getTestsuite(ID)
            related_testcases_ids = [item['ID'] for item in testsuite.getRelatedTestcases()]
            logging.debug("_afimporter.OnListItemChecked(): auto checking testcases %s" % str(related_testcases_ids))
            self.dlg.CheckArtefacts('TESTCASES', related_testcases_ids)


    def _Import(self, aflist, new_aflist, savefn, getfn, changelog):
        for af_id in aflist:
            artefact = getfn(af_id)
            artefact['ID'] = -1
            artefact.clearRelations()
            artefact.setChangelog(changelog)
            newartefact = savefn(artefact)[0]
            new_aflist.append(newartefact['ID'])


    def ImportArtefacts(self):
        (ftlist, rqlist, uclist, tclist, tslist, sslist, gelist) = self.dlg.GetCheckedArtefacts()
        (new_ftlist, new_rqlist, new_uclist, new_tclist, new_tslist, new_sslist, new_gelist) = ([], [], [], [], [], [], [])
        changelog = cChangelogEntry(user=afconfig.CURRENT_USER,
            date=time.strftime(afresource.TIME_FORMAT), description='')

        self._Import(ftlist, new_ftlist, self.basemodel.saveFeature, self.model.getFeature, changelog)
        self._Import(rqlist, new_rqlist, self.basemodel.saveRequirement, self.model.getRequirement, changelog)
        self._Import(tclist, new_tclist, self.basemodel.saveTestcase, self.model.getTestcase, changelog)
        self._Import(uclist, new_uclist, self.basemodel.saveUsecase, self.model.getUsecase, changelog)
        self._Import(tslist, new_tslist, self.basemodel.saveTestsuite, self.model.getTestsuite, changelog)
        self._Import(sslist, new_sslist, self.basemodel.saveSimpleSection, self.model.getSimpleSection, changelog)
        self._Import(gelist, new_gelist, self.basemodel.saveGlossaryEntry, self.model.getGlossaryEntry, changelog)

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
            related_requirement_ids = self.model.getRequirementIDsRelatedToRequirement(rq_id)
            for req_id, new_req_id in zip(rqlist, new_rqlist):
                if req_id in related_requirement_ids:
                    self.basemodel.addRequirementRequirementRelation(new_rq_id, new_req_id)

        for ts_id, new_ts_id in zip(tslist, new_tslist):
            related_testcase_ids = self.model.getTestcaseIDsRelatedToTestsuite(ts_id)
            for tc_id, new_tc_id in zip(tclist, new_tclist):
                if tc_id in related_testcase_ids:
                    self.basemodel.addTestsuiteTestcaseRelation(new_ts_id, new_tc_id)


