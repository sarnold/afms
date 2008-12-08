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
View statistics of current artefact database.
"""

import sys
import wx
import  wx.lib.mixins.listctrl as listmix
import afresource, _afimages

class SimpleTable(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT | wx.LC_NO_HEADER)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(0, "Key")
        self.InsertColumn(1, "Value")
        self.imagelist = wx.ImageList(16, 16)
        self.imagelist.Add(_afimages.getEmptyBitmap())
        self.imagelist.Add(wx.ArtProvider.GetBitmap(wx.ART_WARNING, size=(16,16)))
        self.imagelist.Add(wx.ArtProvider.GetBitmap(wx.ART_ERROR, size=(16,16)))
        self.SetImageList(self.imagelist, wx.IMAGE_LIST_SMALL)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        
    def OnListItemActivated(self, evt):
        pass


class StatisticsDialog(wx.Dialog):
    def __init__(self, parent, ID):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        wx.Dialog.__init__(self, parent, ID, _('Artefact statistics'), pos=wx.DefaultPosition, size=wx.DefaultSize, style=style)
        self.SetMinSize(self.GetSize())
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        
        self.table = SimpleTable(self)
        sizer.Add(self.table, 1, wx.EXPAND | wx.ALL, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)


    def InitContent(self, items):
        for item in items:
            index = self.table.InsertImageStringItem(sys.maxint, item.key, item.imageindex)
            self.table.SetStringItem(index, 1, item.value)
        self.table.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.table.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            
            
class StatisticData():
    def __init__(self, key, value, imageindex=0):
        self.key = key
        self.value = value
        self.imageindex = imageindex

        