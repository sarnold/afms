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
import trconfig
import afresource
from afresource import _


class trTestresultPanel():
    def __init__(self, parent, viewonly = True):
        self.viewonly = viewonly
        labels = [_("Result"), _("Time"), _("Action"), _("Remark")]
        statictext = []
        for label in labels:
            st = wx.StaticText(parent, -1, label + ':')
            statictext.append(st)

        if viewonly:
            self.result_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_READONLY)
            self.timestamp_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_READONLY)
            self.action_edit = afHtmlWindow(parent, -1)
            self.remark_edit = afHtmlWindow(parent, -1)
        else:
            self.result_edit = wx.ComboBox(parent, value="", choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.timestamp_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_READONLY)
            self.action_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_MULTILINE,
                validator = TestresultValidator(self.result_edit.GetSelection, afresource.FAILED, _("Test failed.\nEnter action!")))
            self.remark_edit = wx.TextCtrl(parent, -1, "", style = wx.TE_MULTILINE,
                validator = TestresultValidator(self.result_edit.GetSelection, afresource.SKIPPED, _("Test skipped.\nEnter remark!")))
            self.timer = wx.Timer(parent)
            self.timer.Start(1000)
            parent.Bind(wx.EVT_TIMER, self.OnTimer)

        edit = [self.result_edit, self.timestamp_edit, self.action_edit, self.remark_edit]

        sizer = wx.FlexGridSizer(4, 2, 10, 10)

        for i in range(len(labels)):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_CENTER)
            sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)

        sizer.AddGrowableRow(2, 1)
        sizer.AddGrowableRow(3, 1)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)

        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)
        parent.SetSizer(hbox)

        parent.Layout()


    def InitContent(self, data):
        """
        data is a tuple:
        (result, remark, action, timestamp)
        """
        if self.viewonly:
            self.result_edit.SetValue(afresource.TEST_STATUS_NAME[data[0]])
        else:
            self.result_edit.Clear()
            for item in afresource.TEST_STATUS_NAME[:-1]:
                self.result_edit.Append(item)
            self.result_edit.SetSelection(0)

        self.action_edit.SetValue(str(data[2]))
        self.remark_edit.SetValue(data[1])
        self.timestamp_edit.SetValue(data[3])


    def GetData(self):
        """Get values from widgets
           Return tuple (result, remark, action, timestamp)
        """
        return (self.result_edit.GetSelection(), self.remark_edit.GetValue(),
                self.action_edit.GetValue(), self.timestamp_edit.GetValue())
    
    
    def OnTimer(self, evt):
        self.timestamp_edit.SetValue(time.strftime(afresource.TIME_FORMAT))

#----------------------------------------------------------------------

class TestresultValidator(wx.PyValidator):
     """ This validator is used to ensure that the user has entered
         a action in case the test has failed or taht a remark has been entered
         when test is skipped
     """
     def __init__(self, testresult_functor, trigger, msg):
         """ Standard constructor.
         """
         wx.PyValidator.__init__(self)
         self.getTestResult = testresult_functor
         self.trigger = trigger
         self.msg = msg


     def Clone(self):
         """ Standard cloner. """
         return TestresultValidator(self.getTestResult, self.trigger, self.msg)


     def Validate(self, win):
         """ Validate the contents of the given text control. """
         textCtrl = self.GetWindow()
         text = textCtrl.GetValue()

         if len(text) == 0 and self.getTestResult() == self.trigger:
             textCtrl.SetBackgroundColour("pink")
             textCtrl.Refresh()
             wx.MessageBox(self.msg, _("Error"), wx.ICON_ERROR)
             textCtrl.SetFocus()
             return False
         else:
             textCtrl.SetBackgroundColour(
                 wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
             textCtrl.Refresh()
             return True


     def TransferToWindow(self):
         """ Transfer data from validator to window."""
         return True # Prevent wxDialog from complaining.


     def TransferFromWindow(self):
         """ Transfer data from window to validator."""
         return True # Prevent wxDialog from complaining.

#----------------------------------------------------------------------
