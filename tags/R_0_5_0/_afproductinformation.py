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


class afProductInformation(wx.Panel):
    def __init__(self, parent, id = -1, viewonly = True):
        wx.Panel.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize)
        title_text = wx.StaticText(self, -1, _("Title")+':')
        description_text = wx.StaticText(self, -1, _("Description")+':')

        if viewonly:
            self.title_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY)
            self.description_edit = afHtmlWindow(self, -1)
        else:
            self.title_edit = wx.TextCtrl(self, -1, "", validator = NotEmptyValidator())
            self.description_edit = afTextCtrl(self)

        sizer = wx.FlexGridSizer(2, 2, 10, 10)
        sizer.Add(title_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.title_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(description_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.description_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.AddGrowableRow(1)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(hbox)
        self.Layout()

    def InitContent(self, product_info):
        self.title_edit.SetValue(product_info["title"]);
        self.description_edit.SetValue(product_info["description"]);
        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()

    def GetContent(self):
        return {"title": self.title_edit.GetValue(),
                "description" : self.description_edit.GetValue()}

if __name__ == "__main__":
    import unittest

    class TestURL(unittest.TestCase):
        def setUp(self):
            app = wx.App(redirect=False)
            frame = wx.Frame(None)
            self.m = MyHtmlWindow(frame, -1)
            self.cwd = os.getcwd()
            self.cwd = self.cwd.replace("\\", "/")
            if "wxMSW" in wx.PlatformInfo:
                self.cwd = self.cwd[2:]

        def testFileURL1(self):
            url = "test.gif"
            r =  self.m.OnOpeningURL(wx.html.HTML_URL_IMAGE, url)
            self.assertEqual(r, "file://" + self.cwd + "/" + url)
            r =  self.m.OnOpeningURL(wx.html.HTML_URL_IMAGE, r)
            self.assertEqual(r, wx.html.HTML_OPEN)

        def testFileURL2(self):
            url = "file://test.gif"
            r =  self.m.OnOpeningURL(wx.html.HTML_URL_IMAGE, url)
            self.assertEqual(r, wx.html.HTML_OPEN)

        def testHTTPURL(self):
            url = "http://www.google.com"
            r =  self.m.OnOpeningURL(wx.html.HTML_URL_IMAGE, url)
            self.assertEqual(r, wx.html.HTML_OPEN)

    unittest.main()
