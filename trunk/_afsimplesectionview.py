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
from _afhtmlwindow import *
from _aftextctrl import *
from _afartefactlist import *
from _afvalidators import NotEmptyValidator
import _afbasenotebook
import afconfig
from _afartefact import cSimpleSection


class afSimpleSectionNotebook(_afbasenotebook.afBaseNotebook):
    def __init__(self, parent, id = -1, viewonly = True):
        _afbasenotebook.afBaseNotebook.__init__(self, parent, id, viewonly)
        color = parent.GetBackgroundColour()
        self.SetOwnBackgroundColour(color)
        panel = wx.Panel(self, -1)
        panel.SetOwnBackgroundColour(color)
        labels = [_('Title'), _('ID'), _('Level'), _('Content')]
        statictext = []
        for label in labels:
            st = wx.StaticText(panel, -1, label+':')
            statictext.append(st)

        if viewonly:
            self.title_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.content_edit = afHtmlWindow(panel, -1)
        else:
            self.title_edit = wx.TextCtrl(panel, -1, "", validator = NotEmptyValidator())
            self.content_edit = afTextCtrl(panel)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.content_edit)

        self.id_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY, name='id_edit')
        self.id_edit.Enable(False)
        self.level_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY, name='level_edit')
        self.level_edit.Enable(False)

        edit = [self.title_edit, self.id_edit, self.level_edit, self.content_edit]

        sizer = wx.FlexGridSizer(4, 2, 10, 10)

        for i in range(len(labels)):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
            sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)

        sizer.AddGrowableRow(3, 1)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)
        panel.SetSizer(hbox)

        panel.Layout()
        self.AddPage(panel, _("Section"))
        self.AddChangelogPanel()
        self.panel = panel


    def InitContent(self, simplesection):
        self.id_edit.SetValue(str(simplesection['ID']))
        self.title_edit.SetValue(simplesection['title'])
        self.level_edit.SetValue(str(simplesection['level']))
        self.content_edit.SetValue(simplesection['content'])

        if self.viewonly:
            self.changelist.InitContent(simplesection.getChangelist())

        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()


    def GetContent(self):
        simplesection = cSimpleSection(ID=int(self.id_edit.GetValue()),
                             title=self.title_edit.GetValue(),
                             content=self.content_edit.GetValue(),
                             level=self.level_edit.GetValue())
        simplesection.setChangelog(self.GetChangelogContent())
        return simplesection


