#!/usr/bin/env python
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


"""
Artefact editor

Artefact editor for managing Features, Requirements, Usecases, Testcases
and Testsuites. This module implements the controller part in the design.

@author: Achim Koehler
@version: $Rev$
"""


import os, sys, time
import logging
import wx
import _afimages
import afconfig
import afmodel
import _afhelper
from _afartefactlist import *
from _afproductinformation import *
from _aftrashinformation import *
from _affeatureview import *
from _afrequirementview import *
from _aftestcaseview import *
from _afusecaseview import *
from _aftestsuiteview import *
from _afmainframe import *
from _afeditartefactdlg import *
import afexporthtml
import afexportxml
import _afimporter 
from afresource import _
import afresource
import _afclipboard
from _afartefact import cChangelogEntry

#TODO: validator for features, similar to requirements validator is missing
#TODO: enter key on Feature/Requirement/... in tree should expand the tree
#TODO: empty trash function
#TODO: search functionality

_EDIT_MODE = False

class MyApp(wx.App):
    """
    wxWidgets main application class.
    """
    def OnInit(self):
        """
        Initialization function called by wxWidgets framework.
        
        Event binding, class attributes definitions and similar stuff is
        done here.
        
        @rtype:  boolean
        @return: C{True} on success, C{False} else
        """
        # Read configuration an check for existence of workdir
        self.config = wx.FileConfig(appName="afeditor", vendorName="ka", localFilename="afeditor.cfg", globalFilename="afeditor.gfg", style=wx.CONFIG_USE_LOCAL_FILE|wx.CONFIG_USE_GLOBAL_FILE )
        sp = wx.StandardPaths.Get()
        documents_dir = wx.StandardPaths.GetDocumentsDir(sp)
        workdir = self.config.Read("workdir", documents_dir)
        if not os.path.exists(workdir):
             self.config.Write("workdir", documents_dir)
        wx.Config.Set(self.config)

        self.model = afmodel.afModel(self, self.config.Read("workdir", documents_dir))

        afresource.SetLanguage(self.config.Read("language", "en"))
        self.mainframe = MainFrame(None, "AF Editor")
        self.SetTopWindow(self.mainframe)
        self.mainframe.Show(True)
        self.wildcard = afresource.AF_WILDCARD
        self.htmlwildcard = afresource.HTML_WILDCARD
        self.dont_annoy_at_delete = False
        self.dont_annoy_at_undelete = False
        self.DisableUpdateNodeView = False
        self.DisableOnSelChanged = False
        
        self.productview = 0
        self.trashview = -1
        self.listview = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.trashlistview = self.listview[5:]
        (self.featurelistview, self.requirementlistview,
         self.testcaselistview, self.testsuitelistview, self.usecaselistview,
         self.trashfeaturelistview, self.trashrequirementlistview,
         self.trashtestcaselistview, self.trashtestsuitelistview,
         self.trashusecaselistview) = self.listview
         
        self.singleview = (20, 21, 22, 23, 24)
        (self.featureview, self.requirementview, self.testcaseview,
         self.usecaseview, self.testsuiteview)   = self.singleview

        self.notebooktab = {self.featureview   : 0,  self.requirementview : 0,
                            self.testcaseview  : 0,  self.usecaseview     : 0,
                            self.testsuiteview : 0}
        self.currentview = None

        self.PARENTID = "FEATURES REQUIREMENTS USECASES TESTCASES TESTSUITES".split()
        self.delfuncs = (self.model.deleteFeature, self.model.deleteRequirement, self.model.deleteUsecase, self.model.deleteTestcase, self.model.deleteTestsuite)
        
        self.Bind(wx.EVT_MENU, self.OnNewProduct, id=101)
        self.Bind(wx.EVT_MENU, self.OnOpenProduct, id=102)
        self.Bind(wx.EVT_MENU, self.OnExportHTML, id=103)
        self.Bind(wx.EVT_MENU, self.OnExportXML, id=104)
        self.Bind(wx.EVT_MENU, self.OnImport, id=105)
        
        self.Bind(wx.EVT_MENU, self.OnEditArtefact, id = 201)
        self.Bind(wx.EVT_MENU, self.OnDeleteArtefact, id = 202)
        self.Bind(wx.EVT_MENU, self.copyArtefactToClipboard, id = 203)
        self.Bind(wx.EVT_MENU, self.pasteArtefactFromClipboard, id = 204)

        self.Bind(wx.EVT_MENU, self.OnNewFeature, id = 301)
        self.Bind(wx.EVT_MENU, self.OnNewRequirement, id = 302)
        self.Bind(wx.EVT_MENU, self.OnNewTestcase, id = 303)
        self.Bind(wx.EVT_MENU, self.OnNewTestsuite, id = 304)
        self.Bind(wx.EVT_MENU, self.OnNewUsecase, id = 305)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=300)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnTreeItemActivated, id=301)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        ##self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected)
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        global arguments
        if len(arguments) > 0:
            try:
                self.OpenProduct(arguments[0])
            except:
                print("Could not open file %s" % arguments[0])
                sys.exit(2)
            
        return True
    
            
    def copyArtefactToClipboard(self, evt=None):
        (parent_id, item_id) = self.mainframe.treeCtrl.GetSelectedItem()
        if parent_id == "PRODUCT":
            # a list is shown in the right panel, get ID of selected item
            (parent_id, item_id) = self.contentview.GetSelectionID()
        if parent_id is None: return
        if parent_id.startswith('TRASH'): return
        if item_id is None: return

        logging.debug("afeditor.MyApp.copyArtefactToClipboard(): %s" % str((parent_id, item_id)))
        
        try:
            idx = [item['id'] for item in afresource.ARTEFACTS].index(parent_id)
        except ValueError:
            return
        
        artefact = [self.model.getFeature, self.model.getRequirement, self.model.getUsecase,
                   self.model.getTestcase, self.model.getTestsuite][idx](item_id)
                   
        copytoclip = [_afclipboard.copyFeatureToClipboard, _afclipboard.copyRequirementToClipboard,
                      _afclipboard.copyUsecaseToClipboard, _afclipboard.copyTestcaseToClipboard,
                      _afclipboard.copyTestsuiteToClipboard][idx]
        copytoclip(artefact)
        
        
    def pasteArtefactFromClipboard(self, evt=None):
        # Well, I know here is a lot of repeated code
        # But I think this makes it better understandable
        (af_kind, afobj) = _afclipboard.getArtefactFromClipboard()
        if af_kind is None:
            return
        
        self.DisableUpdateNodeView = True
        afobj['ID'] = -1 # it is a new artefact
        cle = cChangelogEntry(user=afconfig.CURRENT_USER, description='', changetype=0, date=time.strftime(afresource.TIME_FORMAT))
        afobj.setChangelog(cle)

        if af_kind == 'AFMS_FEATURE':
            (data, new_artefact) = self.model.saveFeature(afobj)
            if self.currentview == self.featurelistview:
                self.contentview.AppendItem(data)
            self.updateView([wx.ID_OK, new_artefact, data, None], 'FEATURES', -1)
            
        elif af_kind == 'AFMS_REQUIREMENT':
            (data, new_artefact) = self.model.saveRequirement(afobj)
            if self.currentview == self.requirementlistview:
                # reformat basedata to fit into the list view
                self.contentview.AppendItem(data)
            self.updateView([wx.ID_OK, new_artefact, data, None], 'REQUIREMENTS', -1)

        elif af_kind == 'AFMS_USECASE':
            (data, new_artefact) = self.model.saveUsecase(afobj)
            if self.currentview == self.usecaselistview:
                self.contentview.AppendItem(data)
            self.updateView([wx.ID_OK, new_artefact, data, None], 'USECASES', -1)

        elif af_kind == 'AFMS_TESTCASE':
            (data, new_artefact) = self.model.saveTestcase(afobj)
            if self.currentview == self.testcaselistview:
                # reformat basedata to fit into the list view
                self.contentview.AppendItem(data)
            self.updateView([wx.ID_OK, new_artefact, data, None], 'TESTCASES', -1)

        elif af_kind == 'AFMS_TESTSUITE':
            (data, new_artefact) = self.model.saveTestsuite(afobj)
            if self.currentview == self.testsuitelistview:
                # reformat data to the same format as it is returned by self.model.getTestsuiteList()
                self.contentview.AppendItem(data)
            self.updateView([wx.ID_OK, new_artefact, data, None], 'TESTSUITES', -1)


    def OnPageChanged(self, evt):
        """
        Event handler function called when a notebook page has changed.
        @type  evt: wx.NotebookEvent
        @param evt: event data
        """
        #logging.debug('OnPageChanged,  old:%d, new:%d\n' % (event.GetOldSelection(), evt.GetSelection()))
        self.notebooktab[self.currentview] = evt.GetSelection()


    def OnNewProduct(self, evt):
        """
        Event handler for menu item or toolbar item 'New Product'.
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        dlg = wx.FileDialog(
            self.mainframe, message = _("Save new product to file"),
            defaultDir = self.model.currentdir,
            defaultFile = "",
            wildcard = self.wildcard,
            style=wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            try:
                self.model.requestNewProduct(path)
                self.InitView()
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), _('Error creating product'))
                logging.error(str(sys.exc_info()))


    def OnOpenProduct(self, evt):
        """
        Event handler for menu item or toolbar item 'Open Product'.
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        dlg = wx.FileDialog(
            self.mainframe, message = _("Open product file"),
            defaultDir = self.model.currentdir,
            defaultFile = "",
            wildcard = self.wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            try:
                self.OpenProduct(path)
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), _('Error opening product!'))
            
            
    def OpenProduct(self, path):
        """
        Open product database file.
        @type  path: string
        @param path: Path of product database file
        """
        self.model.requestOpenProduct(path)
        self.InitView()


    def InitView(self):
        path = self.model.getFilename()
        artefactinfo = self.model.getArtefactNames()
        number_of_deleted_artefacts = self.model.getNumberOfDeletedArtefacts()
        self.DisableOnSelChanged = True
        self.mainframe.InitView(path, artefactinfo, number_of_deleted_artefacts)
        self.updateNodeView(None, "PRODUCT")
        self.DisableOnSelChanged = False


    def OnEditArtefact(self, evt):
        """
        Command 'Edit feature' or similar has been issued by menu or toolbat.
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        logging.debug("afeditor.OnEditArtefact(), self.currentview=%s" % self.currentview)
        item = self.mainframe.treeCtrl.GetSelection()
        if not item: return
    
        (parent_id, item_id) = self.mainframe.treeCtrl.GetItemInfo(item)
        if parent_id == "TRASH": return
        if parent_id == "PRODUCT":
            # a list is shown, we want to edit the item selected in the list
            try:
                (tree_parent_id, tree_item_id) = (parent_id, item_id)
                (parent_id, item_id) = self.contentview.GetSelectionID()
                if item_id is None: return
            except:
                # no item selected in the list
                return
        elif item_id == 'PRODUCT':
            pass
        elif parent_id is None:
            return

        self.requestEditView(parent_id, item_id)
        logging.debug("afeditor.OnEditArtefact() done")


    def OnTreeItemActivated(self, evt):
        """
        Item in product tree has been activated by double click or return key
        This is handled as request to edit the item.
        @type  evt: wx.TreeEvent
        @param evt: event data
        """
        self.OnEditArtefact(None)

            
    def OnDeleteArtefact(self, evt):
        """
        The menu item or toolbar item 'Delete Artefact' was issued
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        logging.debug("afeditor.OnDeleteArtefact()")
        delete_from_list = False
        item = self.mainframe.treeCtrl.GetSelection()
        if not item: return
        
        (parent_id, item_id) = self.mainframe.treeCtrl.GetItemInfo(item)
        if parent_id == "TRASH": return
        if parent_id == "PRODUCT":
            # a list is shown, we want to delete the item selected in the list
            try:
                (tree_parent_id, tree_item_id) = (parent_id, item_id)
                delete_from_list = True
                (parent_id, item_id) = self.contentview.GetSelectionID()
            except:
                # no item selected in the list
                return
        elif parent_id is None:
            return
        
        if not self.dont_annoy_at_delete:
            (retval, self.dont_annoy_at_delete) = _afhelper.DontAnnoyMessageBox(_("Really delete artefact?"), _("Delete artefact"))
            if retval != wx.ID_YES: return
        
        try:
            self.delfuncs[self.PARENTID.index(parent_id)](item_id)
        
            (wxTreeParentId, wxTreeChildId) = self.mainframe.treeCtrl.FindItem(parent_id, item_id)
            self.mainframe.treeCtrl.Delete(wxTreeChildId)

            self.mainframe.treeCtrl.UpdateTrashIcons(self.model.getNumberOfDeletedArtefacts())
            
            if delete_from_list is True:
                # Update artefact list in right panel
                self.DisableUpdateNodeView = True
                self.contentview.DeleteSelectedItem()
                self.mainframe.treeCtrl.SelectItem(wxTreeParentId)
                self.mainframe.rightWindow.SetFocus()
                self.contentview.SetFocus()
        except:
            _afhelper.ExceptionMessageBox(sys.exc_info())


    def OnExportHTML(self, evt):
        """
        Export database to HTML file
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        dlg = wx.FileDialog(
            self.mainframe, message = _("Save HTML to file"),
            defaultDir = self.model.currentdir,
            defaultFile = os.path.splitext(self.model.getFilename())[0] + ".html",
            wildcard = self.htmlwildcard,
            style=wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            #try:
                afexporthtml.afExportHTML(path, self.model)
            #except:
                #_afhelper.ExceptionMessageBox(sys.exc_info(), 'Error exporting to HTML!')
        

    def OnExportXML(self, evt):
        """
        Export database to XML file
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        dlg = wx.FileDialog(
            self.mainframe, message = _("Save XML to file"),
            defaultDir = self.model.currentdir,
            defaultFile = os.path.splitext(self.model.getFilename())[0] + ".xml",
            wildcard = afresource.XML_WILDCARD,
            style=wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            #try:
                afexportxml.afExportXML(path, self.model)
            #except:
             #   _afhelper.ExceptionMessageBox(sys.exc_info(), 'Error exporting to XML!')


    def GetParentAndItemID(self):
        """
        Figure out which item is currently selected, either in the left panel tree
        or in an artefact list in the right panel.
        """
        (parent_id, item_id) = (None, None)
        treeitem = self.mainframe.treeCtrl.GetCurrentItem()
        if treeitem:
            (parent_id, item_id) = self.mainframe.treeCtrl.GetItemInfo(treeitem)
        if not treeitem or parent_id == "PRODUCT":
            # no selection in left tree or list in right panel,
            # so lock for an artefact list in the right panel
            try:
                (parent_id, item_id) = self.contentview.GetSelectionID()
            except:
                pass
        return (parent_id, item_id)
                
        
    def OnNewFeature(self, evt):
        """
        The menu item or toolbar item 'New Feature' was issued
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        self.requestEditView("FEATURES", -1)

    
    def OnNewRequirement(self, evt):
        """
        The menu item or toolbar item 'New Requirement' was issued
        @type  evt: wx.CommandEvent
        @param evt: event data
        
        If a featue is selected and the 'New Requirement' command is issued
        then the new requirement will be attached to the selected feature.
        """
        # Get the current selected item when the new command is issued
        (parent_id, item_id) = self.GetParentAndItemID()
        result = self.requestEditView("REQUIREMENTS", -1)
        if result[0] != wx.ID_SAVE: return
        if (parent_id != "FEATURES"): return
        rq_id = result[2]['ID']
        self.model.addFeatureRequirementRelation(item_id, rq_id)


    def OnNewTestcase(self, evt):
        """
        The menu item or toolbar item 'New Testcase' was issued
        @type  evt: wx.CommandEvent
        @param evt: event data

        If a requirement or a testsuite is selected and the 'New Testcase'
        command is issued then the new testcase will be attached to the selected
        requirement or testsuite.
        """
        # Get the current selected item when the new command is issued
        (parent_id, item_id) = self.GetParentAndItemID()
        result = self.requestEditView("TESTCASES", -1)
        if result[0] != wx.ID_SAVE: return
        tc_id = result[2]['ID']
        if (parent_id == "REQUIREMENTS"):
            self.model.addRequirementTestcaseRelation(item_id, tc_id)
        elif (parent_id == "TESTSUITES"):
            self.model.addTestsuiteTestcaseRelation(item_id, tc_id)
            

    def OnNewUsecase(self, evt):
        """
        The menu item or toolbar item 'New Usecase' was issued
        @type  evt: wx.CommandEvent
        @param evt: event data

        If a requirement is selected and the 'New Usecase' command is issued
        then the new usecase will be attached to the selected requirement.
        """
        # Get the current selected item when the new command is issued
        (parent_id, item_id) = self.GetParentAndItemID()
        result = self.requestEditView("USECASES", -1)
        if result[0] != wx.ID_SAVE: return
        uc_id = result[2]['ID']
        if (parent_id == "REQUIREMENTS"):
            self.model.addRequirementUsecaseRelation(item_id, uc_id)
            
        
    def OnNewTestsuite(self, evt):
        """
        The menu item or toolbar item 'New Testsuite' was issued
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        self.requestEditView("TESTSUITES", -1)


    def OnSelChanged(self, evt):
        """
        The selection in the product tree has changed
        @type  evt: wx.TreeEvent
        @param evt: event data
        """
        if self.DisableOnSelChanged: return
        logging.debug("afeditor.OnSelChanged()")
        item = evt.GetItem()
        if item:
            (parent_id, item_id) = self.mainframe.treeCtrl.GetItemInfo(item)
            self.updateNodeView(parent_id, item_id)
            #logging.debug("OnSelChanged: <%s, %s>\n" % (parent_id, item_id))
            self.mainframe.treeCtrl.SetFocus()
            
        
    def OnListItemActivated(self, evt):
        """
        An item in the feature/requirement/... list has been activated
        @type  evt: wx.ListEvent
        @param evt: event data
        """
        logging.debug("afeditor.OnListItemActivated(), self.currentview=%s" % self.currentview)
        (parent_id, item_id) = self.contentview.GetSelectionID()
        if self.currentview in self.trashlistview:
            self.undeleteArtefact(parent_id, item_id)
        else:
            self.requestEditView(parent_id, item_id)


    def ViewProductInfo(self, product_info):
        """
        Display product information in the right panel
        @type  product_info: nested tuple
        @param product_info: Product data
        """
        self.currentview = self.productview
        self.contentview = self.mainframe.AddContentView(afProductInformation)
        self.contentview.InitContent(product_info)


    def ViewTrashInfo(self, trash_info):
        """
        Display trash information in the right panel
        @type  trash_info: dictionary
        @param trash_info: Dictionary with artefact names as keys and number of deleted
                           artefacts as values
        """
        self.currentview = self.trashview
        self.contentview = self.mainframe.AddContentView(afTrashInformation)
        self.contentview.InitContent(trash_info)


    def ViewArtefactList(self, _contentview, _currentview, artefact_list, select_id=0):
        """
        Display list with all artefacts of a certain category in the right panel
        @type   _contentview: list view object
        @param  _contentview: Object to display artefact list
        @type   _currentview: integer
        @param  _currentview: flag for current view
        @type  artefact_list: tuple list
        @param artefact_list: List with artefact objects
        @type      select_id: integer
        @param     select_id: Item to be selected in the list, 0 means none
        """
        self.currentview = _currentview
        self.contentview = self.mainframe.AddContentView(_contentview)
        self.contentview.InitContent(artefact_list, select_id)


    def ViewArtefact(self, data, _contentview, _currentview):
        """
        Display certain artefact in the right panel
        @type           data: object
        @param           data: artefact objects
        @type   _contentview: view object
        @param  _contentview: Object to display artefact 
        @type   _currentview: integer
        @param  _currentview: flag for current view
        """
        self.currentview = None
        contentview = self.mainframe.AddContentView(_contentview)
        self.currentview = _currentview
        contentview.ChangeSelection(self.notebooktab[self.currentview])
        contentview.InitContent(data)


    def EditProductInfo(self, product_info):
        """
        Edit product information in dialog window
        @type  product_info: nested tuple
        @param product_info: Product data
        """
        dlg = EditArtefactDialog(self.mainframe.rightWindow, -1, title=_("Edit Product"), contentview = afProductInformation)
        dlg.contentview.InitContent(product_info)
        dlgResult = dlg.ShowModal()
        if dlgResult == wx.ID_SAVE:
            product_info = dlg.contentview.GetContent()
            self.model.saveProductInfo(product_info)
            self.ViewProductInfo(product_info)


    def EditFeature(self, feature):
        """
        Edit feature data in dialog window
        @type  feature: object
        @param feature: Feature object
        @rtype:  nested tuple
        @return: same as L{EditArtefact}
        """
        feature.validator =  self.validateArtefact
        return self.EditArtefact(_("Edit feature"), afFeatureNotebook, self.model.saveFeature, feature)


    def EditRequirement(self, requirement):
        """
        Edit requirement data in dialog window
        @type  requirement: object
        @param requirement: Requirement object
        @rtype:  nested tuple
        @return: same as L{EditArtefact}
        """
        logging.debug("afeditor.EditRequirement()")
        afconfig.ASSIGNED_NAME = self.model.requestAssignedList()
        requirement.validator = self.validateArtefact
        return self.EditArtefact(_("Edit requirement"), afRequirementNotebook, self.model.saveRequirement, requirement)


    def validateArtefact(self, initial_requirement, current_requirement):
        """
        Validate an edited requirement or feature
        @type initial_basedata  : tuple
        @param initial_basedata : requirement/feature basedata before editing
        @type current_basedata  : tuple
        @param current_basedata : requirement/feature basedata after editing
        @type changelog         : tuple
        @param changelog        : changelog data
        @rtype                  : tuple
        @return                 : Validation result and optional error message
                                  - result 0 means everything okay
                                  - result 1 and 2 means validation failed
        """
        initial_status = initial_requirement['status']
        current_status = current_requirement['status']
        changelog_text = current_requirement.getChangelog()['description']
        if initial_status == afresource.STATUS_APPROVED and current_status == afresource.STATUS_APPROVED and len(changelog_text) <= 0:
            return (1, _("Artefact is already approved!\nChangelog description is required."))
        if initial_status == afresource.STATUS_COMPLETED and current_status == afresource.STATUS_COMPLETED:
            return (2, _("Artefact is already completed!\nChanges are prohibited!"))
        return (0, None)


    def EditTestcase(self, testcase):
        """
        Edit testcase data in dialog window
        @type  testcase: object
        @param testcase: Testcase object
        @rtype:  nested tuple
        @return: same as L{EditArtefact}
        """
        return self.EditArtefact(_("Edit testcase"), afTestcaseNotebook, self.model.saveTestcase, testcase)


    def EditUsecase(self, usecase):
        """
        Edit usecase data in dialog window
        @type  usecase: object
        @param usecase: Usecase object
        @rtype:  nested tuple
        @return: same as L{EditArtefact}
        """
        afconfig.ACTOR_NAME = self.model.requestActorList()
        afconfig.STAKEHOLDER_NAME = self.model.requestStakeholderList()
        return self.EditArtefact(_("Edit usecase"), afUsecaseNotebook, self.model.saveUsecase, usecase)


    def EditTestsuite(self, testsuite):
        """
        Edit testsuite data in dialog window
        @type  testsuite: object
        @param testsuite: Testsuite object
        @return: same as L{EditArtefact}
        @rtype:  nested tuple
        """
        return self.EditArtefact(_("Edit testsuite"), afTestsuiteView, self.model.saveTestsuite, testsuite)

        
    def EditArtefact(self, title, contentview, savedata, data):
        """
        Edit artefact in a dialog window.
        @type        title: string
        @param       title: Dialog window title
        @type  contentview: artefact  view object
        @param contentview: Object to display/edit artefact list
        @type     savedata: function
        @param    savedata: Function to save edited data
        @type         data: nested tuple
        @param        data: Artefact data
        @return: Nested tuple with values
          0. Return value of dialog, either C{wx.SAVE} or C{wx.CANCEL}
          1. Boolean flag indicating a new artefact if set
          2. Possibly edited artefact object
          3. The input parameter contentview
        @rtype:  nested tuple
        """
        logging.debug("afeditor.EditArtefact()")
        dlg = EditArtefactDialog(self.mainframe.rightWindow, -1, title=title, contentview=contentview)
        dlg.contentview.InitContent(data)
        #TODO: pass validator to this function and use this to init validator of contentview
        # this should not be the wxValidator
        global _EDIT_MODE
        _EDIT_MODE = True
        dlgResult = dlg.ShowModal()
        _EDIT_MODE = False
        if dlgResult == wx.ID_SAVE:
            data = dlg.contentview.GetContent()
            try:
                (data, new_artefact) = savedata(data)
            except:
                new_artefact = False
                msg = str(sys.exc_info()[0])+"\n"+str(sys.exc_info()[1])
                wx.MessageBox(msg, _('Error saving artefact'), wx.OK | wx.ICON_ERROR)
                logging.error(msg)
                logging.error(sys.exc_info())
        else:
            data = None
            new_artefact = False
        dlg.Destroy()
        logging.debug("afeditor.EditArtefact() done")
        return [dlgResult, new_artefact, data, contentview]
        

    def requestEditView(self, parent_id, item_id):
        """
        Handle the request to edit an artefact
        
        Depending on C{parent_id} and C{item_id} the corresponding editing function
        is called. This is one of
            - L{EditProductInfo}
            - L{EditFeature}
            - L{EditRequirement}
            - L{EditTestcase}
            - L{EditUsecase}
            - L{EditTestsuite}
        @type  parent_id: string
        @param parent_id: The kind of artefact to be edited
        @type    item_id: int
        @param   item_id: The ID of the artefact to edit
        @return: same as L{EditArtefact} except for feature, requirement and
                 testsuite editing. For these kind of artefacts a nested tuple
                 with values
                     0. Return value of dialog, either C{wx.SAVE} or C{wx.CANCEL}
                     1. Boolean flag indicating a new artefact if set
                     2. Basedata part of Possibly edited artefact data
                     3. The input parameter contentview
                 is returned.
        @rtype:  nested tuple
        """
        logging.debug("afeditor.requestEditView(%s, %s)" % (parent_id, item_id))
        result = None
        
        if item_id == "PRODUCT":
            # Root node of tree is selected, edit project information
            self.EditProductInfo(self.model.getProductInformation())
            return

        elif parent_id == "FEATURES":
            result = self.EditFeature(self.model.getFeature(item_id))
            if result[0] == wx.ID_SAVE:
                # feature data is structured a little bit differently
                result = [result[0], result[1], result[2], result[3]]

        elif parent_id == "REQUIREMENTS":
            result = self.EditRequirement(self.model.getRequirement(item_id))
            if result[0] == wx.ID_SAVE:
                # requirements data is structured a little bit differently
                result = [result[0], result[1], result[2], result[3]]

        elif parent_id == "TESTCASES":
            result = self.EditTestcase(self.model.getTestcase(item_id))
            if result[0] == wx.ID_SAVE:
                result = [result[0], result[1], result[2], result[3]]

        elif parent_id == "USECASES":
            result = self.EditUsecase(self.model.getUsecase(item_id))
            if result[0] == wx.ID_SAVE:
                result = [result[0], result[1], result[2], result[3]]
                
        elif parent_id == "TESTSUITES":
            result = self.EditTestsuite(self.model.getTestsuite(item_id))
            if result[0] == wx.ID_SAVE:
                # testsuite data is structured a little bit differently
                result = [result[0], result[1], result[2], result[3]]
            
        if result is not None:
            self.updateView(result, parent_id, item_id)

        return result


    def undeleteArtefact(self, parent_id, item_id):
        """
        Restore a previously deleted artefact

        @type  parent_id: string
        @param parent_id: The kind of artefact to be restored
        @type    item_id: int
        @param   item_id: The ID of the artefact to restore
        """
        logging.debug("afeditor.undeleteArtefact(parent_id=%s, item_id=%d)" % (parent_id, item_id))
        if not self.dont_annoy_at_undelete:
            (retval, self.dont_annoy_at_undelete) = _afhelper.DontAnnoyMessageBox(_("Really restore artefact?"), _("Restore artefact"))
            if retval == wx.NO: return
        try:
            data = self.delfuncs[self.PARENTID.index(parent_id)](item_id, delcnt=0)
            self.updateNodeView("TRASH", "TRASH"+parent_id)
            self.mainframe.AddItem(parent_id, data)
            self.mainframe.treeCtrl.UpdateTrashIcons(self.model.getNumberOfDeletedArtefacts())
        except:
            _afhelper.ExceptionMessageBox(sys.exc_info())


    def updateNodeView(self, parent_id, item_id, select_id=0):
        """
        Handle change of selection in the main tree in the left panel
        
        Depending on the selection in the left tree the display in the right panel
        is updated. This is done by calling one of the methods
            - L{ViewProductInfo}
            - L{ViewArtefactList}
            - L{ViewArtefact}
        
        @type  parent_id: string
        @param parent_id: String identifying the parent of the selected node
        @type    item_id: integer
        @param   item_id: ID of the selected node
        @type  select_id: integer
        @param select_id: Item to be selected in an artefact list, 0 means none
        """
        if self.DisableUpdateNodeView:
            self.DisableUpdateNodeView = False
            return
        logging.debug("afeditor.updateNodeView(%s, %s)" % (parent_id, item_id))
        if item_id == "PRODUCT":
            # Root node of tree is selected, show project information
            self.ViewProductInfo(self.model.getProductInformation())
        elif item_id == "FEATURES":
            self.ViewArtefactList(afFeatureList, self.featurelistview, self.model.getFeatureList(), select_id)
        elif item_id == "REQUIREMENTS":
            self.ViewArtefactList(afRequirementList, self.requirementlistview, self.model.getRequirementList(), select_id)
        elif item_id == "TESTCASES":
            self.ViewArtefactList(afTestcaseList, self.testcaselistview, self.model.getTestcaseList(), select_id)
        elif item_id == "TESTSUITES":
            self.ViewArtefactList(afTestsuiteList, self.testsuitelistview, self.model.getTestsuiteList(), select_id)
        elif item_id == "USECASES":
            self.ViewArtefactList(afUsecaseList, self.usecaselistview, self.model.getUsecaseList(), select_id)
        elif parent_id == "FEATURES":
            self.ViewArtefact(self.model.getFeature(item_id), afFeatureNotebook, self.featureview)
        elif parent_id == "REQUIREMENTS":
            self.ViewArtefact(self.model.getRequirement(item_id), afRequirementNotebook, self.requirementview)
        elif parent_id == "TESTCASES":
            self.ViewArtefact(self.model.getTestcase(item_id), afTestcaseNotebook, self.testcaseview)
        elif parent_id == "USECASES":
            self.ViewArtefact(self.model.getUsecase(item_id), afUsecaseNotebook, self.usecaseview)
        elif parent_id == "TESTSUITES":
            self.ViewArtefact(self.model.getTestsuite(item_id), afTestsuiteView, self.testsuiteview)
        elif item_id == "TRASHFEATURES":
            self.ViewArtefactList(afFeatureList, self.trashfeaturelistview, self.model.getFeatureList(deleted=True), select_id)
        elif item_id == "TRASHREQUIREMENTS":
            self.ViewArtefactList(afRequirementList, self.trashrequirementlistview, self.model.getRequirementList(deleted=True), select_id)
        elif item_id == "TRASHTESTCASES":
            self.ViewArtefactList(afTestcaseList, self.trashtestcaselistview, self.model.getTestcaseList(deleted=True), select_id)
        elif item_id == "TRASHUSECASES":
            self.ViewArtefactList(afUsecaseList, self.trashusecaselistview, self.model.getUsecaseList(deleted=True), select_id)
        elif item_id == "TRASHTESTSUITES":
            self.ViewArtefactList(afTestsuiteList, self.trashtestsuitelistview, self.model.getTestsuiteList(deleted=True), select_id)
        elif item_id == "TRASH":
            self.ViewTrashInfo(self.model.getNumberOfDeletedArtefacts())

    
    def updateView(self, editresult, parent_id, item_id):
        """
        Update GUI view after editing an artefact

        This function is called if an artefact has been edited. Following
        actions are performed:
            - The tree in the left panel must be updated
            - If we started editing by activating the artefact in the tree
               we have to update the artefact view in the right panel
            - If we started editing by activating the artefact in a list
              (shown in the right panel), we have to show an updated list

        @type  editresult: nested tuple
        @param editresult: see return value of L{requestEditView}
        @type   parent_id: string
        @param  parent_id: Parent ID of artefact in left tree
        @type     item_id: integer
        @param    item_id: ID of artefact in left tree
        """
        (dlgResult, new_artefact, data, contentview) = editresult
        if dlgResult == wx.ID_CANCEL:
             return
        if new_artefact:
            # Update tree in left panel
            logging.debug("afeditor.updateView() (InitTree)")
            self.mainframe.AddItem(parent_id, data)
            logging.debug("afeditor.updateView() (InitTree done)")
            item_id = data['ID']
        else:
            # Update tree in left panel
            self.mainframe.treeCtrl.UpdateItemText(parent_id, item_id, data['title'])
        
        self.DisableOnSelChanged = True
        if self.currentview in self.listview:
            # Update artefact list in right panel
            logging.debug("afeditor.updateView() (1)")
            self.updateNodeView(None, parent_id, item_id)
            self.mainframe.treeCtrl.SetSelection(parent_id)
            pass
        else:
            # Update artefact view in right panel
            logging.debug("afeditor.updateView() (2)")
            self.updateNodeView(parent_id, item_id)
            self.mainframe.treeCtrl.SetSelection(parent_id, item_id)

        self.DisableOnSelChanged = False

        
    def getUsername(self):
        "Return the name of the current user"
        return afconfig.CURRENT_USER
    
    
    def getCurrentTimeStr(self):
        "Return current date and time as string"
        return time.strftime(afresource.TIME_FORMAT)


    def OnExit(self):
        self.config.Write("workdir", self.model.currentdir)
        
        
    def OnImport(self, evt):
        """
        Event handler for menu item 'Import'.
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        dlg = wx.FileDialog(
            self.mainframe, message = _("Import from product file"),
            defaultDir = self.model.currentdir,
            defaultFile = "",
            wildcard = self.wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            try:
                importer = _afimporter.afImporter(self.mainframe, self.model, path)
                importer.Run()
                self.InitView()
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), _('Error importing artefacts!'))


def main():
    import os, sys, getopt
    
    global arguments

    def version():
        print("$Rev$")

    def usage():
        print("Editor for Artefact Management System\nUsage:\n%s [-h|--help] [-V|--version] [-d |--debug] [<ifile>]\n"
        "  -h, --help     show help and exit\n"
        "  -V, --version  show version and exit\n"
        "  -d, --debug    enable debug output\n"
        "  <ifile>        database file"
        % sys.argv[0])

    logging.basicConfig(level=afconfig.loglevel, format=afconfig.logformat)
    logging.disable(afconfig.loglevel)
    
    try:
        opts, arguments = getopt.getopt(sys.argv[1:], "hdV", ["help", "debug", "version"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-V", "--version"):
            version()
            sys.exit()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--debug"):
            logging.disable(logging.NOTSET)
        else:
            assert False, "unhandled option"
    
    app = MyApp(redirect=False)
    app.MainLoop()

if __name__=="__main__":
    main()
