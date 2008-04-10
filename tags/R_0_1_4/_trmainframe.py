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

import os, sys;
import wx;
from wx.lib.wordwrap import wordwrap
import  wx.lib.mixins.listctrl  as  listmix
import _afimages
import trconfig, trinfo
from _trtestcaseview import *
from _trtestresultview import *
import afresource

class MainFrame(wx.Frame):
    """
    This is the main frame. All the view related things are done here.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        self.config = wx.Config.Get()
        self.SetSize((self.config.ReadInt("window_size_x", 800), self.config.ReadInt("window_size_y", 600)))
        self.SetPosition((self.config.ReadInt("window_pos_x", -1), self.config.ReadInt("window_pos_y", -1)))
        self.SetMinSize((800,600))

        self.SetupStatusBar()
        self.SetupToolbar()
        self.SetupMenu()
        self.SetupSashLayout(self.config)

        toppanel = wx.Panel(self.leftWindow, style = wx.BORDER_SUNKEN)
        toppanel.SetAutoLayout(True)
        self.testcaselist = TestcaseListCtrlPanel(toppanel)
        hbox = wx.BoxSizer(wx.VERTICAL)
        sbox = wx.StaticBox(toppanel, -1, _("Test run status"))
        bsizer = wx.StaticBoxSizer(sbox, wx.VERTICAL)
        self.statustext = []
        for i in range(4):
            t = wx.StaticText(toppanel, -1, "")
            self.statustext.append(t)
            bsizer.Add(t, 0, wx.TOP|wx.LEFT, 5)
        self.SetStatusInfo((0,0,0,0), "")
        hbox.Add(bsizer, 0, wx.EXPAND|wx.ALL, 5)
        hbox.Add(self.testcaselist, 1, wx.EXPAND)
        toppanel.SetSizer(hbox)

        self.testcaseview = trTestcasePanel(self.leftPanel)
        self.testresultview = trTestresultPanel(self.rightPanel)

        icons = wx.IconBundle()
        icons.AddIcon(wx.IconFromBitmap(_afimages.getapp16x16Bitmap()))
        icons.AddIcon(wx.IconFromBitmap(_afimages.getapp32x32Bitmap()))
        self.SetIcons(icons)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def SetStatusInfo(self, status, path = None):
        """status is tuple (total, pending, failed, skipped)"""
        label = (_("%3d test cases total"), _("%3d pending"), _("%3d failed"), _("%3d skipped"))
        for i in range(4):
            self.statustext[i].SetLabel(label[i] % status[i])
        if path is not None:
            self.SetStatusText(path, 2)


    def SetupStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        # Sets the three fields to be relative widths to each other.
        self.statusbar.SetStatusWidths([-2, -1, -2])


    def SetupToolbar(self):
        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT )
        tsize = (24,24)

        new_bmp = _afimages.getProdNewBitmap()
        open_bmp = _afimages.getProdOpenBitmap()
        run_bmp = _afimages.getTRRunBitmap()


        tb.SetToolBitmapSize(tsize)
        tb.AddLabelTool(10, _("New"), new_bmp, shortHelp=_("New test run"), longHelp=_("Create a new test run"))
        tb.AddLabelTool(11, _("Open"), open_bmp, shortHelp=_("Open test run"), longHelp=_("Open an existing test run"))
        tb.AddLabelTool(12, _("Run"), run_bmp, shortHelp=_("Run test case"), longHelp=_("Run a test case"))

        tb.EnableTool(12, False)
        tb.Realize()


    def SetupMenu(self):
        "Create menubar"
        # TODO: need Help/About Test Run menu item, toolbar and dialog
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(101, _("&New test run ...\tCtrl-N"), _("Create a new test run"))
        menu.Append(102, _("&Open test run ...\tCtrl-O"), _("Open an existing test run"))
        menu.Append(103, _("Export as HTML ..."), _("Export test run to HTML file"))
        menu.Append(104, _("Export as XML ..."), _("Export test run to XML files"))
        menu.Enable(103, False)
        menu.Enable(104, False)
        menu.Append(wx.ID_EXIT, _("E&xit\tAlt-X"), _("Exit this application"))
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        menuBar.Append(menu, _("&File"))

        menu = wx.Menu()
        menu.Append(201, _("Run ...\tCtrl-R"), _("Run test case"))
        menu.Enable(201, False)
        menu.Append(202, _("About current test run..."), _("Info about the current test run"))
        menu.Enable(202, False)
        menu.Append(203, _("Cancel current test run..."), _("Cancel the current test run"))
        menu.Enable(203, False)
        menuBar.Append(menu, _("&Test"))

        menu = wx.Menu()
        menu.Append(301, _('Language ...'), _('Set language'))
        self.Bind(wx.EVT_MENU, self.OnChangeLanguage, id = 301)
        menu.Enable(301, True)
        menuBar.Append(menu, _('&Settings'))

        menu = wx.Menu()
        menu.Append(901, _("About ..."), _("Info about this program"))
        self.Bind(wx.EVT_MENU, self.OnAbout, id = 901)
        menu.Enable(901, True)
        menuBar.Append(menu, _("&Help"))

        self.SetMenuBar(menuBar)


    def SetupSashLayout(self, config):
        width = self.GetSize().width / 4
        leftwin = wx.SashLayoutWindow(self, -1, wx.DefaultPosition, (200, 30), wx.SW_3D)
        leftwin.SetDefaultSize((width, 1000))
        leftwin.SetMaximumSizeX(width)
        leftwin.SetMinimumSizeX(150)
        leftwin.SetOrientation(wx.LAYOUT_VERTICAL)
        leftwin.SetAlignment(wx.LAYOUT_LEFT)
        leftwin.SetSashVisible(wx.SASH_RIGHT, True)

        self.rightWindow = wx.Panel(self, -1, style=wx.BORDER_NONE)
        self.leftWindow = leftwin

        self.leftPanel = wx.Panel(self.rightWindow, -1, style=wx.BORDER_SUNKEN)
        self.rightPanel = wx.Panel(self.rightWindow, -1, style=wx.BORDER_SUNKEN)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.leftPanel, 1, wx.ALL | wx.EXPAND, 0)
        hbox.Add(self.rightPanel, 1, wx.ALL | wx.EXPAND, 0)
        self.rightWindow.SetSizer(hbox)
        self.Layout()

        self.Bind(wx.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=leftwin.GetId())
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
            return
        eobj = event.GetEventObject()
        self.leftWindow.SetMaximumSizeX(self.GetSize().width / 3)
        self.leftWindow.SetDefaultSize((event.GetDragRect().width, 1000))
        wx.LayoutAlgorithm().LayoutWindow(self, self.rightWindow)
        self.rightWindow.Refresh()


    def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutWindow(self, self.rightWindow)


    def OnAbout(self, evt):
        info = wx.AboutDialogInfo()
        info = trinfo.getInfo(info)
        info.Description = wordwrap(info.Description, 350, wx.ClientDC(self))
        info.License = wordwrap(info.Licence, 500, wx.ClientDC(self))
        wx.AboutBox(info)


    def OnClose(self, evt):
        """Event handler for window closing"""
        self.Close()


    def OnCloseWindow(self, evt):
        self.config.WriteInt("window_size_x", self.GetSize().width),
        self.config.WriteInt("window_size_y", self.GetSize().height)
        self.config.WriteInt("window_pos_x", self.GetPosition().x)
        self.config.WriteInt("window_pos_y", self.GetPosition().y)
        print afresource.GetLanguage()
        self.config.Write("language", afresource.GetLanguage())
        self.Destroy()


    def OnChangeLanguage(self, evt):
        dlg = wx.SingleChoiceDialog(
                self, _('Select program language\n(This takes effect after restarting the program.)'), _('Select language'),
                [_('English'), _('German')], wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            afresource.SetLanguage(['en', 'de'][dlg.GetSelection()])
        dlg.Destroy()


    def InitView(self, testcase_list):
        self.testcaselist.SetFocus()
        self.testcaselist.InitContent(testcase_list, 1)


    def EnableRunCommand(self, on=True):
        self.GetToolBar().EnableTool(12, on)
        self.GetMenuBar().Enable(201, on)


class TestcaseListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class TestcaseListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        self.il = wx.ImageList(16, 16)
        self.img_empty = self.il.Add(_afimages.getEmptyBitmap())
        self.img_sm_up = self.il.Add(_afimages.getSmallUpArrowBitmap())
        self.img_sm_dn = self.il.Add(_afimages.getSmallDnArrowBitmap())
        self.img_pass  = self.il.Add(_afimages.getTRPassBitmap())
        self.img_fail  = self.il.Add(_afimages.getTRFailBitmap())
        self.img_skip  = self.il.Add(_afimages.getTRSkipBitmap())
        self.img_pend  = self.il.Add(_afimages.getTRPendBitmap())

        self.img = (self.img_fail, self.img_pass, self.img_skip, self.img_pend)
        self.color = (wx.RED, wx.Color(0, 150, 0), wx.BLUE, wx.BLACK)

        self.list = TestcaseListCtrl(self, -1, style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)

        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.list.InsertColumn(0, _("ID"))
        self.list.InsertColumn(1, _("Status"))
        self.list.InsertColumn(2, _("Title"))

        self.itemDataMap = {}
        listmix.ColumnSorterMixin.__init__(self, 3)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)


    def OnItemSelected(self, evt):
        self.currentItem = evt.m_itemIndex
        evt.Skip()


    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list


    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.img_sm_dn, self.img_sm_up)


    def UpdateItem(self, index, status):
        self.itemDataMap[index][1] = status
        self.list.SetStringItem(index, 1, afresource.TEST_STATUS_NAME[status])
        item = self.list.GetItem(index)
        item.SetTextColour(self.color[status])
        item.SetImage(self.img[status])
        self.list.SetItem(item)


    def InitContent(self, testcases, select_id=0):
        self.list.DeleteAllItems()
        self.itemDataMap = {}
        for i in range(len(testcases)):
            testcase = testcases[i]
            ID = testcase['ID']
            idstr = "%4d" % ID
            title = testcase['title']
            testresult = testcase['testresult']
            data = [idstr, testresult, title]
            self.itemDataMap[i] = testcase

            img = self.img[data[1]]
            index = self.list.InsertImageStringItem(sys.maxint, idstr, img)
            self.list.SetItemData(index, i)

            self.list.SetStringItem(index, 0, idstr)
            self.list.SetStringItem(index, 1, _(afresource.TEST_STATUS_NAME[testresult]))
            if isinstance(title, (type(''), type(u''))):
                self.list.SetStringItem(index, 2, title)
            else:
                self.list.SetStringItem(index, 2, str(title))

            item = self.list.GetItem(index)
            item.SetTextColour(self.color[testresult])
            self.list.SetItem(item)

            if ID == select_id:
                self.list.SetItemState(index, wx.LIST_STATE_SELECTED | wx.LIST_STATE_FOCUSED , wx.LIST_STATE_SELECTED | wx.LIST_STATE_FOCUSED )

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.list.SetColumnWidth(0, self.list.GetColumnWidth(0)+10)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)



