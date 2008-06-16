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
from _afartefactlist import *
import afresource


class ImportArtefactDialog(wx.Dialog):
    def __init__(self, parent, ID):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        size = parent.GetSize()
        wx.Dialog.__init__(self, parent, ID, _('Import artefacts'), pos=wx.DefaultPosition, size=size, style=style)
        # need this to enable validation in all subwindows
        self.SetMinSize(size)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.select_related_checkbox = wx.CheckBox(self, -1, _('Select related artefacts automatically'))
        self.select_related_checkbox.SetValue(True)
        sizer.Add(self.select_related_checkbox, 0, wx.EXPAND | wx.ALL, 5)

        self.notebook = ArtefactNotebook(self)
        sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)


    def OnListItemActivated(self, evt):
        pass


    def InitContent(self, *args):
        """args should be
        - feature list
        - requirements list
        - use case list
        - test case list
        - test suite list
        """
        self.notebook.InitContent(*args)


    def GetAutoSelectRelated(self):
        return self.select_related_checkbox.GetValue()


    def CheckArtefacts(self, artefact_kind, idlist):
        artefact_kinds = [item['id'] for item in afresource.ARTEFACTS]
        index = artefact_kinds.index(artefact_kind)
        listobj = self.notebook.artefactlist[index]
        listobj.CheckItems(idlist)


    def GetCheckedArtefacts(self):
        """Return list with list of checked features, requirements,
        use cases, test cases and testsuites."""
        idlist = []
        for listobj in self.notebook.artefactlist:
            idlist.append(listobj.GetItemIDByCheckState()[0])
        return idlist


class ArtefactNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)

        self.artefactlist = [obj(self, checkstyle = True) for obj in [afFeatureList, afRequirementList, afUsecaseList, afTestcaseList, afTestsuiteList, afSimpleSectionList, afGlossaryEntryList]]
        for i in range(len(afresource.ARTEFACTS)):
            self.AddPage(self.artefactlist[i], _(afresource.ARTEFACTS[i]['name']))


    def InitContent(self, *args):
        """args should be
        - feature list
        - requirements list
        - use case list
        - test case list
        - test suite list
        """
        for i in range(len(self.artefactlist)):
            self.artefactlist[i].InitCheckableContent(args[i], [])


