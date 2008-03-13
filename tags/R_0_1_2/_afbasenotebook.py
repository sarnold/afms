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

import time
import wx
from _afhtmlwindow import *
from _afartefactlist import afChangeList
from afresource import _
import afresource

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
        panel = wx.Panel(self, -1)
        
        if self.viewonly:
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.changelist = afChangeList(panel, -1, checkstyle=False)
            sizer.Add(self.changelist, 2, wx.BOTTOM| wx.EXPAND, 3)
        else:
            sizer = wx.FlexGridSizer(3, 2, 10, 10)
            self.changelog_edit = wx.TextCtrl(panel, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
            self.changedate_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            #TODO: think about where the user name should come from
            self.changeuser_edit = wx.TextCtrl(panel, -1, afconfig.CURRENT_USER, style = wx.TE_READONLY)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
            self.Bind(wx.EVT_TIMER, self.OnTimer)

            labels = [_("Date"), _("User"), _("Description")]

            statictext = []
            for label in labels:
                st = wx.StaticText(panel, -1, label+':')
                statictext.append(st)

            edit = [self.changedate_edit, self.changeuser_edit, self.changelog_edit]

            for i in range(3):
                sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
                sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)
            sizer.AddGrowableCol(1)
            sizer.AddGrowableRow(2)
            sizer.SetFlexibleDirection(wx.BOTH)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 6)
        panel.SetSizer(mainsizer)
        self.AddPage(panel, _('Changelog'))


    def GetChangelogContent(self):
        return tuple([f.GetValue() for f in (self.changedate_edit, self.changeuser_edit, self.changelog_edit)])
        
        
    def OnTimer(self, evt):
        self.changedate_edit.SetValue(time.strftime(afresource.TIME_FORMAT))
