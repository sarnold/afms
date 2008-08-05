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

import wx
from _afhtmlwindow import *
from _aftextctrl import *
from _afartefactlist import *
from _afvalidators import NotEmptyValidator, ArtefactHookValidator
import _afbasenotebook
import afconfig
import afresource
from _afartefact import cRequirement, cTestcase, cUsecase

class afRequirementNotebook(_afbasenotebook.afBaseNotebook):
    def __init__(self, parent, id = -1, viewonly = True):
        _afbasenotebook.afBaseNotebook.__init__(self, parent, id, viewonly)
        color = parent.GetBackgroundColour()
        self.SetOwnBackgroundColour(color)
        panel1 = wx.Panel(self, -1)
        panel1.SetOwnBackgroundColour(color)
        panel2 = wx.Panel(self, -1)
        panel2.SetOwnBackgroundColour(color)

        labels1 = [_('Title'), _('ID'), _('Version'), _('Priority'), _('Status'), _('Complexity'), _('Assigned'), _('Effort'), _('Category'), _('Description')]
        labels2 = [_('Origin'), _('Rationale')]


        (width, height) = (0, 0)
        statictext = []
        for label in labels1:
            st = wx.StaticText(panel1, -1, label+':')
            (w, h) = st.GetSize()
            (width, height) =  (max(width, w), max(height, h))
            statictext.append(st)

        for st in statictext:
            st.SetMinSize((width,height))

        if viewonly:
            self.title_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.id_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.version_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.priority_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.status_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.complexity_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.assigned_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.effort_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.category_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.description_edit = afHtmlWindow(panel1, -1)
            self.origin_edit = afHtmlWindow(panel2, -1)
            (w, h) = self.origin_edit.GetSize()
            self.origin_edit.SetMinSize((w, 3*h))
            self.rationale_edit = afHtmlWindow(panel2, -1)
        else:
            self.title_edit = wx.TextCtrl(panel1, -1, "", validator = NotEmptyValidator())
            self.id_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.version_edit = wx.TextCtrl(panel1, -1, "")
            self.priority_edit = wx.ComboBox(panel1, -1, choices = [_(i) for i in afresource.PRIORITY_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.status_edit = wx.ComboBox(panel1, -1, choices = [_(i) for i in afresource.STATUS_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.complexity_edit = wx.ComboBox(panel1, -1, choices = [_(i) for i in afresource.COMPLEXITY_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.assigned_edit = wx.ComboBox(panel1, -1, choices = afconfig.ASSIGNED_NAME, style=wx.CB_DROPDOWN)
            self.effort_edit = wx.ComboBox(panel1, -1, choices = [_(i) for i in afresource.EFFORT_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.category_edit = wx.ComboBox(panel1, -1, choices = [_(i) for i in afresource.CATEGORY_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.description_edit = afTextCtrl(panel1)
            self.origin_edit = afTextCtrl(panel2)
            self.rationale_edit = afTextCtrl(panel2)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.description_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.origin_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.rationale_edit)

        self.id_edit.Enable(False)
        edit = [self.title_edit, self.id_edit, self.version_edit, self.priority_edit, self.status_edit, \
                self.complexity_edit, self.assigned_edit, self.effort_edit, self.category_edit, self.description_edit, self.origin_edit, self.rationale_edit]

        mainsizer = wx.FlexGridSizer(3, 1, 10, 10)

        sizer = wx.FlexGridSizer(1, 2, 10, 10)
        sizer.Add(statictext[0], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(edit[0], 0, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)

        mainsizer.Add(sizer, 0, wx.EXPAND)

        sizer = wx.FlexGridSizer(4, 4, 10, 10)
        for i in range(1,9):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
            sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
        sizer.SetFlexibleDirection(wx.BOTH)

        mainsizer.Add(sizer, 0, wx.EXPAND)

        sizer = wx.FlexGridSizer(1, 2, 10, 10)
        sizer.Add(statictext[9], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(edit[9], 0, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(0)
        sizer.SetFlexibleDirection(wx.BOTH)
        sizer.Layout()

        mainsizer.Add(sizer, 1, wx.EXPAND)

        mainsizer.AddGrowableCol(0)
        mainsizer.AddGrowableRow(2)
        mainsizer.Layout()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(mainsizer, 1, wx.ALL | wx.EXPAND, 10)
        panel1.SetSizer(hbox)

        panel1.Layout()
        self.AddPage(panel1, _("Requirement"))

        #-----------------------------------------------------------------
        # Rationale panel

        statictext = []
        for label in labels2:
            st = wx.StaticText(panel2, -1, label+':')
            statictext.append(st)

        mainsizer = wx.FlexGridSizer(2, 2, 10, 10)
        mainsizer.Add(statictext[0], 0, wx.EXPAND)
        mainsizer.Add(self.origin_edit, 0, wx.EXPAND)
        mainsizer.Add(statictext[1], 0, wx.EXPAND)
        mainsizer.Add(self.rationale_edit, 1, wx.EXPAND)
        mainsizer.AddGrowableCol(1)
        mainsizer.AddGrowableRow(1)
        mainsizer.Layout()
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(mainsizer, 1, wx.ALL | wx.EXPAND, 10)
        panel2.SetSizer(hbox)
        self.AddPage(panel2, _("Rationale"))

        #-----------------------------------------------------------------
        # Related testcases panel

        panel3 = wx.Panel(self, -1)
        self.testcaselist = afTestcaseList(panel3, -1, checkstyle=not self.viewonly)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.testcaselist, 1, wx.ALL| wx.EXPAND, 6)
        panel3.SetSizer(sizer)
        self.AddPage(panel3, _("Attached Testcases"))
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)

        #-----------------------------------------------------------------
        # Related usecases panel

        panel4 = wx.Panel(self, -1)
        self.usecaselist = afUsecaseList(panel4, -1, checkstyle=not self.viewonly)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.usecaselist, 1, wx.ALL| wx.EXPAND, 6)
        panel4.SetSizer(sizer)
        self.AddPage(panel4, _("Attached Usecases"))
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)

        #-----------------------------------------------------------------
        # Related features panel; this relation could not be edited from here

        self.featurelist = self.AddRelatedArtefactPanel(afFeatureList, _("Related Features"))

        #-----------------------------------------------------------------
        # Related requirements panel

        panel5 = wx.Panel(self, -1)
        self.requirementlist = afRequirementList(panel5, -1, checkstyle=not self.viewonly)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.requirementlist, 1, wx.ALL| wx.EXPAND, 6)
        panel5.SetSizer(sizer)
        self.AddPage(panel5, _("Related Requirements"))
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)

        #-----------------------------------------------------------------

        self.AddChangelogPanel()


    def InitContent(self, requirement):
        self.id_edit.SetValue(str(requirement['ID']))
        self.title_edit.SetValue(requirement['title'])
        self.version_edit.SetValue(requirement['version'])
        self.assigned_edit.SetValue(requirement['assigned'])
        self.origin_edit.SetValue(requirement['origin'])
        self.rationale_edit.SetValue(requirement['rationale'])
        self.description_edit.SetValue(requirement['description'])
        self.priority_edit.SetValue(_(afresource.PRIORITY_NAME[requirement['priority']]))
        self.status_edit.SetValue(_(afresource.STATUS_NAME[requirement['status']]))
        self.complexity_edit.SetValue(_(afresource.COMPLEXITY_NAME[requirement['complexity']]))
        self.effort_edit.SetValue(_(afresource.EFFORT_NAME[requirement['effort']]))
        self.category_edit.SetValue(_(afresource.CATEGORY_NAME[requirement['category']]))
        if not self.viewonly:
            self.priority_edit.SetSelection(requirement['priority'])
            self.status_edit.SetSelection(requirement['status'])
            self.complexity_edit.SetSelection(requirement['complexity'])
            self.effort_edit.SetSelection(requirement['effort'])
            self.category_edit.SetSelection(requirement['category'])

        self.testcaselist.InitCheckableContent(requirement.getUnrelatedTestcases(), requirement.getRelatedTestcases(), self.viewonly)
        self.usecaselist.InitCheckableContent(requirement.getUnrelatedUsecases(), requirement.getRelatedUsecases(), self.viewonly)
        self.requirementlist.InitCheckableContent(requirement.getUnrelatedRequirements(), requirement.getRelatedRequirements(), self.viewonly)
        self.featurelist.InitContent(requirement.getRelatedFeatures())

        if self.viewonly:
            self.changelist.InitContent(requirement.getChangelist())
        else:
            self.validator_hook = requirement.validator
            self.initial_requirement = requirement
            self.changelogpanel.changelog_edit.SetValidator(ArtefactHookValidator(self.ValidateRequirement))

        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()


    def GetContent(self):
        requirement = cRequirement(ID=int(self.id_edit.GetValue()),
                                   title=self.title_edit.GetValue(),
                                   priority=self.priority_edit.GetCurrentSelection(),
                                   status=self.status_edit.GetCurrentSelection(),
                                   version=self.version_edit.GetValue(),
                                   complexity=self.complexity_edit.GetCurrentSelection(),
                                   assigned=self.assigned_edit.GetValue(),
                                   effort=self.effort_edit.GetCurrentSelection(),
                                   category=self.category_edit.GetCurrentSelection(),
                                   origin=self.origin_edit.GetValue(),
                                   rationale=self.rationale_edit.GetValue(),
                                   description=self.description_edit.GetValue())
        related_testcases = []
        for tc_id in self.testcaselist.GetItemIDByCheckState()[0]:
            tc = cTestcase(ID=tc_id)
            related_testcases.append(tc)
        requirement.setRelatedTestcases(related_testcases)

        related_usecases = []
        for uc_id in self.usecaselist.GetItemIDByCheckState()[0]:
            uc = cUsecase(ID=uc_id)
            related_usecases.append(uc)
        requirement.setRelatedUsecases(related_usecases)

        related_requirements = []
        for rq_id in self.requirementlist.GetItemIDByCheckState()[0]:
            rq = cRequirement(ID=rq_id)
            related_requirements.append(rq)
        requirement.setRelatedRequirements(related_requirements)

        requirement.setChangelog(self.GetChangelogContent())

        return requirement


    def ValidateRequirement(self):
        (result, msg) = self.validator_hook(self.initial_requirement, self.GetContent())
        if result != 0:
            wx.MessageBox(msg, "Error", wx.ICON_ERROR)
        if result == 1:
            # set focus to changelog description
            self.ChangeSelection(5)
            self.changelogpanel.changelog_edit.SetFocus()
        return result == 0


