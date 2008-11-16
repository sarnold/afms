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

import  string
import wx
from _afhtmlwindow import *
from _aftextctrl import *
from _afartefactlist import *
from _afvalidators import NotEmptyValidator
from _afartefact import cTestsuite, cTestcase
import _afbasenotebook

class afTestsuiteNotebook(_afbasenotebook.afBaseNotebook):
    def __init__(self, parent, id = -1, viewonly = True):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style= wx.BK_DEFAULT)
        self.viewonly = viewonly
        color = parent.GetBackgroundColour()
        self.SetOwnBackgroundColour(color)
        panel = wx.Panel(self, -1)
        title_text = wx.StaticText(panel, -1, _("Title")+':')
        id_text = wx.StaticText(panel, -1, _("ID")+':')
        description_text = wx.StaticText(panel, -1, _("Description")+':')


        if viewonly:
            self.title_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.id_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.description_edit = afHtmlWindow(panel, -1)
        else:
            self.title_edit = wx.TextCtrl(panel, -1, "", validator = NotEmptyValidator())
            self.id_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.description_edit = afTextCtrl(panel)

        self.id_edit.Enable(False)

        sizer = wx.FlexGridSizer(4, 2, 10, 10)
        sizer.Add(title_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.title_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(id_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.id_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.Add(description_text, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        sizer.Add(self.description_edit, 0, wx.EXPAND | wx.ALIGN_TOP )
        sizer.AddGrowableRow(2)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(sizer, 3, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(hbox)
        panel.Layout()
        self.AddPage(panel, _('Testsuite'))

        #-----------------------------------------------------------------
        # Related testcases panel
        panel = wx.Panel(self, -1)
        seq_text = wx.StaticText(panel, -1, _("Execution order ID's")+':')
        if self.viewonly:
            self.seq_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
        else:
            self.seq_edit = wx.TextCtrl(panel, -1, "", validator = MyValidator(panel))
        self.testcaselist = afTestcaseList(panel, -1, checkstyle=not self.viewonly)
        sizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(seq_text, 0, wx.EXPAND | wx.RIGHT | wx.ALIGN_BOTTOM , 5 )
        hbox.Add(self.seq_edit, 1, wx.EXPAND)
        sizer.Add(hbox, 0, wx.ALL | wx.EXPAND, 6)
        sizer.Add(self.testcaselist, 1, wx.ALL| wx.EXPAND, 6)
        panel.SetSizer(sizer)
        self.AddPage(panel, _("Attached Testcases"))
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

        self.AddTagsPanel()


    def InitContent(self, testsuite):
        self.id_edit.SetValue(str(testsuite['ID']))
        self.title_edit.SetValue(testsuite['title']);
        self.description_edit.SetValue(testsuite['description']);
        self.seq_edit.SetValue(testsuite['execorder'])

        self.testcaselist.InitCheckableContent(testsuite.getUnrelatedTestcases(), testsuite.getRelatedTestcases(), self.viewonly)
        self.InitTags(testsuite.getTags())
        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()


    def GetContent(self):
        testsuite = cTestsuite(ID=int(self.id_edit.GetValue()), title=self.title_edit.GetValue(),
                               description=self.description_edit.GetValue(), execorder=self.seq_edit.GetValue())

        (related_testcases, unrelated_testcases) = self.testcaselist.GetItemIDByCheckState()

        related_tcobjs = []
        for tc_id in related_testcases:
            tcobj = cTestcase(ID=tc_id)
            related_tcobjs.append(tcobj)
        testsuite.setRelatedTestcases(related_tcobjs)

        unrelated_tcobjs = []
        for tc_id in unrelated_testcases:
            tcobj = cTestcase(ID=tc_id)
            unrelated_tcobjs.append(tcobj)
        testsuite.setUnrelatedTestcases(unrelated_tcobjs)
        testsuite.setTags(self.GetTags())
        return testsuite


    def UpdateContent(self, artefact):
        self.id_edit.SetValue(str(artefact['ID']))


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

