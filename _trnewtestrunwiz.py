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

import wx
import  wx.wizard as wiz
import  wx.lib.filebrowsebutton as filebrowse
from afresource import AF_WILDCARD, TR_WILDCARD, _


class NewTestrunWizard():
    def __init__(self, parent, config = None):
        self.parent = parent
        
    def ShowModal(self):
        wizard = wiz.Wizard(self.parent, -1, _("Create new test run"))
        page1 = SelectProductDatabasePage(wizard, _("Step 1/4: Select product database"))
        page2 = SelectTestsuitePage(wizard, _("Step 2/4: Select test suite"))
        page3 = EnterTestrunInfo(wizard, _("Step 3/4: Enter test description"))
        page4 = SelectOutputFilePage(wizard, _("Step 4/4: Select test run output file"))

        self.pages = (page1, page2, page3, page4)
        
        wiz.WizardPageSimple_Chain(page1, page2)
        wiz.WizardPageSimple_Chain(page2, page3)
        wiz.WizardPageSimple_Chain(page3, page4)

        wizard.GetPageAreaSizer().Add(page1)
        return wizard.RunWizard(page1)
    
    def GetValue(self):
        return [page.GetValue() for page in self.pages]
    
    def GetProductDatabase(self):
        return self.pages[0].GetValue()


class myWizardPage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        title = wx.StaticText(self, -1, title)
        font = title.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        font.SetPointSize(font.GetPointSize()+2)
        title.SetFont(font)
        sizer.Add(title, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)
        self.sizer = sizer

    def GetValue(self):
        return None
    
    def SetFocus(self):
        pass

#----------------------------------------------------------------------

class SelectFilePage(myWizardPage):
    def __init__(self, parent, title, filebrowsesettings):
        myWizardPage.__init__(self, parent, title)
        self.fbbh = filebrowse.FileBrowseButton(
            self, -1, size=(480, -1),
            buttonText = _('Browse')+' ...', **filebrowsesettings)
            
        self.sizer.Add(self.fbbh, 0, wx.ALL, 5)
        self.SetSizer(self.sizer)

    def GetValue(self):
        return self.fbbh.GetValue()
    
    def SetValue(self, value):
        self.fbbh.SetValue(value)
    
    def SetFocus(self):
        self.fbbh.SetFocus()


class SelectProductDatabasePage(SelectFilePage):
    def __init__(self, parent, title):
        SelectFilePage.__init__(self, parent, title, 
                {   "labelText"      : _("Database file")+':',
                    "toolTip"        : "",
                    "dialogTitle"    : _("Open Database"),
                    "startDirectory" : ".",
                    "initialValue"   : "",
                    "fileMask"       : AF_WILDCARD,
                    "fileMode"       : wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
                })


class SelectOutputFilePage(SelectFilePage):
    def __init__(self, parent, title):
        SelectFilePage.__init__(self, parent, title,
                {   "labelText"      : _("File") + ':',
                    "toolTip"        : "",
                    "dialogTitle"    : _("Save test run"),
                    "startDirectory" : ".",
                    "initialValue"   : "",
                    "fileMask"       : TR_WILDCARD,
                    "fileMode"       : wx.FD_SAVE
                })


class SelectTestsuitePage(myWizardPage):
    def __init__(self, parent, title):
        myWizardPage.__init__(self, parent, title)

        fgsizer = wx.FlexGridSizer(2, 2, 10, 10)

        label = wx.StaticText(self, -1, _("Test suite:"))
        self.testsuite_combobox = wx.ComboBox(self, value="", choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY)

        fgsizer.Add(label, 0, wx.ALIGN_CENTER)
        fgsizer.Add(self.testsuite_combobox, 1, wx.EXPAND | wx.ALIGN_CENTER)

        fgsizer.AddGrowableCol(1)
        fgsizer.AddGrowableRow(0)

        self.sizer.Add(fgsizer, 0, wx.ALL | wx.EXPAND, 5)

    def GetValue(self):
        """Return ID of selected test suite"""
        return self.testsuite_combobox.GetClientData(self.testsuite_combobox.GetSelection())
    
    def SetValue(self, items):
        """Populate combobox with test suite names and ID's; ID's are stored as client data"""
        self.testsuite_combobox.Clear()
        for item in items:
            self.testsuite_combobox.Append("[%d] %s" % item, item[0])
        self.testsuite_combobox.SetSelection(0)


class EnterTestrunInfo(myWizardPage):
    def __init__(self, parent, title):
        myWizardPage.__init__(self, parent, title)

        fgsizer = wx.FlexGridSizer(2, 2, 10, 10)

        label = wx.StaticText(self, -1, _("Description")+':')
        self.description_edit = wx.TextCtrl(self, -1, "", style = wx.TE_MULTILINE)
        fgsizer.Add(label, 0, wx.EXPAND | wx.ALIGN_BOTTOM )
        fgsizer.Add(self.description_edit, 1, wx.EXPAND | wx.ALIGN_TOP )

        label = wx.StaticText(self, -1, _("Tester name")+':')
        self.tester_edit = wx.TextCtrl(self, -1, "")
        fgsizer.Add(label, 0, wx.EXPAND | wx.ALIGN_CENTER )
        fgsizer.Add(self.tester_edit, 1, wx.EXPAND | wx.ALIGN_CENTER )

        fgsizer.AddGrowableCol(1)
        fgsizer.AddGrowableRow(0)

        self.sizer.Add(fgsizer, 1, wx.ALL | wx.EXPAND, 5)

    def GetValue(self):
        return (self.description_edit.GetValue(), self.tester_edit.GetValue())
    
    def SetFocus(self, which=0):
        if which == 0:
            self.description_edit.SetFocus()
        else:
            self.tester_edit.SetFocus()
