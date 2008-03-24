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
import afconfig
from afresource import _
import afresource

        
class afTrashInformation(wx.Panel):
    def __init__(self, parent, id = -1):
        wx.Panel.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize)
        
        title = wx.StaticText(self, -1, _("Trash overview"))
        font = title.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        
        sizer = wx.FlexGridSizer(len(afresource.ARTEFACTS), 2, 10, 10)
        statictext = []
        self.edit = []
        for af in afresource.ARTEFACTS:
            statictext.append(wx.StaticText(self, -1, _("Number of %s in Trash:") % af["name"]))
            self.edit.append(wx.TextCtrl(self, -1, "", style = wx.TE_READONLY))
            sizer.Add(statictext[-1], 0, wx.EXPAND | wx.ALIGN_BOTTOM )
            sizer.Add(self.edit[-1], 0, wx.EXPAND | wx.ALIGN_BOTTOM )
            
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(title, 0, wx.ALL | wx.EXPAND, 5)
        hbox.AddSpacer(15)
        hbox.Add(sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(hbox)
        self.Layout()

    def InitContent(self, trash_info):
        for af, e in zip(afresource.ARTEFACTS, self.edit):
            e.SetValue(str(trash_info[af["id"]]))
        self.Show()
        self.GetParent().Layout()
        
        
