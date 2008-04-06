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


def ExceptionMessageBox(exceptiondata, title="Exception"):
    """exceptiondata is tuple (exc_type, exc_value, exc_traceback) as returned from
    sys.exc_info()
    """
    wx.MessageBox("Type: %s\nValue: %s" % exceptiondata[0:2], title, wx.OK|wx.ICON_ERROR)


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
