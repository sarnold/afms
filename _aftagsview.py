# -*- coding: utf-8  -*-

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

import copy
import wx
import afresource, afconfig, _afartefactlist
from _afartefact import cTag

class afTagListEditor(wx.Dialog):
    def __init__(self, parent, ID=-1):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        wx.Dialog.__init__(self, parent, ID, _('Select tag to edit'), pos=wx.DefaultPosition, size=wx.DefaultSize, style=style)
        self.SetMinSize(self.GetSize())
        self.taglist = _afartefactlist.afTagList(self)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_SAVE, _('Save && Close'))
        at = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE )])
        self.SetAcceleratorTable(at)
        self.SetAffirmativeId(wx.ID_SAVE)
        btn.SetDefault()
        btnsizer.AddButton(btn)        
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.taglist, 1, wx.ALL | wx.EXPAND, 10)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.ALL, 10)
    
        self.SetSizer(sizer)
        self.Layout()

 
    def OnListItemActivated(self, evt):
        dlg = cTagEdit(self)
        index = evt.GetData()
        tagobj = self.temptaglist[index]
        dlg.InitContent(tagobj)
        if (dlg.ShowModal() == wx.ID_OK):
            tagobj = dlg.GetContent()
            self.temptaglist[index] = tagobj
            self.taglist.ChangeItem(index, tagobj)
            self.taglist.list.SetItemTextColour(index, tagobj.color[tagobj['color']])
        dlg.Destroy()
        
        
    def InitContent(self, taglist):
        self.temptaglist = copy.deepcopy(taglist)
        self.taglist.InitContent(self.temptaglist)
        
        
    def GetContent(self):
        return self.temptaglist

    
class cTagEdit(wx.Dialog):
    def __init__(self, parent, ID=-1):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        wx.Dialog.__init__(self, parent, ID, _('Edit tag'), pos=wx.DefaultPosition, size=wx.DefaultSize, style=style)
        self.SetMinSize(self.GetSize())
        self.id_edit = wx.TextCtrl(self, -1, "", style = wx.TE_READONLY, name='id_edit')
        self.id_edit.Enable(False)
        self.shortdesc_edit = wx.TextCtrl(self, -1, '')
        self.longdesc_edit = wx.TextCtrl(self, -1, '')
        choices = [_(s) for s in cTag.colornames]
        self.color_combo = wx.ComboBox(self, -1, choices=choices, style=wx.CB_READONLY)
        fgs = wx.FlexGridSizer(4, 2, 10, 10)
        fgs.AddGrowableCol(1, 1)
        fgs.Add(wx.StaticText(self, -1, _('ID:')), 0, wx.ALL, 0)
        fgs.Add(self.id_edit, 0, wx.ALL|wx.EXPAND, 0)
        fgs.Add(wx.StaticText(self, -1, _('Short description:')), 0, wx.ALL, 0)
        fgs.Add(self.shortdesc_edit, 0, wx.ALL|wx.EXPAND, 0)
        fgs.Add(wx.StaticText(self, -1, _('Long description:')), 0, wx.ALL, 0)
        fgs.Add(self.longdesc_edit, 0, wx.ALL|wx.EXPAND, 0)
        fgs.Add(wx.StaticText(self, -1, _('Tag color:')), 0, wx.ALL, 0)
        fgs.Add(self.color_combo, 0, wx.ALL|wx.EXPAND, 0)
        fgs.SetFlexibleDirection(wx.BOTH)
        btnsizer = wx.StdDialogButtonSizer()
        self.okbtn = wx.Button(self, wx.ID_OK)
        self.okbtn.SetDefault()
        btnsizer.AddButton(self.okbtn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(fgs, 1, wx.ALL | wx.EXPAND, 10)
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        
        
    def InitContent(self, tagobj):
        self.id_edit.SetValue(str(tagobj['ID']))
        self.shortdesc_edit.SetValue(tagobj['shortdesc'])
        self.longdesc_edit.SetValue(tagobj['longdesc'])
        self.color_combo.SetSelection(cTag.colornames.index(tagobj['color']))


    def GetContent(self):
        ID = int(self.id_edit.GetValue())
        shortdesc=self.shortdesc_edit.GetValue()
        longdesc=self.longdesc_edit.GetValue()
        color = cTag.colornames[self.color_combo.GetSelection()]
        tagobj = cTag(ID, shortdesc, longdesc, color)
        return tagobj