#!/usr/bin/env python
# -*- coding: utf-8  -*-

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
Test runner dialog to run all scripted testcases in a batch

@author: Achim Koehler
@version: $Rev$
"""

import wx
from _afartefactlist import afArtefactList

class afTestcaseList(afArtefactList):
    """Widget for displaying testcase lists"""
    def __init__(self, parent, ID = -1, checkstyle=False):
        self.column_titles = [_('ID'), _('Title'), _('Version'), _('Script URL'), _('Purpose')]
        self.key = "TESTCASES"
        afArtefactList.__init__(self, parent, self.column_titles, ID, checkstyle=checkstyle)


    def FormatRow(self, tcobj):
        return (self.idformat % tcobj['ID'],
                tcobj['title'],
                tcobj['version'],
                self.toText(tcobj['scripturl']),
                self.toText(tcobj['purpose']))


class BatchTestrunDialog(wx.Dialog):
    def __init__(self, parent, ID, title):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        size = parent.GetSize()
        wx.Dialog.__init__(self, parent, ID, title, pos=parent.GetScreenPosition(), size=size, style=style)
        self.SetMinSize(size)

        self.testcaselist = afTestcaseList(self, checkstyle=True)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.Ignore)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Ignore)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK, label=_('Run selected'))
        at = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('R'), wx.ID_OK )])
        self.SetAcceleratorTable(at)
        self.SetAffirmativeId(wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.testcaselist, 1, wx.ALL | wx.EXPAND, 5)
        vbox.Add(btnsizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(vbox)


    def Ignore(self, evt):
        pass