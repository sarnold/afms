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
import _afimages
import _afimages
from _afproducttree import *
import afinfo
import afconfig
import afresource, _afsettingsview


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
        self.SetupMenu()
        self.SetupToolbar()
        self.SetupStatusBar()
        self.SetupSashLayout(self)

        icons = wx.IconBundle()
        icons.AddIcon(wx.IconFromBitmap(_afimages.getapp16x16Bitmap()))
        icons.AddIcon(wx.IconFromBitmap(_afimages.getapp32x32Bitmap()))
        self.SetIcons(icons)

        self.rightWindowSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightWindow.SetSizer(self.rightWindowSizer)

        self.bottomWindowSizer = wx.BoxSizer(wx.VERTICAL)
        self.bottomWindow.SetSizer(self.bottomWindowSizer)

        self.treeCtrl = afProductTree(self.leftWindow)
        self.treeCtrl.Disable()

        self.expand = False
        self.filterview = None


    def AddContentView(self, contentview):
        panel = contentview(self.rightWindow)
        self.rightWindowSizer.Clear(deleteWindows = True)
        self.rightWindowSizer.Add(panel, 1, wx.ALL | wx.EXPAND, 6)
        self.rightWindow.Layout()
        panel.Layout()
        return panel


    def AddFilterView(self, filterview):
        """Place a view filter panel in the bottom window"""
        if self.filterview == filterview: return
        if self.filterview is not None:
            # hide filter currently shown
            self.filterview.Hide()
        self.filterview = filterview
        self.filterview.Show()
        self.filterview.SetupScrolling()
        self.bottomWindowSizer.Clear(deleteWindows = False)
        self.bottomWindowSizer.Add(filterview, 1, wx.ALL | wx.EXPAND, 5)
        self.bottomWindow.Layout()
        filterview.Layout()


    def SetFilterInfo(self, filterstate):
        for aftype, state in filterstate.iteritems():
            if state:
                color = wx.GREEN
            else:
                color = self.headpanel.GetBackgroundColour()
            self.filterstatus[aftype].SetBackgroundColour(color)
        self.headpanel.Refresh()


    def OnFilterSizeButtonClick(self, event):
        size = self.bottomWindow.GetSize()
        self.expand = not self.expand
        if self.expand:
            size[1] = self.bottomWindow.GetMaximumSizeY()
            self.filtersizebutton.SetLabel(_('Filter')+' <<')
        else:
            size[1] = self.bottomWindow.GetMinimumSizeY()
            self.filtersizebutton.SetLabel(_('Filter')+' >>')
        self.bottomWindow.Show(self.expand)
        self.bottomWindow.SetSize(size)
        self.bottomWindow.SetDefaultSize(size)
        wx.LayoutAlgorithm().LayoutWindow(self, self.rightWindow)
        self.rightWindow.Refresh()


    def SetupStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        # Sets the three fields to be relative widths to each other.
        self.statusbar.SetStatusWidths([-2, -1, -2])


    def SetupSashLayout(self, parent):
        winids = []

        # where the view filter control bar goes to
        h = 30
        filterfootwin = wx.SashLayoutWindow(
                parent, -1, wx.DefaultPosition, (200, h),
                wx.NO_BORDER|wx.SW_3D
                )
        filterfootwin.SetDefaultSize((1000, h))
        filterfootwin.SetMaximumSizeY(h)
        filterfootwin.SetMinimumSizeY(h)
        filterfootwin.SetOrientation(wx.LAYOUT_HORIZONTAL)
        filterfootwin.SetAlignment(wx.LAYOUT_BOTTOM)
        filterfootwin.SetBackgroundColour(wx.WHITE)
        filterfootwin.SetSashVisible(wx.SASH_TOP, True)

        headpanel = wx.Panel(filterfootwin, style=wx.BORDER_STATIC )
        headpanel.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
        self.filtersizebutton = wx.Button(headpanel, wx.ID_ANY, _('Filter') + ' >>')
        self.Bind(wx.EVT_BUTTON, self.OnFilterSizeButtonClick, self.filtersizebutton)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.filtersizebutton)
        hbox.AddStretchSpacer()

        self.filterstatus = {}
        for artefact in afresource.ARTEFACTLIST:
            stext = wx.StaticText(headpanel, -1, ' '+afresource.ARTEFACTSHORT[artefact]+' ', style=wx.BORDER_STATIC )
            hbox.Add(stext,  0, wx.LEFT | wx.TOP, 5)
            self.filterstatus[artefact] = stext

        hbox.AddSpacer(10)
        headpanel.SetSizer(hbox)
        self.headpanel = headpanel

        # where the view filter goes to
        h = 200
        bottomwin = wx.SashLayoutWindow(
                parent, -1, wx.DefaultPosition, (parent.GetClientSize()[0], h),
                wx.NO_BORDER|wx.SW_3D
                )
        bottomwin.SetMaximumSizeY(200)
        bottomwin.SetMinimumSizeY(h)
        bottomwin.SetOrientation(wx.LAYOUT_HORIZONTAL)
        bottomwin.SetAlignment(wx.LAYOUT_BOTTOM)
        bottomwin.SetSashVisible(wx.SASH_TOP, False)
        bottomwin.Hide()

        # A window to the left of the client window
        leftwin =  wx.SashLayoutWindow(
                parent, -1, wx.DefaultPosition, (200, 30),
                wx.NO_BORDER|wx.SW_3D
                )
        leftwin.SetDefaultSize((self.config.ReadInt("sash_pos_x", 250), 1000))
        leftwin.SetMaximumSizeX(250)
        leftwin.SetMinimumSizeX(150)
        leftwin.SetOrientation(wx.LAYOUT_VERTICAL)
        leftwin.SetAlignment(wx.LAYOUT_LEFT)
        leftwin.SetBackgroundColour(wx.WHITE)
        leftwin.SetSashVisible(wx.SASH_RIGHT, True)

        self.leftWindow = leftwin
        winids.append(leftwin.GetId())
        self.bottomWindow = bottomwin
        winids.append(bottomwin.GetId())

        # will occupy the space not used by the Layout Algorithm
        self.rightWindow = wx.Panel(parent, -1, style=wx.SUNKEN_BORDER)

        self.Bind(wx.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=min(winids), id2=max(winids))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def SetupToolbar(self):
        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT )
        tsize = (24,24)

        edit_bmp = _afimages.getAFEditBitmap()
        tcnew_bmp = _afimages.getTCNewBitmap()
        tsnew_bmp = _afimages.getTSNewBitmap()
        snew_bmp = _afimages.getSNewBitmap()
        fnew_bmp = _afimages.getFNewBitmap()
        rqnew_bmp = _afimages.getRQNewBitmap()
        ucnew_bmp = _afimages.getUCNewBitmap()
        genew_bmp = _afimages.getGENewBitmap()
        new_bmp = _afimages.getProdNewBitmap()
        open_bmp = _afimages.getProdOpenBitmap()
        delete_bmp = _afimages.getAFDeleteBitmap()
        copy_bmp = _afimages.getAFCopyBitmap()
        paste_bmp = _afimages.getAFPasteBitmap()

        tb.SetToolBitmapSize(tsize)
        tb.AddLabelTool(10, _("New"), new_bmp, shortHelp=_("New Product"), longHelp=_("Create new product"))
        tb.AddLabelTool(11, _("Open"), open_bmp, shortHelp=_("Open Product"), longHelp=_("Open existing product"))
        tb.AddLabelTool(12, _("Edit"), edit_bmp, shortHelp=_("Edit artefact"), longHelp=_("Edit selected artefact"))
        tb.EnableTool(12, False)
        tb.AddLabelTool(30, _("Copy"), copy_bmp, shortHelp=_("Copy artefact"), longHelp=_("Copy selected artefact to clipboard"))
        tb.EnableTool(30, False)
        tb.AddLabelTool(31, _("Paste"), paste_bmp, shortHelp=_("Paste artefact"), longHelp=_("Paste artefact from clipboard"))
        tb.EnableTool(31, False)
        tb.AddLabelTool(18, _("Delete"), delete_bmp, shortHelp=_("Delete artefact"), longHelp=_("Delete selected artefact"))
        tb.EnableTool(18, False)
        tb.AddLabelTool(13, _('New'), fnew_bmp, shortHelp=_('New feature'), longHelp=_('Create new feature'))
        tb.EnableTool(13, False)
        tb.AddLabelTool(14, _('New'), rqnew_bmp, shortHelp=_('New requirement'), longHelp=_('Create/attach new requirement'))
        tb.EnableTool(14, False)
        tb.AddLabelTool(17, _('New'), ucnew_bmp, shortHelp=_('New usecase'), longHelp=_('Create/attach new usecase'))
        tb.EnableTool(17, False)
        tb.AddLabelTool(15, _('New'), tcnew_bmp, shortHelp=_('New testcase'), longHelp=_('Create/attach new testcase'))
        tb.EnableTool(15, False)
        tb.AddLabelTool(16, _('New'), tsnew_bmp, shortHelp=_('New testsuite'), longHelp=_('Create new testsuite'))
        tb.EnableTool(16, False)
        tb.AddLabelTool(19, _('New'), snew_bmp, shortHelp=_('New text section'), longHelp=_('Create new text section'))
        tb.EnableTool(19, False)
        tb.AddLabelTool(20, _('New'), genew_bmp, shortHelp=_('New glossary entry'), longHelp=_('Create new glossary entry'))
        tb.EnableTool(20, False)

        tb.Realize()

    def SetupMenu(self):
        "Create menubar"
        # Create the menubar
        menuBar = wx.MenuBar()
        # and a menu
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(101, _('&New product ...\tCtrl-N'), _('Create new product'))
        menu.Append(102, _('&Open product ...\tCtrl-O'), _('Open existing product'))
        menu.Append(103, _('Export as HTML ...'), _('Export product to HTML file'))
        menu.Append(104, _('Export as XML ...'), _('Export product to XML files'))
        menu.Enable(103, False)
        menu.Enable(104, False)
        menu.Append(105, _('Import ...'), _('Import artefacts from AF database'))
        menu.Enable(105, False)
        menu.AppendSeparator()
        menu.Append(106, _('Statistics ...'), _('Statistics of current AF database'))
        menu.Enable(106, False)
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, _('E&xit\tAlt-X'), _('Exit this application'))

        # adding a file history to the menu
        self.filehistory = wx.FileHistory()
        self.filehistory.UseMenu(menu)
        self.filehistory.Load(self.config)

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, _('&File'))

        menu = wx.Menu()
        menu.Append(201, _('&Edit artefact ...\tCtrl-E'), _('Edit selected artefact'))
        menu.Enable(201, False)

        menu.Append(203, _('&Copy artefact\tCtrl-C'), _('Copy selected artefact to clipboard'))
        menu.Enable(203, False)

        menu.Append(204, _('&Paste artefact\tCtrl-V'), _('Paste artefact from clipboard'))
        menu.Enable(204, False)

        menu.Append(202, _('&Delete artefact ...\tDel'), _('Delete selected artefact'))
        menu.Enable(202, False)
        menuBar.Append(menu, _('&Edit'))

        menu = wx.Menu()
        menu.Append(301, _('New &feature ...'), _('Create new feature'))
        menu.Enable(301, False)

        menu.Append(302, _('New &requirement ...'), _('Create new requirement'))
        menu.Enable(302, False)

        menu.Append(305, _('New &usecase ...'), _('Create new usecase'))
        menu.Enable(305, False)

        menu.Append(303, _('New &testcase ...'), _('Create new testcase'))
        menu.Enable(303, False)

        menu.Append(304, _('New test&suite ...'), _('Create new testsuite'))
        menu.Enable(304, False)

        menu.Append(306, _('New text section ...'), _('Create new text section'))
        menu.Enable(306, False)

        menu.Append(307, _('New glossary entry ...'), _('Create new glossary entry'))
        menu.Enable(307, False)
        menuBar.Append(menu, _('&New'))

        menu = wx.Menu()
        menu.Append(401, _('Database to archive ...'), _('Dump current database to archive file'))
        menu.Enable(401, False)
        menu.Append(402, _('Archive to database ...'), _('Create database from archive file'))
        menu.Enable(402, True)
        menuBar.Append(menu, _('&Archive'))

        menu = wx.Menu()
        menu.Append(501, _('General ...'), _('General settings'))
        self.Bind(wx.EVT_MENU, self.Settings, id = 501)
        menu.Enable(501, True)
        menuBar.Append(menu, _('&Settings'))

        menu = wx.Menu()
        menu.Append(901, _('About ...'), _('Info about this program'))
        self.Bind(wx.EVT_MENU, self.OnAbout, id = 901)
        menu.Enable(901, True)
        menuBar.Append(menu, _('&Help'))

        self.SetMenuBar(menuBar)


    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.SASH_STATUS_OUT_OF_RANGE:
            return
        eobj = event.GetEventObject()
        if eobj is self.leftWindow:
            self.leftWindow.SetMaximumSizeX(self.GetSize().width / 3)
            self.leftWindow.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eobj is self.bottomWindow:
            self.bottomWindow.SetDefaultSize((1000, event.GetDragRect().height))
        wx.LayoutAlgorithm().LayoutWindow(self, self.rightWindow)
        self.rightWindow.Refresh()


    def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutWindow(self, self.rightWindow)
        event.Skip()


    def OnClose(self, evt):
        """Event handler for window closing"""
        self.Close()


    def OnCloseWindow(self, evt):
        self.config.WriteInt("window_size_x", self.GetSize().width)
        self.config.WriteInt("window_size_y", self.GetSize().height)
        self.config.WriteInt("window_pos_x", self.GetPosition().x)
        self.config.WriteInt("window_pos_y", self.GetPosition().y)
        self.config.WriteInt("sash_pos_y", self.bottomWindow.GetSize().height)
        self.config.WriteInt("sash_pos_x", self.leftWindow.GetSize().width)
        self.config.Write("language", afresource.GetLanguage())
        self.filehistory.Save(self.config)
        self.Destroy()


    def OnAbout(self, evt):
        info = wx.AboutDialogInfo()
        info = afinfo.getInfo(info)
        info.Description = wordwrap(info.Description, 350, wx.ClientDC(self))
        info.License = wordwrap(info.Licence, 500, wx.ClientDC(self))
        wx.AboutBox(info)


    def OnSettings(self, evt):
        _afsettingsview.EditSettings(self)


    def InitView(self, path, artefactnames, number_of_deleted_artefacts):
        """Init the tree view, set status bar and enable edit functions"""
        self.InitTree(artefactnames, number_of_deleted_artefacts)
        self.treeCtrl.SelectItem(self.treeCtrl.root)
        self.SetStatusText(path, 2)
        for m, i in zip([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3], [103, 104, 105, 106, 201, 202, 203, 204, 301, 302, 303, 304, 305, 306, 307, 401]):
            self.GetMenuBar().GetMenu(m).Enable(i, True)
        for i in (12,13,14,15,16, 17, 18, 19, 20, 30, 31):
            self.GetToolBar().EnableTool(i, True)


    def InitTree(self, artefactnames, number_of_deleted_artefacts):
        self.treeCtrl.InitTreeCtrl(artefactnames, number_of_deleted_artefacts)


    def AddItem(self, parent, item):
        self.treeCtrl.AddChildItem(parent, item)
