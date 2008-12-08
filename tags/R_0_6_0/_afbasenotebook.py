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

import time
import wx
from _afhtmlwindow import *
from _afartefactlist import afChangeList, afTagList
import afresource
from _afartefact import cChangelogEntry, cTag
from _afchangelogentryview import afChangelogEntryView

class afBaseNotebook(wx.Notebook):
    def __init__(self, parent, id = -1, viewonly = True):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style= wx.BK_DEFAULT)
        self.viewonly = viewonly

    def OnListItemActivated(self, evt):
        # Ignore double clicks in lists (related testcases, ...)
        pass


    def EvtTextEnter(self, event):
        event.Skip()


    def AddRelatedArtefactPanel(self, afList, title):
        panel = wx.Panel(self, -1)
        _list = afList(panel, -1, checkstyle=False)
        sizer = wx.BoxSizer(wx.VERTICAL)
        if not self.viewonly:
            bmp =  wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_CMN_DIALOG, (32, 32))
            sb = wx.StaticBitmap(panel, -1, bmp)
            st = wx.StaticText(panel, -1, _("This list could not be edited here"))
            st.SetForegroundColour("Red")
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            hsizer.Add(sb, 0, wx.RIGHT, 10)
            hsizer.Add(st, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL , 10)
            sizer.Add(hsizer, 0, wx.ALL|wx.EXPAND, 6)
        sizer.Add(_list, 1, wx.ALL| wx.EXPAND, 6)
        panel.SetSizer(sizer)
        self.AddPage(panel, title)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        return _list


    def AddChangelogPanel(self):
        if self.viewonly:
            panel = wx.Panel(self, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.changelist = afChangeList(panel, -1, checkstyle=False)
            sizer.Add(self.changelist, 2, wx.BOTTOM| wx.EXPAND, 3)
            panel.SetSizer(sizer)
        else:
            panel = afChangelogEntryView(self, viewonly=self.viewonly)
        self.changelogpanel = panel
        self.AddPage(panel, _('Changelog'))


    def AddTagsPanel(self):
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.tagslist = afTagList(panel, -1, checkstyle=not self.viewonly)
        sizer.Add(self.tagslist, 2, wx.BOTTOM| wx.EXPAND, 3)
        panel.SetSizer(sizer)
        self.tagspanel = panel
        self.AddPage(panel, _('Tags'))


    def InitTags(self, tags):
        import afconfig
        checked_taglist = []
        unchecked_taglist = []
        index = 0
        for tag in afconfig.TAGLIST:
            if cTag.index2tagchar(index) in tags:
                checked_taglist.append(tag)
            else:
                unchecked_taglist.append(tag)
            index += 1
        if self.viewonly:
            self.tagslist.InitContent(checked_taglist)
        else:
            self.tagslist.InitCheckableContent(unchecked_taglist, checked_taglist)


    def GetTags(self):
        s = ''
        for id in self.tagslist.GetItemIDByCheckState()[0]:
            s += cTag.index2tagchar(id-1)
        return s


    def GetChangelogContent(self):
        return self.changelogpanel.GetContent()


    def OnTimer(self, evt):
        self.changedate_edit.SetValue(time.strftime(afresource.TIME_FORMAT))


    def UpdateContent(self, artefact):
        self.id_edit.SetValue(str(artefact['ID']))
