# -*- coding: utf-8 -*-

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
import  wx.gizmos   as  gizmos
import afresource

class EditSimpleSectionLevelDialog(wx.Dialog):
    def __init__(self, items, parent=None):
        wx.Dialog.__init__(self, parent, title=_('Edit text section order'), style=wx.RESIZE_BORDER|wx.DEFAULT_DIALOG_STYLE)
        self.SetMinSize((400, -1))
        self.SetSize(self.GetMinSize())
        self.items = items

        self.elb = gizmos.EditableListBox(self, -1, _("Text sections"), style=0)
        self.elb.SetStrings(items)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.elb, 1, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

    def GetItems(self):
        return self.elb.GetStrings()
