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
from _trtestcaseview import *

class ExecTestrunDialog(wx.Dialog):
    def __init__(self, parent, ID, title):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        size = parent.GetSize()
        wx.Dialog.__init__(self, parent, ID, title, pos=parent.GetScreenPosition(), size=size, style=style)
        # need this to enable validation in all subwindows
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        self.SetMinSize(size)
        
        self.leftPanel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        self.rightPanel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.leftPanel, 1, wx.ALL | wx.EXPAND, 0)
        hbox.Add(self.rightPanel, 1, wx.ALL | wx.EXPAND, 0)

        self.testresultview = trTestresultPanel(self.rightPanel, viewonly = False)
        self.testcaseview = trTestcasePanel(self.leftPanel)
        
        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_SAVE)
        at = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE )])
        self.SetAcceleratorTable(at)
        self.SetAffirmativeId(wx.ID_SAVE)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hbox, 1, wx.ALL | wx.EXPAND, 6)
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

        
