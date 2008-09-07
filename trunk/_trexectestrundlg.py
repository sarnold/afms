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

import subprocess, os.path, sys, traceback
import wx
import wx.lib.hyperlink as hl
from _trtestresultview import *
from _trtestcaseview import *

class ExecTestrunDialog(wx.Dialog):
    def __init__(self, parent, ID, title):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        size = parent.GetSize()
        wx.Dialog.__init__(self, parent, ID, title, pos=parent.GetScreenPosition(), size=size, style=style)
        # need this to enable validation in all subwindows
        self.SetExtraStyle(wx.WS_EX_VALIDATE_RECURSIVELY)
        self.SetMinSize(size)

        self.leftPanel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        self.rightPanel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.leftPanel, 1, wx.ALL | wx.EXPAND, 0)
        hbox.Add(self.rightPanel, 1, wx.ALL | wx.EXPAND, 0)

        self.testresultview = trTestresultPanel(self.rightPanel, viewonly = False)
        self.testcaseview = trTestcasePanel(self.leftPanel, viewonly=False)
        self.Bind(hl.EVT_HYPERLINK_LEFT, self.OnRunScript)

        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_SAVE)
        at = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE )])
        self.SetAcceleratorTable(at)
        self.SetAffirmativeId(wx.ID_SAVE)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hbox, 1, wx.ALL | wx.EXPAND, 6)
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()


    def OnRunScript(self, evt):
        scripturl = os.path.join(os.getcwd(), self.testcaseview.scripturl_edit.GetValue())
        cwd = os.path.dirname(scripturl)
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        try:
            process = subprocess.Popen(scripturl, cwd=cwd, stdout=stdout, stderr=stderr)
            returncode = process.wait()
            message = _('Script returns code %d\nScript stdout:\n%s\nScript stderr:\n%s' %
                (returncode, ''.join(process.stdout.readlines()), ''.join(process.stderr.readlines())))
            self.testresultview.remark_edit.SetValue(message)
            if returncode != 0:
                self.testresultview.result_edit.SetSelection(0)
            else:
                self.testresultview.result_edit.SetSelection(1)
        except OSError:
            message = traceback.format_exc()
            message += '\nscripturl=%s\ncwd=%s' % (scripturl, cwd)
            self.testresultview.remark_edit.SetValue(message)
            self.testresultview.result_edit.SetSelection(0)


