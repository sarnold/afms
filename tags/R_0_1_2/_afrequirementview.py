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

import wx
from _afhtmlwindow import *
from _afartefactlist import *
from _afvalidators import NotEmptyValidator, ArtefactHookValidator
import _afbasenotebook
import afconfig
import afresource
from afresource import _

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
            self.priority_edit = wx.ComboBox(panel1, -1, choices = afresource.PRIORITY_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.status_edit = wx.ComboBox(panel1, -1, choices = afresource.STATUS_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.complexity_edit = wx.ComboBox(panel1, -1, choices = afresource.COMPLEXITY_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.assigned_edit = wx.ComboBox(panel1, -1, choices = afresource.ASSIGNED_NAME, style=wx.CB_DROPDOWN)
            self.effort_edit = wx.ComboBox(panel1, -1, choices = afresource.EFFORT_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.category_edit = wx.ComboBox(panel1, -1, choices = afresource.CATEGORY_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.description_edit = wx.TextCtrl(panel1, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
            self.origin_edit = wx.TextCtrl(panel2, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
            self.rationale_edit = wx.TextCtrl(panel2, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)

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

        self.AddChangelogPanel()
        

    def InitContent(self, requirementdata):
        """
        basedata  is a tuple:
        (ID, title, priority, status, version, complexity, assigned, effort, category, origin, rationale, description),
        relatedtestcaselist, unrelatedtestcaselist
        """
        basedata = requirementdata[0]
        
        self.id_edit.SetValue(str(basedata[0]))
        self.title_edit.SetValue(basedata[1])
        self.priority_edit.SetValue(afresource.PRIORITY_NAME[basedata[2]])
        self.status_edit.SetValue(afresource.STATUS_NAME[basedata[3]])
        self.version_edit.SetValue(basedata[4])
        self.complexity_edit.SetValue(afresource.COMPLEXITY_NAME[basedata[5]])
        self.assigned_edit.SetValue(basedata[6])
        self.effort_edit.SetValue(afresource.EFFORT_NAME[basedata[7]])
        self.category_edit.SetValue(afresource.CATEGORY_NAME[basedata[8]])
        self.origin_edit.SetValue(basedata[9])
        self.rationale_edit.SetValue(basedata[10])
        self.description_edit.SetValue(basedata[11])
        
        testcases = requirementdata[1]
        (relatedtestcases, unrelatedtestcases) = testcases
        self.testcaselist.InitCheckableContent(unrelatedtestcases, relatedtestcases, self.viewonly)
        
        usecases = requirementdata[2]
        (relatedusecases, unrelatedusecases) = usecases
        self.usecaselist.InitCheckableContent(unrelatedusecases, relatedusecases, self.viewonly)
        
        features = requirementdata[3]
        self.featurelist.InitContent(features)
        
        if self.viewonly:
            changelist = requirementdata[4]
            self.changelist.InitContent(changelist)
        else:
            self.validator_hook = requirementdata[5]
            self.initial_basedata = basedata
            self.changelog_edit.SetValidator(ArtefactHookValidator(self.ValidateRequirement))
            
        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()
        
        
    def GetBasedata(self):
        basedata = (int(self.id_edit.GetValue()),
            self.title_edit.GetValue(),
            self.priority_edit.GetCurrentSelection(),
            self.status_edit.GetCurrentSelection(),
            self.version_edit.GetValue(),
            self.complexity_edit.GetCurrentSelection(),
            self.assigned_edit.GetValue(),
            self.effort_edit.GetCurrentSelection(),
            self.category_edit.GetCurrentSelection(),
            self.origin_edit.GetValue(),
            self.rationale_edit.GetValue(),
            self.description_edit.GetValue())
        return basedata


    def GetContent(self):
        (testcases) = self.testcaselist.GetItemIDByCheckState()
        (usecases) = self.usecaselist.GetItemIDByCheckState()
        return (self.GetBasedata(), testcases, usecases, self.GetChangelogContent())
    
    
    def ValidateRequirement(self):
        (result, msg) = self.validator_hook(self.initial_basedata, self.GetBasedata(), self.GetChangelogContent())
        if result != 0:
            wx.MessageBox(msg, "Error", wx.ICON_ERROR)
        if result == 1:
            # set focus to changelog description
            self.ChangeSelection(5)
            self.changelog_edit.SetFocus()
        return result == 0
    

