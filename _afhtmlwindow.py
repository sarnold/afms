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

import logging
import wx
import  wx.html as  html
import webbrowser, urlparse, os
import afconfig
import _afdocutils
from afresource import _

class afHtmlWindow(html.HtmlWindow):
    def __init__(self, parent, id, size=wx.DefaultSize, enablescriptexec=False):
        self.watchdog = 0
        self.script_execution_enabled = enablescriptexec
        html.HtmlWindow.__init__(self, parent, id, size=size,
            style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.BORDER_STATIC)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()
            
        if "wxMSW" in wx.PlatformInfo:
            # Original font sizes are [7, 8, 10, 12, 16, 22, 30]
            _FONT_SIZES = [5, 6,  8, 10, 14, 20, 24]
            self.SetFonts("MS Sans Serif", "Courier New", _FONT_SIZES)
        else:
            #FIXME: consider other platforms
            pass

    def _MakeLocalURL(self, url):
        logging.debug("_afhtmlwindows._MakeLocalURL(%s)" % url)
        lst = urlparse.urlsplit(url)
        if lst.scheme != "file":
            return url

        path = url[7:]
        cwd = os.getcwd()
        cwd = cwd.replace("\\", "/")
        if not path.startswith(cwd):
            path = cwd + "/" + path
        url = "file:///" + path
        logging.debug("\t==> %s" % url)
        return url

    def OnLinkClicked(self, linkinfo):
        url = linkinfo.GetHref()
        lst = urlparse.urlsplit(url)
        if lst.scheme == "script":
            if self.script_execution_enabled:
                path = lst[2]
                if path.startswith('//'):
                    path = path[2:]
                if "wxMSW" in wx.PlatformInfo:
                    path = path.replace("/", "\\")
                logging.debug("afHTMLWindow.OnLinkClicked ==> os.system(%s)" % path)
                os.system(path)
            else:
                wx.MessageBox(_("Unable to execute %s\nScript execution is disabled.") % url, "AF Editor", wx.ICON_ERROR|wx.OK)
        else:
            webbrowser.open(url=self._MakeLocalURL(url), new=2)

    def OnOpeningURL(self, urltype, url):
        return wx.html.HTML_OPEN
    
    def SetValue(self, value):
        """
        Set value to display.
        If value is not HTML code, i.e. does not start with a <html> tag,
        then mask special HTML chars and replace
        line breaks with <br> tags to give proper line wrapping
        """
        value = value.strip()
        if value.startswith((".. rest", ".. REST")):
            value = _afdocutils.html_body(value, doctitle=0, initial_header_level=3)
        elif not value.startswith(("<html>", "<HTML>")):
            value = value.replace("&", "&amp;");
            value = value.replace(">", "&gt;")
            value = value.replace("<", "&lt;")
            value = value.replace('"', "&quot;")
            lines = value.split("\n")
            value = "<br>".join(lines)
        self.SetPage(value)

        
    logging.basicConfig(level=afconfig.loglevel, format=afconfig.logformat)

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
