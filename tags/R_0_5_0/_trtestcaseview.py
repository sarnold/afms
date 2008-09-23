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

"""
Sections of this code are very similar to those in _aftestcaseview.py.
Maybe it is a good idea to do some refactoring some day to prevent code duplication
"""

import wx
import wx.lib.hyperlink as hl
from _afhtmlwindow import *


class trTestcasePanel():
    def __init__(self, parent, viewonly=True):
        labels = [_("Title"),  _("ID"),  _("Version"),  _("Purpose"),  _("Prerequisite"),  _("Testdata"),  _("Steps"),
                  _('Script URL'), _("Notes &&\nQuestions")]
        statictext = []
        for label in labels:
            st = wx.StaticText(parent, -1, label + ':')
            statictext.append(st)

        self.viewonly = viewonly
        if viewonly == False:
            self.scriptlink = hl.HyperLinkCtrl(parent, wx.ID_ANY, labels[7], URL="")
            self.scriptlink.SetToolTip(wx.ToolTip('Run script'))
            self.scriptlink.AutoBrowse(False)
            statictext[7].Destroy()
            statictext[7] = self.scriptlink

        self.title_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_READONLY)
        self.id_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_READONLY)
        self.version_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_READONLY)
        self.purpose_edit = afHtmlWindow(parent, -1, enablescriptexec=True)
        self.prerequisite_edit = afHtmlWindow(parent, -1, enablescriptexec=True)
        self.testdata_edit =afHtmlWindow(parent, -1, enablescriptexec=True)
        self.steps_edit = afHtmlWindow(parent, -1, enablescriptexec=True)
        self.scripturl_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_READONLY)
        self.notes_edit = afHtmlWindow(parent, -1, enablescriptexec=True)

        self.id_edit.Enable(False)

        edit = [self.title_edit, self.id_edit, self.version_edit, self.purpose_edit,
            self.prerequisite_edit, self.testdata_edit, self.steps_edit, self.scripturl_edit, self.notes_edit]

        sizer = wx.FlexGridSizer(8, 2, 10, 10)
        sizer.Add(statictext[0], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(edit[0], 0, wx.EXPAND | wx.ALIGN_LEFT)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.id_edit, 0)
        hsizer.Add(statictext[2], 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        hsizer.Add(self.version_edit, 1, wx.LEFT | wx.EXPAND, 5)
        sizer.Add(statictext[1], 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALIGN_LEFT)

        for i in range(3, len(labels)):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
            sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)

        sizer.AddGrowableRow(2, 2)
        sizer.AddGrowableRow(3, 2)
        sizer.AddGrowableRow(4, 1)
        sizer.AddGrowableRow(5, 2)
        sizer.AddGrowableRow(7, 1)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)
        parent.SetSizer(hbox)

        parent.Layout()


    def InitContent(self, testcase):
        self.title_edit.SetValue(testcase['title'])
        self.id_edit.SetValue(str(testcase['ID']))
        self.version_edit.SetValue(testcase['version'])
        self.purpose_edit.SetValue(testcase['purpose'])
        self.prerequisite_edit.SetValue(testcase['prerequisite'])
        self.testdata_edit.SetValue(testcase['testdata'])
        self.steps_edit.SetValue(testcase['steps'])
        if self.viewonly==False:
            if len(testcase['scripturl']) > 0:
                self.scriptlink.SetURL(testcase['scripturl'])
            else:
                self.scriptlink.Disable()
        self.scripturl_edit.SetValue(testcase['scripturl'])
        self.notes_edit.SetValue(testcase['notes'])


    def OnRunScript(self, evt):
        print '_trtestcaseview.OnRunScript'
        evt.Skip()
