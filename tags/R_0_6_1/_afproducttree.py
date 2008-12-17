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
import afconfig
import _afimages
import afresource, _afhelper

class afProductTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize)
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.emptytrashidx = il.Add(_afimages.getTrashEmptyBitmap())
        self.fulltrashidx = il.Add(_afimages.getTrashFullBitmap())
        self.SetImageList(il)
        self.il = il

        self.root = self.AddRoot(_("Product"))
        self.SetPyData(self.root, {'ID':"PRODUCT", 'colorindex':None})
        self.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)

        self.treeChild = {}
        for i in afresource.ARTEFACTSTREEVIEWORDER:
            item = afresource.ARTEFACTS[i]
            child = self.AppendItem(self.root, _(item["name"]))
            self.SetPyData(child, {'ID':item["id"], 'colorindex':None})
            self.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            self.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
            self.treeChild[item["id"]] = child

        # --- artefact trash ---
        trash = self.AppendItem(self.root, _(afresource.TRASH["name"]))
        self.SetPyData(trash, {'ID':afresource.TRASH["id"], 'colorindex':None})
        self.SetItemImage(trash, self.emptytrashidx, wx.TreeItemIcon_Normal)
        self.SetItemImage(trash, self.emptytrashidx, wx.TreeItemIcon_Expanded)
        self.treeChild[afresource.TRASH["id"]] = trash
        self.trashChild = {}
        for i in afresource.ARTEFACTSTREEVIEWORDER:
            item = afresource.ARTEFACTS[i]
            child = self.AppendItem(trash, _(item["name"]))
            self.SetPyData(child, {'ID':afresource.TRASH["id"]+item["id"], 'colorindex':None})
            self.SetItemImage(child, self.emptytrashidx, wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.emptytrashidx, wx.TreeItemIcon_Expanded)
            self.trashChild[item["id"]] = child

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)

        self.currentitem = None

    def UpdateTrashIcons(self, number_of_deleted_artefacts):
        total = 0
        for af in afresource.ARTEFACTS:
            nbr = number_of_deleted_artefacts[af['id']]
            total += nbr
            if nbr != 0:
                idx = self.fulltrashidx
            else:
                idx = self.emptytrashidx
            self.SetItemImage(self.trashChild[af['id']], idx, wx.TreeItemIcon_Normal)

        if total != 0:
            idx = self.fulltrashidx
        else:
            idx = self.emptytrashidx

        self.SetItemImage(self.treeChild[afresource.TRASH["id"]], idx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.treeChild[afresource.TRASH["id"]], idx, wx.TreeItemIcon_Expanded)


    def InitTreeCtrl(self, artefactnames, number_of_deleted_artefacts):
        self.Enable()
        self.Expand(self.root)
        for af in afresource.ARTEFACTS:
            self.DeleteChildren(self.treeChild[af["id"]])
            for item in artefactnames[af['id']]:
                self.AddChildItem(af['id'], item)
        self.UpdateTrashIcons(number_of_deleted_artefacts)
        self.SelectItem(self.root)


    def __getProperties(self, item):
        ID = item['ID']
        title = item['title']
        (color, colorindex) = _afhelper.getColorForArtefact(item)
        return (ID, title, color, colorindex)


    def AddChildItem(self, parent, item):
        (ID, title, color, colorindex) = self.__getProperties(item)
        item_text = self.FormatChildLabel(ID, title)
        child = self.AppendItem(self.treeChild[parent], item_text, 2, -1)
        self.SetItemTextColour(child, color)
        self.SetPyData(child, {'ID':ID, 'colorindex':colorindex})


    def FormatChildLabel(self, ID, text):
        return "(" + str(ID) + ") " + text


    def GetItemInfo(self, item):
        item_id = self.GetPyData(item)['ID']
        parent = self.GetItemParent(item)
        if parent:
            parent_id = self.GetPyData(parent)['ID']
        else:
            parent_id = None
        return (parent_id, item_id)


    def _FindParentItemId(self, parent_id):
        rootItemId = self.GetRootItem()
        (treeItemId, cookie) = self.GetFirstChild(rootItemId)
        for i in range(0, self.GetChildrenCount(rootItemId, False)):
            if self.GetPyData(treeItemId)['ID'] == parent_id:
                break;
            treeItemId = self.GetNextSibling(treeItemId)
        return treeItemId


    def _FindChildItemId(self, treeItemId, item_id):
        (childItemId, cookie) = self.GetFirstChild(treeItemId)
        for i in range(0, self.GetChildrenCount(treeItemId, False)+1):
            if self.GetPyData(childItemId)['ID'] == item_id:
                break;
            childItemId = self.GetNextSibling(childItemId)
        return (childItemId)


    def FindItem(self, parent_id, item_id):
        treeParentId = self._FindParentItemId(parent_id)
        if item_id is not None:
            treeChildId = self._FindChildItemId(treeParentId, item_id)
        else:
            treeChildId = None
        return (treeParentId, treeChildId)


    def UpdateItemText(self, parent_id, item_id, item):
        (ID, title, color, colorindex) = self.__getProperties(item)
        (treeParentId, treeChildId) = self.FindItem(parent_id, item_id)
        self.SetItemText(treeChildId, self.FormatChildLabel(item_id, title))
        self.SetItemTextColour(treeChildId, color)
        pydata = self.GetPyData(treeChildId)
        pydata['colorindex'] = colorindex


    def UpdateItemColors(self):
        for af in afresource.ARTEFACTS:
            treeParentId = self._FindParentItemId(af['id'])
            (treeChildId, cookie) = self.GetFirstChild(treeParentId)
            for i in range(0, self.GetChildrenCount(treeParentId, False)):
                ci = self.GetPyData(treeChildId)['colorindex']
                if ci is not None:
                    colorname = afconfig.TAGLIST[ci]['color']
                    color = wx.Color(*afconfig.TAGLIST[0].color[colorname])
                    self.SetItemTextColour(treeChildId, color)
                    ID = self.GetPyData(treeChildId)['ID']
                    self.SetPyData(treeChildId, {'ID':ID, 'colorindex':ci})
                treeChildId = self.GetNextSibling(treeChildId)


    def SetSelection(self, parent_id, item_id = None):
        (treeParentId, treeChildId) = self.FindItem(parent_id, item_id)
        treeItemId = treeParentId
        if item_id is not None:
            treeItemId = treeChildId
        self.SelectItem(treeItemId, True)


    def GetCurrentItem(self):
        return self.currentitem


    def OnSelChanged(self, evt):
        "Propagate event"
        self.currentitem = evt.GetItem()
        evt.SetId(300)
        evt.Skip()


    def OnItemActivated(self, evt):
        "Propagate event"
        evt.SetId(301)
        evt.Skip()


    def GetSelectedItem(self):
        treeItemId = self.GetSelection()
        return self.GetItemInfo(treeItemId)
