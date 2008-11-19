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


class EditBulkArtefactDialog(wx.Dialog):
    def __init__(self, parent, title, contentview):
        style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | \
                wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR
        size = parent.GetSize()
        wx.Dialog.__init__(self, parent, -1, title, pos=parent.GetScreenPosition(), size=size, style=style)
        self.SetMinSize(parent.GetSize())

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.Layout()

        self.contentview = contentview(self)
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


class afBulkFeatureView(afBulkArtefactView):
    def __init__(self, parent):
        afBulkArtefactView.__init__(self, parent)
        self.aflist = _afartefactlist.afFeatureList(self.leftWindow)
        self.leftWindow.GetSizer().Add(self.aflist, 1, wx.EXPAND)
        
        self.afnotebook = _afbasenotebook.afBaseNotebook(self.rightWindow)
        panel = wx.Panel(self.afnotebook)
        sizer = wx.FlexGridSizer(4, 2, 10, 10)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        panel.SetSizer(sizer)
        st = wx.StaticText(panel, -1, _("Version")+':')
        self.version_edit = wx.ComboBox(panel, -1, choices = afconfig.VERSION_NAME, style=wx.CB_DROPDOWN)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.version_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        st = wx.StaticText(panel, -1, _("Priority")+':')
        self.priority_edit = wx.ComboBox(panel, -1, choices = [_(i) for i in afresource.PRIORITY_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.priority_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)  
        st = wx.StaticText(panel, -1, _("Status")+':')    
        self.status_edit = wx.ComboBox(panel, -1, choices = [_(i) for i in afresource.STATUS_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.status_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        st = wx.StaticText(panel, -1, _("Risk")+':')
        self.risk_edit = wx.ComboBox(panel, -1, choices = [_(i) for i in afresource.RISK_NAME], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        sizer.Add(st, 0, wx.LEFT|wx.TOP, 10)
        sizer.Add(self.risk_edit, 1, wx.EXPAND|wx.RIGHT|wx.TOP, 10)
        self.afnotebook.AddPage(panel, _('Feature'))
        
        
        self.afnotebook.AddTagsPanel()
        self.rightWindow.GetSizer().Add(self.afnotebook, 1, wx.EXPAND|wx.ALL, 10)
        
        
        
