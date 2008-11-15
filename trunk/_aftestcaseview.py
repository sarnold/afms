# -*- coding: utf-8 -*-

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
from _afartefactlist import *
from _afvalidators import NotEmptyValidator
import _afbasenotebook
import afconfig
from _afartefact import cTestcase
from _afhelper import SimpleFileBrowser, getRelFolder, getRelPath

def _relpath(path):
    getRelFolder(path)

class afTestcaseNotebook(_afbasenotebook.afBaseNotebook):
    def __init__(self, parent, id = -1, viewonly = True):
        _afbasenotebook.afBaseNotebook.__init__(self, parent, id, viewonly)
        color = parent.GetBackgroundColour()
        self.SetOwnBackgroundColour(color)
        panel = wx.Panel(self, -1)
        panel.SetOwnBackgroundColour(color)
        labels = [_('Title'), _('ID'), _('Version'), _('Purpose'), _('Prerequisite'), _('Testdata'), _('Steps'), _('Script'), _('Notes && Questions')]
        statictext = []
        for label in labels:
            st = wx.StaticText(panel, -1, label+':')
            statictext.append(st)

        if viewonly:
            self.title_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.id_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.version_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.scripturl_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.purpose_edit = afHtmlWindow(panel, -1, name='purpose')
            self.prerequisite_edit = afHtmlWindow(panel, -1, name='prerequisite')
            self.testdata_edit =afHtmlWindow(panel, -1, name='testdata')
            self.steps_edit = afHtmlWindow(panel, -1, name='steps')
            self.notes_edit = afHtmlWindow(panel, -1, name='notes')
        else:
            self.title_edit = wx.TextCtrl(panel, -1, "", validator = NotEmptyValidator())
            self.id_edit = wx.TextCtrl(panel, -1, "", style = wx.TE_READONLY)
            self.version_edit = wx.ComboBox(panel, -1, choices = afconfig.VERSION_NAME, style=wx.CB_DROPDOWN)
            self.scripturl_edit = SimpleFileBrowser(panel, labelText=None, fileWildcard=_(afresource.ALL_WILDCARD),
                                                    fileDialogTitle=_("Choose script"), callbackFunc=self.__setRelPath)
            self.purpose_edit = afTextCtrl(panel)
            self.prerequisite_edit = afTextCtrl(panel)
            self.testdata_edit = afTextCtrl(panel)
            self.steps_edit = afTextCtrl(panel)
            self.notes_edit = afTextCtrl(panel)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.purpose_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.prerequisite_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.testdata_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.steps_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.notes_edit)

        self.id_edit.Enable(False)

        edit = [self.title_edit, self.id_edit, self.version_edit, self.purpose_edit,
            self.prerequisite_edit, self.testdata_edit, self.steps_edit, self.scripturl_edit, self.notes_edit]

        sizer = wx.FlexGridSizer(8, 2, 10, 10)
        sizer.Add(statictext[0], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(edit[0], 0, wx.EXPAND | wx.ALIGN_LEFT)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.id_edit, 0)
        hsizer.Add(statictext[2], 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        hsizer.Add(self.version_edit, 1, wx.LEFT | wx.EXPAND, 5)
        sizer.Add(statictext[1], 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(hsizer, 0, wx.EXPAND | wx.ALIGN_LEFT)

        for i in range(3, len(labels)):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
            sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)

        sizer.AddGrowableRow(2, 1)
        sizer.AddGrowableRow(3, 2)
        sizer.AddGrowableRow(4, 2)
        sizer.AddGrowableRow(5, 3)
        sizer.AddGrowableRow(7, 1)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.BOTH)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)
        panel.SetSizer(hbox)

        panel.Layout()
        self.AddPage(panel, _("Testcase"))

        # Related requirements panel; this relation could not be edited from here
        self.requirementlist = self.AddRelatedArtefactPanel(afRequirementList, _("Related Requirements"))

        # Related testsuites panel; this relation could not be edited from here
        self.testsuitelist = self.AddRelatedArtefactPanel(afTestsuiteList, _("Related Testsuites"))
        self.AddTagsPanel()
        self.AddChangelogPanel()


    def InitContent(self, testcase):
        self.id_edit.SetValue(str(testcase['ID']))
        self.title_edit.SetValue(testcase['title'])
        self.purpose_edit.SetValue(testcase['purpose'])
        self.prerequisite_edit.SetValue(testcase['prerequisite'])
        self.testdata_edit.SetValue(testcase['testdata'])
        self.steps_edit.SetValue(testcase['steps'])
        self.notes_edit.SetValue(testcase['notes'])
        self.version_edit.SetValue(testcase['version'])
        self.scripturl_edit.SetValue(testcase['scripturl'])

        self.requirementlist.InitContent(testcase.getRelatedRequirements())
        self.testsuitelist.InitContent(testcase.getRelatedTestsuites())
        self.InitTags(testcase.getTags())
        if self.viewonly:
            self.changelist.InitContent(testcase.getChangelist())

        self.Show()
        self.GetParent().Layout()
        self.title_edit.SetFocus()


    def GetContent(self):
        testcase = cTestcase(ID=int(self.id_edit.GetValue()),
                             title=self.title_edit.GetValue(),
                             purpose=self.purpose_edit.GetValue(),
                             prerequisite=self.prerequisite_edit.GetValue(),
                             testdata=self.testdata_edit.GetValue(),
                             steps=self.steps_edit.GetValue(),
                             notes=self.notes_edit.GetValue(),
                             version=self.version_edit.GetValue(),
                             scripturl = self.scripturl_edit.GetValue())
        testcase.setChangelog(self.GetChangelogContent())
        testcase.setTags(self.GetTags())
        return testcase


    def __setRelPath(self, path):
        self.scripturl_edit.SetValue(getRelPath(path))
