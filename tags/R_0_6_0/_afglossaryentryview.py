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
from _aftextctrl import *
from _afvalidators import NotEmptyValidator
from _afartefact import cGlossaryEntry


class afGlossaryEntryView(wx.Panel):
    def __init__(self, parent, id = -1, viewonly = True):
        wx.Panel.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize)
        title_text = wx.StaticText(self, -1, _("Term")+':')
        description_text = wx.StaticText(self, -1, _("Description")+':')
        id_text = wx.StaticText(self, -1, _("ID")+':')

        if viewonly:
            self.title_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY)
            self.description_edit = afHtmlWindow(self, -1)
        else:
            self.title_edit = wx.TextCtrl(self, -1, "", validator = NotEmptyValidator())
            self.description_edit = afTextCtrl(self)

        self.id_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY)
        self.id_edit.Enable(False)

        sizer = wx.FlexGridSizer(3, 2, 10, 10)
        sizer.Add(title_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.title_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(id_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.id_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(description_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.description_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.AddGrowableRow(2)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(hbox)
        self.Layout()

    def InitContent(self, glossaryentry):
        self.title_edit.SetValue(glossaryentry["title"]);
        self.description_edit.SetValue(glossaryentry["description"]);
        self.id_edit.SetValue(str(glossaryentry['ID']))
        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()

    def GetContent(self):
        return cGlossaryEntry(title=self.title_edit.GetValue(),
            description=self.description_edit.GetValue(),
            ID=int(self.id_edit.GetValue()))

    def UpdateContent(self, artefact):
        self.id_edit.SetValue(str(artefact['ID']))

    def ChangeSelection(self, n):
        pass

