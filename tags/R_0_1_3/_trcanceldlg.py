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
from _afvalidators import *
from afresource import _

class CancelTestrunDialog(wx.Dialog):
    def __init__(self, parent, info=None):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        wx.Dialog.__init__(self, parent, -1, _("Cancel Test Run"), pos=wx.DefaultPosition, size=wx.DefaultSize, style=style)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(self, -1, _("Enter reason for cancelation")+ ':'), 0, wx.EXPAND|wx.ALL, 5)
        self.reason = wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE, validator = NotEmptyValidator())
        self.reason.SetMinSize((320, 240))
        box.Add(self.reason, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(box)
        self.Layout()

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        box.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.Fit()
        self.SetMinSize(self.GetSize())
        
    def GetValue(self):
        return self.reason.GetValue()
