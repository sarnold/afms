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
from _afvalidators import NotEmptyValidator
from _afartefactlist import afChangeList
import afresource, afconfig
from _afartefact import cChangelogEntry

class afChangelogEntryView(wx.Panel):
    def __init__(self, parent, id = -1, viewonly = True):
        wx.Panel.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize)
        self.viewonly = viewonly
        if self.viewonly:
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.changelist = afChangeList(self, -1, checkstyle=False)
            sizer.Add(self.changelist, 2, wx.BOTTOM| wx.EXPAND, 3)
        else:
            sizer = wx.FlexGridSizer(3, 2, 10, 10)
            self.changelog_edit = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
            self.changedate_edit = wx.TextCtrl(self, -1, time.strftime(afresource.TIME_FORMAT), style = wx.TE_READONLY)
            #TODO: think about where the user name should come from
            self.changeuser_edit = wx.TextCtrl(self, -1, afconfig.CURRENT_USER, style = wx.TE_READONLY)
            self.timer = wx.Timer(self)
            self.timer.Start(1000)
            self.Bind(wx.EVT_TIMER, self.OnTimer)

            labels = [_("Date"), _("User"), _("Description")]

            statictext = [wx.StaticText(self, -1, label+':') for label in labels]
            edit = [self.changedate_edit, self.changeuser_edit, self.changelog_edit]

            for i in range(3):
                sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
                sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)
            sizer.AddGrowableCol(1)
            sizer.AddGrowableRow(2)
            sizer.SetFlexibleDirection(wx.BOTH)

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 6)
        self.SetSizer(mainsizer)
        self.Layout()


    def OnTimer(self, evt):
        self.changedate_edit.SetValue(time.strftime(afresource.TIME_FORMAT))


    def GetContent(self):
        changelogentry = cChangelogEntry(user=self.changeuser_edit.GetValue(),
                                         description=self.changelog_edit.GetValue(),
                                         date=self.changedate_edit.GetValue())
        return changelogentry


    def InitContent(self, changelist):
        if self.viewonly:
            self.changelist.InitContent(changelist)
        else:
            self.changelog_edit.SetFocus()
