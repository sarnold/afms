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

"""
Test runner main application

@author: Achim Koehler
@version: $Rev: 75 $
"""

import os, sys, logging
import gettext
import wx
import trconfig
from _trmainframe import *
from _trnewtestrunwiz import *
from _trexectestrundlg import *
from _trinfotestrundlg import *
from _trcanceldlg import *
import trmodel
import afmodel, _afhelper
import trexporthtml, trexportxml
import afresource

class TestRunnerApp(wx.App):
    """
    wxWidgets main application class.
    """
    def OnInit(self):
        """Init method for wxWidgets"""
        # Read configuration an check for existence of workdir
        self.config = wx.FileConfig(appName="testrunner", vendorName="ka", localFilename="aftestrunner.cfg", globalFilename="aftestrunner.gfg", style=wx.CONFIG_USE_LOCAL_FILE|wx.CONFIG_USE_GLOBAL_FILE )
        sp = wx.StandardPaths.Get()
        workdir = self.config.Read("workdir", wx.StandardPaths.GetDocumentsDir(sp))
        if not os.path.exists(workdir):
             self.config.Write("workdir", wx.StandardPaths.GetDocumentsDir(sp))
        wx.Config.Set(self.config)
        
        self.model = trmodel.trModel()
        afresource.SetLanguage(self.config.Read("language", "en"))
        self.mainframe = MainFrame(None, "AF Test Runner")
        self.SetTopWindow(self.mainframe)
        self.mainframe.Show(True)
        
        self.Bind(wx.EVT_MENU, self.OnNewTestrun, id=101)
        self.Bind(wx.EVT_TOOL, self.OnNewTestrun, id=10)
        
        self.Bind(wx.EVT_MENU, self.OnOpenTestrun, id=102)
        self.Bind(wx.EVT_TOOL, self.OnOpenTestrun, id=11)
        self.Bind(wx.EVT_TOOL, self.OnRunTestcase, id=12)
        self.Bind(wx.EVT_MENU, self.OnRunTestcase, id=201)
        self.Bind(wx.EVT_MENU, self.OnShowTestrunInfo, id=202)
        self.Bind(wx.EVT_MENU, self.OnCancelTestrun, id=203)
        self.Bind(wx.EVT_MENU, self.OnExportHTML, id=103)
        self.Bind(wx.EVT_MENU, self.OnExportXML, id=104)
        
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGING, self.OnWizPageChanging)
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGED, self.OnWizPageChanged)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

        global arguments
        if len(arguments) > 0:
            self.OpenTestrun(arguments[0])

        return True
    
    
    def OnExit(self):
        """Write working directory to configuration when application exits"""
        self.config.Write("workdir", self.model.currentdir)


    def OnItemSelected(self, event):
        """Event handler for selection of an item in the test case list"""
        currentItem = self.mainframe.testcaselist.currentItem
        tc = self.mainframe.testcaselist.itemDataMap[currentItem]
        self.mainframe.testcaseview.InitContent(self.model.getTestcase(tc[0]))
        self.mainframe.testresultview.InitContent(self.model.getTestresult(tc[0]))
        self.mainframe.EnableRunCommand(tc[1] == afresource.PENDING)


    def OnItemActivated(self, evt):
        """Event handler for activation of an item in the tst case list"""
        currentItem = self.mainframe.testcaselist.currentItem
        tc = self.mainframe.testcaselist.itemDataMap[currentItem]
        if tc[1] != afresource.PENDING:
            wx.MessageBox(_("Test already has been executed!"), _("Oops ..."), wx.OK | wx.ICON_INFORMATION)
            return
        self.OnRunTestcase(None)
        
        
    def OnNewTestrun(self, evt):
        """
        Event handler for menu item or toolbar item 'New test run'.
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        self.wizard = NewTestrunWizard(self.mainframe)
        if not self.wizard.ShowModal(): return
        (afdatabase, ts_id, description, path) =  self.wizard.GetValue()
        self.wizard = None
        ##(afdatabase, ts_id, description, path) = ("aa.af", 1, ("D", "T"), "aa.tr")
        self.model.requestNewTestrun(path, afdatabase, ts_id, description)
        self.OpenTestrun(path)
        
        
    def OnOpenTestrun(self, evt):
        """
        Event handler for menu item or toolbar item 'Open test run'.
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        dlg = wx.FileDialog(
            self.mainframe, message = "Open test run file",
            defaultDir = self.model.currentdir,
            defaultFile = "",
            wildcard = afresource.TR_WILDCARD,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            try:
                self.OpenTestrun(path)
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), 'Error opening test run!')

        
    def OpenTestrun(self, path):
        """Actions to be performed when a test run is opened"""
        self.model.OpenTestrun(path)
        self.mainframe.SetStatusInfo(self.model.getStatusSummary(), path)
        self.mainframe.InitView(self.model.getTestcaseList())
        self.mainframe.GetMenuBar().Enable(202, True)
        self.mainframe.GetMenuBar().Enable(203, True)
        self.mainframe.GetMenuBar().Enable(103, True)
        self.mainframe.GetMenuBar().Enable(104, True)
        

    def OnShowTestrunInfo(self, evt):
        """Show dialog with information about the current test run"""
        dlg = InfoTestrunDialog(self.mainframe, self.model.getInfo())
        dlg.ShowModal()
        
        
    def OnWizPageChanging(self, evt):
        """Event handler for the 'New Test Run' wizard"""
        error = False
        action = None
        forwarddir = evt.GetDirection()
        page = evt.GetPage()
        if page.__class__ == SelectProductDatabasePage:
            filename = page.GetValue()
            if len(filename) <= 0:
                error = True
                msg = 'Please enter database name!'
                page.SetFocus()
            else:
                class noTestSuites(): pass
                try:
                    model = afmodel.afModel(None)
                    model.requestOpenProduct(filename)
                    testsuites = model.getTestsuiteList()
                    if len(testsuites) == 0: raise noTestSuites()
                    comboboxitems = [(testsuite[0], testsuite[1]) for testsuite in testsuites]
                    page.GetNext().SetValue(comboboxitems)
                except noTestSuites:
                    error = True
                    msg = 'Database contains no test suites!'
                    page.SetFocus()
                except:
                    logging.error(sys.exc_info())
                    error = True
                    msg = 'Could not open database or invalid database format!'
                    page.SetFocus()
                    
        elif page.__class__ == SelectOutputFilePage and forwarddir:
            filename = page.GetValue()
            if len(filename) <= 0:
                error = True
                msg = 'Please enter file name!'
                page.SetFocus()
            else:
                if os.path.exists(filename):
                    code = wx.MessageBox('File %s already exists.\nOkay to overwrite?' % filename, "Save test run", wx.YES_NO  | wx.ICON_WARNING)
                    print code
                    if code != wx.YES:
                        evt.Veto()
                        page.SetFocus()
                        return
                try:
                    fp = open(filename, "w")
                    fp.close()
                except IOError:
                    error = True
                    msg = 'Could not open file for writing!'
                    page.SetFocus()
                
        elif page.__class__ == EnterTestrunInfo and forwarddir:
            values = page.GetValue()
            if len(values[0]) <= 0:
                error = True
                msg = 'Test run description required!'
                page.SetFocus(0)
                
            elif len(values[1]) <= 0:
                error = True
                msg = 'Tester name required!'
                page.SetFocus(1)
                
        if error:
            wx.MessageBox(msg, 'Warning', wx.OK | wx.ICON_WARNING)
            evt.Veto()
            
            
    def OnWizPageChanged(self, evt):
        """Event handler for the 'New Test Run' wizard"""
        page = evt.GetPage()
        if page.__class__ != SelectOutputFilePage: return
        if len(page.GetValue()) > 0: return
        # provide an initial value for the output file
        if self.wizard is None: return
        (dbname, ts_id) = self.wizard.GetValue()[0:2]
        for cnt in range(1000):
            initialValue = "%s_ts%03d_%03d.tr" % (os.path.splitext(dbname)[0], ts_id, cnt)
            if not os.path.exists(initialValue):
                page.SetValue(initialValue)
                return;
        
        
    def OnRunTestcase(self,evt):
        """Event handler for 'Run test case'"""
        currentItem = self.mainframe.testcaselist.currentItem
        tc = self.mainframe.testcaselist.itemDataMap[currentItem]
        dlg = ExecTestrunDialog(self.mainframe.rightPanel, -1, "Run test case ID %s" % tc[0])
        dlg.testresultview.InitContent(self.model.getTestresult(tc[0]))
        result = dlg.ShowModal()
        if result == wx.ID_CANCEL: return
        testresult = dlg.testresultview.GetData()
        self.model.saveTestresult(int(tc[0]), testresult)
        self.mainframe.testresultview.InitContent(testresult)
        self.mainframe.SetStatusInfo(self.model.getStatusSummary())
        self.mainframe.EnableRunCommand(testresult[0] == afresource.PENDING)
        self.mainframe.testcaselist.UpdateItem(currentItem, testresult[0])
        

    def OnCancelTestrun(self, evt):
        """Handle cancellation of a test run"""
        dlg = CancelTestrunDialog(self.mainframe)
        if dlg.ShowModal() == wx.ID_OK:
            self.model.cancelTestrun(dlg.GetValue())
            self.mainframe.SetStatusInfo(self.model.getStatusSummary())
            self.mainframe.InitView(self.model.getTestcaseList())
        dlg.Destroy()
        
        
    def OnExportHTML(self, evt):
        dlg = wx.FileDialog(
            self.mainframe, message = "Save HTML to file",
            defaultDir = self.model.currentdir,
            defaultFile = os.path.splitext(self.model.getFilename())[0] + ".html",
            wildcard = afresource.HTML_WILDCARD,
            style=wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            try:
                trexporthtml.trExportHTML(path, self.model)
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), 'Error exporting to HTML!')


    def OnExportXML(self, evt):
        dlg = wx.FileDialog(
            self.mainframe, message = "Save XML to file",
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
            try:
                trexportxml.trExportXML(path, self.model)
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), 'Error exporting to XML!')


def main():
    import os, sys, getopt
    
    global arguments

    def version():
        print("$Rev$")

    def usage():
        print("Test runner for Artefact Management System\nUsage:\n%s [-h|--help] [-V|--version] [-d |--debug]\n"
        "  -h, --help     show help and exit\n"
        "  -V, --version  show version and exit\n"
        "  -d, --debug    enable debug output"
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


    app = TestRunnerApp(redirect=False)

    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    localedir = basepath
    domain = "messages"
    langid = wx.LANGUAGE_DEFAULT
    mylocale = wx.Locale(langid)
    mylocale.AddCatalogLookupPathPrefix(localedir)
    mylocale.AddCatalog(domain)
    _ = wx.GetTranslation

    app.MainLoop()

if __name__=="__main__":
    main()