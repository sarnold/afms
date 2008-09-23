# -*- coding: utf-8  -*-

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
from afresource import CSS_WILDCARD, XSL_WILDCARD
import afresource
from _afhelper import SimpleFileBrowser


class SettingsDialog(wx.Dialog):
    def __init__(self, parent, id=-1):
        wx.Dialog.__init__(self, parent, id, title=_('Settings'), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        self.SetMinSize((800, -1))
        gap = 5
        filebrowsesettings = {'labelText' : None, 'buttonText' : '...', 
                              'fileDialogTitle' : _("Open Stylesheet"), 'fileDialogStyle' : wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                              'defaultFile' : ''}

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        box = wx.StaticBox(self, -1, _("Language Settings (taking effect after restart)"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.Add(wx.StaticText(self, -1, _("User Interface Language")+':'), 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP, gap)
        self.language = wx.ComboBox(self, choices = [_('English'), _('German')], style=wx.CB_READONLY )
        self.language.SetSelection(0)
        bsizer.Add(self.language, 1, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, gap)
        sizer.Add(bsizer, 0, wx.EXPAND|wx.ALL, gap)
        
        box = wx.StaticBox(self, -1, _("HTML Report Settings"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.Add(wx.StaticText(self, -1, _("CSS Stylesheet")+':'), 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.RIGHT, gap)
        filebrowsesettings['fileWildcard'] = CSS_WILDCARD
        self.cssfile = SimpleFileBrowser(self, **filebrowsesettings )
        bsizer.Add(self.cssfile, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, gap)
        self.openhtmlreport = wx.CheckBox(self, -1, _('View after creation'))
        bsizer.Add(self.openhtmlreport, 0, wx.EXPAND|wx.ALL, gap)
        sizer.Add(bsizer, 0, wx.EXPAND|wx.ALL, gap)        
        
        box = wx.StaticBox(self, -1, _("XML Report Settings"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.Add(wx.StaticText(self, -1, _("XSL Stylesheet")+':'), 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.RIGHT, gap)
        filebrowsesettings['fileWildcard'] = XSL_WILDCARD
        self.xslfile = SimpleFileBrowser(self, **filebrowsesettings)
        bsizer.Add(self.xslfile, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, gap)
        self.openxmlreport = wx.CheckBox(self, -1, _('View after creation'))
        bsizer.Add(self.openxmlreport, 0, wx.EXPAND|wx.ALL, gap)
        sizer.Add(bsizer, 0, wx.EXPAND|wx.ALL, gap)
        
        sizer.AddStretchSpacer(1)
        
        btnsizer = wx.StdDialogButtonSizer()
        self.okbtn = wx.Button(self, wx.ID_OK)
        self.okbtn.SetDefault()
        btnsizer.AddButton(self.okbtn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.ALL, 5)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())
        
        
    def SetValue(self, language, cssfile, openhtml, xslfile, openxml):
        self.language.SetSelection(language)
        self.cssfile.SetValue(cssfile)
        self.xslfile.SetValue(xslfile)
        self.openhtmlreport.SetValue(openhtml)
        self.openxmlreport.SetValue(openxml)
        
    def GetValue(self):
        return (self.language.GetSelection(), self.cssfile.GetValue(), self.openhtmlreport.GetValue(),
                self.xslfile.GetValue(), self.openxmlreport.GetValue())


def EditSettings(parent):
    config = wx.Config.Get()
    try:
        language = ['en', 'de'].index(config.Read("language", 'en'))
    except IndexError:
        language = 0
    cssfile = config.Read('cssfile', '')
    openhtmlreport = config.ReadBool('autoopenhtmlreport', False)
    xslfile = config.Read('xslfile', '')
    openxmlreport = config.ReadBool('autoopenxmlreport', False)
    dlg = SettingsDialog(parent)
    dlg.SetValue(language, cssfile, openhtmlreport, xslfile, openxmlreport)
    if dlg.ShowModal() == wx.ID_OK:
        (language, cssfile, openhtmlreport, xslfile, openxmlreport) = dlg.GetValue()
        afresource.SetLanguage(['en', 'de'][language])
        config.Write('cssfile', cssfile)
        config.Write('xslfile', xslfile)
        config.WriteBool('autoopenhtmlreport', openhtmlreport)
        config.WriteBool('autoopenxmlreport', openxmlreport)
    dlg.Destroy()
