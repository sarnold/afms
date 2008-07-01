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

import  wx
        

class afTextCtrl(wx.TextCtrl):
    def __init__(self, parent, ID=-1):
        style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_RICH2
        wx.TextCtrl.__init__(self, parent, ID, style=style)
        font = self.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE )
        self.SetFont(font)


    def SetValue(self, value):
        start = self.GetInsertionPoint()
        wx.TextCtrl.SetValue(self, value)
        end = self.GetLastPosition()
        style = self.GetDefaultStyle()
        font = style.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE )
        style.SetFont(font)
        self.SetStyle(start, end, style)
