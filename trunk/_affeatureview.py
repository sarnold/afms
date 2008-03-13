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
import afconfig
import _afbasenotebook
from afresource import _
import afresource

class afFeatureNotebook(_afbasenotebook.afBaseNotebook):
    def __init__(self, parent, id = -1, viewonly = True):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style= wx.BK_DEFAULT)
        self.viewonly = viewonly
        color = parent.GetBackgroundColour()
        self.SetOwnBackgroundColour(color)
        panel = wx.Panel(self, -1)
        panel.SetOwnBackgroundColour(color)
        labels = [_("Title"), _("ID"), _("Version"), _("Priority"), _("Status"), _("Risk"), _("Description")]
        
        (width, height) = (0, 0)
        statictext = []
        for label in labels:
            st = wx.StaticText(panel, -1, label+':')
            (w, h) = st.GetSize()
            (width, height) =  (max(width, w), max(height, h))
            statictext.append(st)

        for st in statictext:
            st.SetMinSize((width,height))

        if viewonly:
            self.title_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.id_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.version_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.priority_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.status_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.risk_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.description_edit = afHtmlWindow(panel, -1)
        else:
            self.title_edit = wx.TextCtrl(panel, -1, "", validator = NotEmptyValidator())
            self.id_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.version_edit = wx.TextCtrl(panel, -1, "")
            self.priority_edit = wx.ComboBox(panel, -1, choices = afresource.PRIORITY_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.status_edit = wx.ComboBox(panel, -1, choices = afresource.STATUS_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.risk_edit = wx.ComboBox(panel, -1, choices = afresource.RISK_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.description_edit = wx.TextCtrl(panel, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB )
            
        self.id_edit.Enable(False)
        edit = [self.title_edit, self.id_edit, self.version_edit, self.priority_edit, \
                self.status_edit, self.risk_edit, self.description_edit]
        
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer = wx.FlexGridSizer(1, 2, 10, 10)
        sizer.Add(statictext[0], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(edit[0], 0, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)

        mainsizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        sizer = wx.FlexGridSizer(3, 4, 10, 10)
        for i in range(1, 6):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
            sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)

        mainsizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)

        sizer = wx.FlexGridSizer(1, 2, 10, 10)
        sizer.Add(statictext[6], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(edit[6], 1, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(0, 1)
        sizer.SetFlexibleDirection(wx.BOTH)

        mainsizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)

        panel.SetSizer(mainsizer)

        panel.Layout()
        self.AddPage(panel, _("Feature"))
        
        panel = wx.Panel(self, -1)
        self.requirementlist = afRequirementList(panel, -1, checkstyle=not self.viewonly)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.requirementlist, 1, wx.ALL| wx.EXPAND, 6)
        panel.SetSizer(sizer)
        self.AddPage(panel, _("Attached Requirements"))
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)

        self.AddChangelogPanel()
        

    def OnListItemActivated(self, evt):
        # Ignore double clicks in lists (related requirements, ...)
        pass


    def InitContent(self, featuredata):
        """
        Feature data is a tuple:
        ID, title, priority, status, version, description
        """
        (basedata, requirements, changelist) = featuredata[0], featuredata[1], featuredata[2]
        (related_requirements_list, unrelated_requirements_list) = requirements
        
        self.id_edit.SetValue(str(basedata[0]))
        self.title_edit.SetValue(basedata[1])
        self.priority_edit.SetValue(afresource.PRIORITY_NAME[basedata[2]])
        self.status_edit.SetValue(afresource.STATUS_NAME[basedata[3]])
        self.version_edit.SetValue(basedata[4])
        self.risk_edit.SetValue(afresource.RISK_NAME[basedata[5]])
        self.description_edit.SetValue(basedata[6])
        
        self.requirementlist.InitCheckableContent(unrelated_requirements_list, related_requirements_list, self.viewonly)

        if self.viewonly:
            self.changelist.InitContent(changelist)
        else:
            self.validator_hook = featuredata[3]
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
            self.risk_edit.GetCurrentSelection(),
            self.description_edit.GetValue())
        return basedata


    def GetContent(self):
        basedata = self.GetBasedata()            
        (requirements) = self.requirementlist.GetItemIDByCheckState()
        return (basedata, requirements, self.GetChangelogContent())


    def ValidateRequirement(self):
        (result, msg) = self.validator_hook(self.initial_basedata, self.GetBasedata(), self.GetChangelogContent())
        if result != 0:
            wx.MessageBox(msg, _("Error"), wx.ICON_ERROR)
        if result == 1:
            # set focus to changelog description
            self.ChangeSelection(2)
            self.changelog_edit.SetFocus()
        return result == 0
