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
from _afartefactlist import *
from _afvalidators import NotEmptyValidator, ArtefactHookValidator
import afconfig
import _afbasenotebook
import afresource
from _afartefact import cFeature, cRequirement

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
            self.priority_edit = wx.ComboBox(panel, -1, choices = [_(i) for i in afresource.PRIORITY_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.status_edit = wx.ComboBox(panel, -1, choices = [_(i) for i in afresource.STATUS_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.risk_edit = wx.ComboBox(panel, -1, choices = [_(i) for i in afresource.RISK_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
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


    def InitContent(self, feature):
        self.id_edit.SetValue(str(feature['ID']))
        self.title_edit.SetValue(feature['title'])
        self.version_edit.SetValue(feature['version'])
        self.description_edit.SetValue(feature['description'])
        if self.viewonly:
            self.priority_edit.SetValue(_(afresource.PRIORITY_NAME[feature['priority']]))
            self.status_edit.SetValue(_(afresource.STATUS_NAME[feature['status']]))
            self.risk_edit.SetValue(_(afresource.RISK_NAME[feature['risk']]))
        else:
            self.priority_edit.SetSelection(feature['priority'])
            self.status_edit.SetSelection(feature['status'])
            self.risk_edit.SetSelection(feature['risk'])

        self.requirementlist.InitCheckableContent(feature.getUnrelatedRequirements(), feature.getRelatedRequirements(), self.viewonly)

        if self.viewonly:
            self.changelist.InitContent(feature.getChangelist())
        else:
            self.validator_hook = feature.validator
            self.initial_feature = feature
            self.changelog_edit.SetValidator(ArtefactHookValidator(self.ValidateRequirement))

        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()


    def GetContent(self):
        feature = cFeature(ID=int(self.id_edit.GetValue()),
                           title=self.title_edit.GetValue(),
                           priority=self.priority_edit.GetCurrentSelection(),
                           status=self.status_edit.GetCurrentSelection(),
                           version=self.version_edit.GetValue(),
                           risk=self.risk_edit.GetCurrentSelection(),
                           description=self.description_edit.GetValue())

        related_requirements = []
        for rq_id in self.requirementlist.GetItemIDByCheckState()[0]:
            rq = cRequirement(ID=rq_id)
            related_requirements.append(rq)
        feature.setRelatedRequirements(related_requirements)

        feature.setChangelog(self.GetChangelogContent())

        return feature


    def ValidateRequirement(self):
        (result, msg) = self.validator_hook(self.initial_feature, self.GetContent())
        if result != 0:
            wx.MessageBox(msg, _("Error"), wx.ICON_ERROR)
        if result == 1:
            # set focus to changelog description
            self.ChangeSelection(2)
            self.changelog_edit.SetFocus()
        return result == 0
