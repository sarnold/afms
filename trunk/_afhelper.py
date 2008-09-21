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

import os, sys, traceback
if __name__=="__main__":
    import sys, gettext
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)
import wx
from _afchangelogentryview import *
import afinfo, _afhtmlwindow


def ShowFeedbackDialog(parent):
        dlg = wx.Dialog(parent, -1, _('How to give feedback'), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER )
        size = dlg.GetSize()
        dlg.SetMinSize(size)
        size = (int(size[0]*1.5), int(size[1]*1.5))
        dlg.SetSize(size)
        info = wx.AboutDialogInfo()
        info = afinfo.getInfo(info)
        htmlwin = _afhtmlwindow.afHtmlWindow(dlg, -1)
        htmlwin.SetPage(info.feedback)
        sizer = dlg.CreateStdDialogButtonSizer(wx.OK)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(htmlwin, 1, wx.EXPAND | wx.ALL, 5)
        vsizer.Add(sizer, 0, wx.EXPAND | wx.ALL, 5)
        dlg.SetSizer(vsizer)
        dlg.ShowModal()


class ExceptionViewDialog(wx.Dialog):
    def __init__(self, parent, title, briefmsg, detailedmsg):
        wx.Dialog.__init__(self, parent, id=-1, title=title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        st = wx.StaticText(self, label=briefmsg)
        font = st.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        st.SetFont(font)
        tb = wx.TextCtrl(self, -1, detailedmsg, style=wx.TE_MULTILINE | wx.TE_READONLY );
        bmp = wx.ArtProvider.GetBitmap(wx.ART_ERROR)
        sb = wx.StaticBitmap(self, -1, bmp)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(sb, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL , 5)
        hsizer.Add(st, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL , 5)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer, 0, wx.ALL, 5)
        sizer.Add(tb, 1, wx.ALL|wx.EXPAND, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(sizer)


def ExceptionMessageBox(exceptiondata, title="Exception"):
    """exceptiondata is tuple (exc_type, exc_value, exc_traceback) as returned from
    sys.exc_info()
    """
    brief = ''.join(traceback.format_exception_only(exceptiondata[0], exceptiondata[1]))
    details = ''.join(traceback.format_exception(exceptiondata[0], exceptiondata[1], exceptiondata[2]))
    dlg = ExceptionViewDialog(None, title, brief, details)
    dlg.ShowModal()
    

class DontAnnoyYesNoDialog(wx.Dialog):
    def __init__(self, message, title=""):
        wx.Dialog.__init__(self, parent=None, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer =  wx.BoxSizer(wx.HORIZONTAL)
        question_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_TOOLBAR, (32, 32))
        sb = wx.StaticBitmap(self, -1, question_bmp)
        hsizer.Add(sb, 0, wx.ALIGN_LEFT | wx.RIGHT, 15)

        label = wx.StaticText(self, -1, message)
        label.Wrap(400)
        hsizer.Add(label, 0, wx.ALIGN_LEFT|wx.LEFT, 15)

        sizer.Add(hsizer, 0, wx.ALIGN_CENTRE|wx.ALL, 15)

        self.cb = wx.CheckBox(self, -1, _("Don't ask again in this session"))
        sizer.Add(self.cb, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 15)
        sizer.Add((10,10))


        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_YES)
        self.SetAffirmativeId(wx.ID_YES)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_NO)
        self.SetEscapeId(wx.ID_NO)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


def DontAnnoyMessageBox(title, message):
    dlg = DontAnnoyYesNoDialog(title, message)
    dlgresult = dlg.ShowModal()
    dont_annoy = dlg.cb.GetValue()
    dlg.Destroy()
    return (dlgresult, dont_annoy)


class ChangelogEntryDialog(wx.Dialog):
    def __init__(self, title=""):
        wx.Dialog.__init__(self, parent=None, title=title, style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = afChangelogEntryView(self, viewonly=False)
        sizer.Add(self.panel, 1, wx.EXPAND)

        btnsizer = wx.StdDialogButtonSizer()
        btnsizer.AddButton(wx.Button(self, wx.ID_OK))
        btnsizer.AddButton(wx.Button(self, wx.ID_CANCEL))
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.SetMinSize((600,400))
        self.SetSize(self.GetMinSize())
        self.Layout()


def ChangelogEntryMessageBox(title):
    dlg = ChangelogEntryDialog(title)
    dlgresult = dlg.ShowModal()
    cle = dlg.panel.GetContent()
    dlg.Destroy()
    return (dlgresult, cle)


class ArchiveToDBDialog(wx.Dialog):
    def __init__(self, parent, id=-1):
        wx.Dialog.__init__(self, parent, id, title=_('Convert archive to database'))

        fbc = { 'labelText' : _('Archive file') + ':',
                'fileDialogStyle' : wx.OPEN | wx.CHANGE_DIR,
                'fileDialogTitle' : _('Choose archive file'),
                'callbackFunc' : self._ArchiveFileCallback,
                'fileWildcard' : afresource.XML_WILDCARD}
        self.infilebrowser = SimpleFileBrowser(self, **fbc)
        fbc = { 'labelText' : _('Database file') + ':',
                'fileDialogStyle' : wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT,
                'fileDialogTitle' : _('Save database file'),
                'callbackFunc' : self._DatabaseFileCallback,
                'fileWildcard' : afresource.AF_WILDCARD}
        self.outfilebrowser = SimpleFileBrowser(self, **fbc)
        self.outfilebrowser.AlignWith(self.infilebrowser)

        self.openflag = wx.CheckBox(self, -1, _('Open database after conversion'))
        self.openflag.SetValue(True)

        btnsizer = wx.StdDialogButtonSizer()
        self.okbtn = wx.Button(self, wx.ID_OK)
        self.okbtn.SetDefault()
        self.okbtn.Enable(False)
        btnsizer.AddButton(self.okbtn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.infilebrowser, 0, wx.EXPAND | wx.ALL, 15)
        mainsizer.Add(self.outfilebrowser, 0, wx.EXPAND | wx.ALL, 15)
        mainsizer.Add(self.openflag, 0, wx.EXPAND | wx.ALL, 15)
        mainsizer.Add(btnsizer, 0, wx.EXPAND | wx.ALL, 15)
        self.SetSizer(mainsizer)
        mainsizer.SetMinSize((400, -1))
        mainsizer.Fit(self)

        self.Layout()

    def _ArchiveFileCallback(self, path):
        if len(path) <= 0:
            self.okbtn.Enable(False)
            return
        if len(self.outfilebrowser.GetValue()) <= 0:
            path = os.path.splitext(path)[0] + ".af"
            self.outfilebrowser.SetValue(path)
            self.okbtn.Enable(True)
        else:
            self.okbtn.Enable(True)

    def _DatabaseFileCallback(self, path):
        if len(path) <= 0:
            self.okbtn.Enable(False)
            return
        if len(self.infilebrowser.GetValue()) <= 0:
            self.okbtn.Enable(False)
            return
        self.okbtn.Enable(True)

    def GetValue(self):
        return (self.infilebrowser.GetValue(), self.outfilebrowser.GetValue(), self.openflag.GetValue())


def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")


def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))

    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))


def getRelFolder(reffolder, folder):
    if reffolder == folder:
        return ''
    commonprefix = os.path.commonprefix([reffolder, folder])
    if commonprefix != '':
        folder = folder[len(commonprefix):]
        reffolder = reffolder[len(commonprefix):]
        if reffolder.startswith(os.sep):
            reffolder = reffolder.lstrip(os.sep)
        n = len(reffolder.split(os.sep))
        relfolder = os.sep.join(['..'] * n)
        folder =  os.path.join(relfolder, folder)
        if folder.startswith(os.sep):
            folder = folder.lstrip(os.sep)
    return folder


def getRelPath(path):
    # try to compute relative path
    reffolder = afconfig.basedir
    folder = os.path.dirname(path)
    path = os.path.join(getRelFolder(reffolder, folder), os.path.basename(path))
    return path


class SimpleFileBrowser(wx.Panel):
    def __init__(self, parent, id=-1, labelText='File name', 
            buttonText = '...', buttonStyle = wx.BU_EXACTFIT,
            fileDialogTitle = 'Choose file', fileDialogStyle = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
            defaultDir = '.', defaultFile = '', fileWildcard='*.*', callbackFunc = None):
        self.fileDialogTitle = fileDialogTitle
        self.fileDialogStyle = fileDialogStyle
        self.defaultDir = defaultDir
        self.defaultFile = defaultFile
        self.fileWildcard = fileWildcard
        self.callbackFunc = callbackFunc
        wx.Panel.__init__(self, parent, id)
        
        self.edit  = wx.TextCtrl(self, -1)
        self.button = wx.Button(self, -1, buttonText, style=buttonStyle)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        if labelText is not None:
            self.label = wx.StaticText(self, -1, labelText)
            sizer.Add(self.label, 0, wx.RIGHT | wx.ALIGN_CENTER, 10)
        sizer.Add(self.edit, 1, wx.EXPAND)
        sizer.Add(self.button, 0, wx.LEFT, 10)
        self.SetSizer(sizer)
        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.button)
        self.edit.Bind(wx.EVT_KILL_FOCUS, self.OnText, self.edit)
        
    def AlignWith(self, sfb):
        if not isinstance(sfb, SimpleFileBrowser): raise TypeError
        self._SameSize(self.label, sfb.label)
        self._SameSize(self.button, sfb.button)
    
    def _SameSize(self, widget1, widget2):
        size1 = widget1.GetSize()
        size2 = widget1.GetSize()
        size1[0] = size2[0] = max(size1[0], size2[0])
        widget1.SetMinSize(size1)
        widget2.SetMinSize(size2)
        
    def OnButtonClick(self, evt):
        dlg = wx.FileDialog(
            self, message = self.fileDialogTitle,
            defaultDir = self.defaultDir,
            defaultFile = self.defaultFile,
            wildcard = self.fileWildcard,
            style = self.fileDialogStyle)
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
            self.edit.SetValue(path)
            self.OnText(None)
        dlg.Destroy()
        
    def OnText(self, evt):
        if self.callbackFunc is not None: 
            text = self.edit.GetValue()
            self.callbackFunc(text)
        
    def GetValue(self):
        return self.edit.GetValue()
        
    def SetValue(self, value):
        self.edit.SetValue(value)


if __name__ == "__main__":
    import unittest

    class TestRelFolder(unittest.TestCase):
        def setUp(self):
            pass
            
        def tofolder(self, f):
            return f.replace('/', os.sep)
            
        def test1(self):
            reffolder = self.tofolder('/a/b/c')
            folder = self.tofolder('/a/b/d')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, self.tofolder('../d'))

        def test2(self):
            reffolder = self.tofolder('/a/b/c')
            folder = self.tofolder('/a/b/c/d')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, self.tofolder('d'))

        def test3(self):
            reffolder = self.tofolder('c:\\a\\b\\c')
            folder = self.tofolder('d:\\a\\b\\c')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, folder)
            
        def test4(self):
            reffolder = self.tofolder('/a/b/c')
            folder = self.tofolder('/a/b/c')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, '')
            
        def test5(self):
            reffolder = self.tofolder('/a/b/c')
            folder = self.tofolder('/a/b')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, self.tofolder('../'))


    unittest.main()
