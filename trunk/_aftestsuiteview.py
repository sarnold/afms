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

import  string
import wx
from _afhtmlwindow import *
from _afartefactlist import *
from _afvalidators import NotEmptyValidator
from afresource import _


class afTestsuiteView(wx.Panel):
    def __init__(self, parent, id = -1, viewonly = True):
        wx.Panel.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize)
        self.viewonly = viewonly
        title_text = wx.StaticText(self, -1, _("Title")+':')
        id_text = wx.StaticText(self, -1, _("ID")+':')
        description_text = wx.StaticText(self, -1, _("Description")+':')
        seq_text = wx.StaticText(self, -1, _("Execution order ID's")+':')
        
        if viewonly:
            self.title_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY)
            self.id_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY)
            self.description_edit = afHtmlWindow(self, -1)
            self.seq_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY)
            self.testcaselist = afTestcaseList(self, -1)
        else:
            self.title_edit = wx.TextCtrl(self, -1, "", validator = NotEmptyValidator())
            self.id_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY)
            self.description_edit = wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
            self.seq_edit = wx.TextCtrl(self, -1, "", validator = MyValidator(self))
            self.testcaselist = afTestcaseList(self, -1, checkstyle=True)
            
        self.id_edit.Enable(False)
         
        sizer = wx.FlexGridSizer(4, 2, 10, 10)
        sizer.Add(title_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.title_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(id_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.id_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(description_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.description_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(seq_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.seq_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.AddGrowableRow(2)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(sizer, 3, wx.ALL | wx.EXPAND, 5)
        hbox.Add(wx.StaticText(self, -1, _("Testcases")+':'), 0, wx.LEFT, 5)
        hbox.Add(self.testcaselist, 4, wx.ALL | wx.EXPAND, 5)
        
        self.SetSizer(hbox)
        self.Layout()
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)


    def InitContent(self, testsuitedata):
        (basedata, includedtestcases, excludedtestcases) = testsuitedata
        self.id_edit.SetValue(str(basedata[0]))
        self.title_edit.SetValue(basedata[1]);
        self.description_edit.SetValue(basedata[2]);
        self.seq_edit.SetValue(basedata[3])
        
        self.testcaselist.InitCheckableContent(excludedtestcases, includedtestcases, self.viewonly)
        
        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()

        
    def GetContent(self):
        basedata = (int(self.id_edit.GetValue()), self.title_edit.GetValue(), self.description_edit.GetValue(), self.seq_edit.GetValue())
        (includedtestcasesID, excludedtestcasesID) = self.testcaselist.GetItemIDByCheckState()
        return (basedata, includedtestcasesID, excludedtestcasesID)

        
    def OnItemActivated(self, evt):
        # Ignore activation of items in the testcase list
        pass

    
    def ChangeSelection(self, dummy):
        # dummy function for compatibility with other view classes
        pass

#----------------------------------------------------------------------

class MyValidator(wx.PyValidator):
    def __init__(self, parent, pyVar=None):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.parent = parent

    def Clone(self):
        return MyValidator(self.parent)

    def Validate(self, win):
        textCtrl = self.GetWindow()
        val = textCtrl.GetValue().replace(",", " ")

        try:
            msg = _("Syntax error in execution order")
            intarray = [int(x) for x in val.split()]
            if len(intarray) == 0:
                return True
            intarray = set(intarray)
            includedtestcasesID = set(self.parent.testcaselist.GetItemIDByCheckState()[0])
            if len(includedtestcasesID-intarray):
                msg = _("Some testcase ID's in this testsuite are not listed in execution order")
                raise
            if len(intarray-includedtestcasesID):
                msg = _("Some testcase ID's in execution order are not in this testsuite")
                raise
        except:
            wx.MessageBox(msg+'!', _("Error"), wx.ICON_ERROR )
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False

        return True


    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits or chr(key) == ',':
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

    def TransferToWindow(self):
         """ Transfer data from validator to window.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
         return True # Prevent wxDialog from complaining.


    def TransferFromWindow(self):
         """ Transfer data from window to validator.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
         return True # Prevent wxDialog from complaining.

#----------------------------------------------------------------------

