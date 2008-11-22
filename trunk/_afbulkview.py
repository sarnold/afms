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

# $Id: _affeatureview.py 108 2008-11-15 13:43:29Z achimk $

import wx
from _afartefactlist import *
import afconfig
import _afbasenotebook, _afartefactlist, _afbasenotebook
import afresource
from _afartefact import cTag


class EditBulkArtefactDialog(wx.Dialog):
    def __init__(self, parent, title, contentview, aflist):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        size = parent.GetSize()
        wx.Dialog.__init__(self, parent, -1, title, pos=parent.GetScreenPosition(), size=size, style=style)
        self.SetMinSize(parent.GetSize())

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.Layout()

        self.contentview = contentview(self, aflist)
        sizer.Add(self.contentview, 1, wx.EXPAND)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.NewId(), _('Save && Continue'))
        btnsizer.Add(btn)
        self.savecontbtn = btn
        btn = wx.Button(self, wx.ID_SAVE, _('Save && Close'))
        at = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE )])
        self.SetAcceleratorTable(at)
        self.SetAffirmativeId(wx.ID_SAVE)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        self.savebtn = btn
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        self.cancelbtn = btn
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)


class afBulkArtefactView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=-1, size=wx.DefaultSize, style= wx.BK_DEFAULT)
        leftwin =  wx.SashLayoutWindow(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER|wx.SW_3D, name='leftwin')
        leftwin.SetDefaultSize((parent.GetClientSize().width / 2, -1))
        leftwin.SetMaximumSizeX(parent.GetClientSize().width - 20)
        leftwin.SetMinimumSizeX(20)
        leftwin.SetOrientation(wx.LAYOUT_VERTICAL)
        leftwin.SetAlignment(wx.LAYOUT_LEFT)
        leftwin.SetBackgroundColour(wx.WHITE)
        leftwin.SetSashVisible(wx.SASH_RIGHT, True)
        self.leftWindow = leftwin
        self.leftWindow.SetSizer(wx.BoxSizer(wx.VERTICAL))
        # will occupy the space not used by the Layout Algorithm
        self.rightWindow = wx.Panel(self, -1, style=wx.SUNKEN_BORDER, name='rightPanel')
        self.rightWindow.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.Bind(wx.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=leftwin.GetId())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def OnSize(self, event):
        self.leftWindow.SetMaximumSizeX(self.GetParent().GetClientSize().width-20)
        self.KeepRightWindowMinSize()


    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE: return
        self.leftWindow.SetDefaultSize((event.GetDragRect().width, -1))
        self.KeepRightWindowMinSize()


    def KeepRightWindowMinSize(self):
        if self.rightWindow.GetSize()[0] < 20:
            self.leftWindow.SetDefaultSize((self.GetParent().GetClientSize()[0]-20, -1))
        wx.LayoutAlgorithm().LayoutWindow(self, self.rightWindow)
        self.rightWindow.Refresh()


    def InitTagsSelection(self, aflist):
        """Initialize list of tags.
           For each tags:
            If none af the artefacts in aflist has the current tag, the tag is unchecked in the list
            If all af the artefacts in aflist has the current tag, the tag is checked in the list
            If some af the artefacts in aflist has the current tag, the tag is tristated in the list
            or checked, when there is only one artefact in aflist.
        """
        tagcnt = [0] * len(afconfig.TAGLIST)
        for af in aflist:
            tagstr =  af.getTags()
            for tagchar in tagstr:
                tagcnt[cTag.tagchar2index(tagchar)] += 1
        if len(aflist) == 1:
            fn = self.afnotebook.tagslist.list.CheckItem
        else:
            fn = self.afnotebook.tagslist.list.TristateItem
        for i in range(len(tagcnt)):
            if tagcnt[i] == len(aflist):
                # every artefact has this tag
                self.afnotebook.tagslist.list.CheckItem(i)
            elif tagcnt[i] > 0:
                # some artefacts have this tag
                fn(i)


    def GetTagsSelection(self):
        selection = []
        for i in range(self.afnotebook.tagslist.list.GetItemCount()):
            value = self.afnotebook.tagslist.list.GetState(i)
            if value == 2:
                value = None
            selection.append(value)
        return selection


class afBulkFeatureView(afBulkArtefactView):
    #TODO: overwrite existing tags? How to clear tags?
    def __init__(self, parent, aflist):
        afBulkArtefactView.__init__(self, parent)
        self.aflistview = _afartefactlist.afFeatureList(self.leftWindow, checkstyle=True)
        self.aflistview.InitCheckableContent(aflist, [])
        self.leftWindow.GetSizer().Add(self.aflistview, 1, wx.EXPAND)

        self.afnotebook = _afbasenotebook.afBaseNotebook(self.rightWindow, viewonly=False)
        self.afnotebook.SetOwnBackgroundColour(parent.GetBackgroundColour())

        panel = wx.Panel(self.afnotebook)
        sizer = wx.FlexGridSizer(4, 2, 10, 10)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        panel.SetSizer(sizer)
        DONTCHANGE = '---'+_("don't change")+'---'
        st = wx.StaticText(panel, -1, _("Version")+':')
        choices = [DONTCHANGE,]+afconfig.VERSION_NAME
        self.version_edit = wx.ComboBox(panel, -1, choices=choices, style=wx.CB_DROPDOWN)
        self.version_edit.SetSelection(0)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.version_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        #
        st = wx.StaticText(panel, -1, _("Priority")+':')
        choices = [DONTCHANGE,] + [_(i) for i in afresource.PRIORITY_NAME]
        self.priority_edit = wx.ComboBox(panel, -1, choices = choices, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.priority_edit.SetSelection(0)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.priority_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        #
        st = wx.StaticText(panel, -1, _("Status")+':')
        choices = [DONTCHANGE,] + [_(i) for i in afresource.STATUS_NAME]
        self.status_edit = wx.ComboBox(panel, -1, choices=choices , style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.status_edit.SetSelection(0)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.status_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        #
        st = wx.StaticText(panel, -1, _("Risk")+':')
        choices = [DONTCHANGE,] + [_(i) for i in afresource.RISK_NAME]
        self.risk_edit = wx.ComboBox(panel, -1, choices=choices, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.risk_edit.SetSelection(0)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.risk_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        self.afnotebook.AddPage(panel, _('Feature'))

        self.afnotebook.AddTagsPanel()
        self.afnotebook.InitTags([])
        self.InitTagsSelection(aflist)
        self.afnotebook.AddChangelogPanel()
        self.rightWindow.GetSizer().Add(self.afnotebook, 1, wx.EXPAND|wx.ALL, 10)


    def GetContent(self):
        fields = []
        for widget in [self.version_edit, self.priority_edit, self.status_edit, self.risk_edit]:
            value = widget.GetCurrentSelection()
            if value == 0:
                fields.append(None)
            else:
                fields.append(value-1)
        if fields[0] is not None:
            # get version (key) string instead of selection
            fields[0] = self.version_edit.GetValue()
        artefactids = self.aflistview.GetItemIDByCheckState()[0]
        return (artefactids, fields, self.GetTagsSelection(), self.afnotebook.changelogpanel.GetContent())
