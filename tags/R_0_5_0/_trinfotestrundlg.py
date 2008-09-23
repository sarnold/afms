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
from _trtestresultview import *

class InfoTestrunDialog(wx.Dialog):
    def __init__(self, parent, info=None):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        wx.Dialog.__init__(self, parent, -1, _("Test Run Info"), pos=wx.DefaultPosition, size=wx.DefaultSize, style=style)

        panel = wx.Panel(self, -1)

        labels = (_("Product"), _("Creation date"), _("Test run\ndescription"), _("Tester"), _("AF Database"),
                  _("Test suite ID"), _("Test suite title"), _("Test suite\ndescription"), _("Test case order"))

        statictext = []
        for label in labels:
            st = wx.StaticText(self, -1, label + ':')
            statictext.append(st)

        edit = []
        edit.append(wx.TextCtrl(self, -1, info['product_title'], style = wx.TE_READONLY))
        edit.append(wx.TextCtrl(self, -1, info['creation_date'], style = wx.TE_READONLY))
        w = afHtmlWindow(self, -1)
        w.SetValue(info['description'])
        edit.append(w)
        edit.append(wx.TextCtrl(self, -1, info['tester'], style = wx.TE_READONLY))
        edit.append(wx.TextCtrl(self, -1, info['afdatabase'], style = wx.TE_READONLY))
        edit.append(wx.TextCtrl(self, -1, info['testsuite_id'], style = wx.TE_READONLY))
        edit.append(wx.TextCtrl(self, -1, info['testsuite_title'], style = wx.TE_READONLY))
        w = afHtmlWindow(self, -1)
        w.SetValue(info['testsuite_description'])
        edit.append(w)
        edit.append(wx.TextCtrl(self, -1, info['testsuite_execorder'], style = wx.TE_READONLY))

        s = edit[0].GetSize()
        s[0] += 300
        edit[0].SetMinSize(s)

        sizer = wx.FlexGridSizer(9, 2, 10, 10)
        for i in range(len(labels)):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_RIGHT)
            sizer.Add(edit[i], 1, wx.EXPAND | wx.ALIGN_LEFT)

        sizer.SetFlexibleDirection(wx.BOTH)
        sizer.AddGrowableRow(2, 1)
        sizer.AddGrowableRow(7, 1)
        sizer.AddGrowableCol(1)

        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(hbox)

        self.Layout()

        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btnsizer.Realize()
        hbox.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.Fit()
        self.SetMinSize(self.GetSize())
