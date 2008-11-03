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
Test runner main application

@author: Achim Koehler
@version: $Rev$
"""

import os, sys, logging, time
import gettext
import wx

basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
LOCALEDIR = os.path.join(basepath, 'locale')
DOMAIN = "afms"
gettext.install(DOMAIN, LOCALEDIR, unicode=True)

import trconfig
from _trmainframe import *
from _trnewtestrunwiz import *
from _trexectestrundlg import *
import _trbatchrundlg
from _trinfotestrundlg import *
from _trcanceldlg import *
import trmodel
import afmodel, _afhelper
import trexporthtml, trexportxml
import afresource


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, callback):
        wx.FileDropTarget.__init__(self)
        self.callback = callback


    def OnDropFiles(self, x, y, filenames):
        if len(filenames) > 1: return False
        self.callback(filenames[0])


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
        cssfile = self.config.Read('cssfile', afresource.getDefaultTrCSSFile())
        self.config.Write('cssfile', cssfile)
        xslfile = self.config.Read('xslfile', afresource.getDefaultTrXSLFile())
        self.config.Write('xslfile', xslfile)

        wx.Config.Set(self.config)

        self.model = trmodel.trModel()

        # Setup language stuff
        language = self.config.Read("language", 'en')
        afresource.SetLanguage(language)
        wxLanguage = {'de' : wx.LANGUAGE_GERMAN, 'en' : wx.LANGUAGE_ENGLISH}
        try:
            self.wxLanguageCode = wxLanguage[language]
        except KeyError:
            logging.debug('TestrunnerApp.OnInit(), language %s unknown' % language)
            self.wxLanguageCode = wx.LANGUAGE_DEFAULT

        try:
            t = gettext.translation(DOMAIN, LOCALEDIR, languages=[language])
            t.install(unicode=True)
        except IOError:
            logging.debug('TestrunnerApp.OnInit(), gettext.translation() failed for language %s' % language)
            pass

        self.mainframe = MainFrame(None, "AF Test Runner")
        dt = FileDropTarget(self.OpenTestrun)
        self.mainframe.leftWindow.SetDropTarget(dt)

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
        self.Bind(wx.EVT_MENU, self.OnRunScripted, id=204)
        self.Bind(wx.EVT_MENU, self.OnExportHTML, id=103)
        self.Bind(wx.EVT_MENU, self.OnExportXML, id=104)
        self.Bind(wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)

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
        testcase = self.model.getTestcase(tc['ID'])
        self.mainframe.testcaseview.InitContent(testcase)
        self.mainframe.testresultview.InitContent(testcase)
        self.mainframe.EnableRunCommand(tc['testresult'] == afresource.PENDING)


    def OnItemActivated(self, evt):
        """Event handler for activation of an item in the tst case list"""
        currentItem = self.mainframe.testcaselist.currentItem
        tc = self.mainframe.testcaselist.itemDataMap[currentItem]
        if tc['testresult'] != afresource.PENDING:
            wx.MessageBox(_("Test already has been executed!"), _("Oops ..."), wx.OK | wx.ICON_INFORMATION)
            return
        self.OnRunTestcase(None)


    def OnNewTestrun(self, evt):
        """
        Event handler for menu item or toolbar item 'New test run'.
        @type  evt: wx.CommandEvent
        @param evt: event data
        """
        config = {'lastafdir': self.config.Read('lastafdir', '.')}
        self.wizard = NewTestrunWizard(self.mainframe, config)
        if not self.wizard.ShowModal(): return
        (afdatabase, ts_id, description, path) =  self.wizard.GetValue()
        self.wizard = None
        self.model.requestNewTestrun(path, afdatabase, ts_id, description)
        self.OpenTestrun(path)
        self.config.Write('lastafdir', os.path.dirname(afdatabase))


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
            wildcard = _(afresource.TR_WILDCARD),
            style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            self.OpenTestrun(path)


    def OpenTestrun(self, path):
        """Actions to be performed when a test run is opened"""
        try:
            self.model.OpenTestrun(path)
            self.mainframe.filehistory.AddFileToHistory(path)
            self.mainframe.SetStatusInfo(self.model.getStatusSummary(), path)
            self.mainframe.InitView(self.model.getTestcaseOverviewList())
            self.mainframe.GetMenuBar().Enable(202, True)
            self.mainframe.GetMenuBar().Enable(203, True)
            self.mainframe.GetMenuBar().Enable(204, True)
            self.mainframe.GetMenuBar().Enable(103, True)
            self.mainframe.GetMenuBar().Enable(104, True)
        except:
            _afhelper.ExceptionMessageBox(sys.exc_info(), 'Error opening test run!')


    def OnFileHistory(self, evt):
        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.mainframe.filehistory.GetHistoryFile(fileNum)
        try:
            self.OpenTestrun(path)
            # add it back to the history so it will be moved up the list
            self.mainframe.filehistory.AddFileToHistory(path)
        except:
            _afhelper.ExceptionMessageBox(sys.exc_info(), _('Error opening product!'))
            self.mainframe.filehistory.RemoveFileFromHistory(fileNum)


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
                    comboboxitems = [(testsuite['ID'], testsuite['title']) for testsuite in testsuites]
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
        dlg = ExecTestrunDialog(self.mainframe, -1, _("Run test case ID %s") % tc['ID'])
        testcase = self.model.getTestcase(tc['ID'])
        dlg.testresultview.InitContent(testcase)
        dlg.testcaseview.InitContent(testcase)
        result = dlg.ShowModal()
        if result == wx.ID_CANCEL: return
        testresult = dlg.testresultview.GetData()
        self.model.saveTestresult(testresult)
        self.mainframe.testresultview.InitContent(testresult)
        self.mainframe.SetStatusInfo(self.model.getStatusSummary())
        self.mainframe.EnableRunCommand(testresult['testresult'] == afresource.PENDING)
        self.mainframe.testcaselist.UpdateItem(currentItem, testresult['testresult'])


    def OnCancelTestrun(self, evt):
        """Handle cancellation of a test run"""
        dlg = CancelTestrunDialog(self.mainframe)
        if dlg.ShowModal() == wx.ID_OK:
            self.model.cancelTestrun(dlg.GetValue())
            self.mainframe.SetStatusInfo(self.model.getStatusSummary())
            self.mainframe.InitView(self.model.getTestcaseOverviewList())
        dlg.Destroy()


    def OnExportHTML(self, evt):
        dlg = wx.FileDialog(
            self.mainframe, message = "Save HTML to file",
            defaultDir = self.model.currentdir,
            defaultFile = os.path.splitext(self.model.getFilename())[0] + ".html",
            wildcard = _(afresource.HTML_WILDCARD),
            style=wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            try:
                stylesheet = self.config.Read('cssfile', afresource.getDefaultTrCSSFile())
                trexporthtml.doExportHTML(path, self.model, stylesheet)
                openhtmlreport = self.config.ReadBool('autoopenhtmlreport', False)
                if openhtmlreport:
                    webbrowser.open(url=path, new=2)
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), 'Error exporting to HTML!')


    def OnExportXML(self, evt):
        dlg = wx.FileDialog(
            self.mainframe, message = "Save XML to file",
            defaultDir = self.model.currentdir,
            defaultFile = os.path.splitext(self.model.getFilename())[0] + ".xml",
            wildcard = _(afresource.XML_WILDCARD),
            style=wx.SAVE | wx.CHANGE_DIR | wx.OVERWRITE_PROMPT
            )
        dlgResult = dlg.ShowModal()
        if  dlgResult == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult == wx.ID_OK:
            try:
                stylesheet = self.config.Read('xslfile', afresource.getDefaultTrXSLFile())
                trexportxml.doExportXML(path, self.model, stylesheet)
                openxmlreport = self.config.ReadBool('autoopenxmlreport', False)
                if openxmlreport:
                    webbrowser.open(url=path, new=2)
            except:
                _afhelper.ExceptionMessageBox(sys.exc_info(), 'Error exporting to XML!')


    def OnRunScripted(self, evt):
        dlg = _trbatchrundlg.BatchTestrunDialog(self.mainframe, wx.ID_ANY, _('Select testcases to run'))
        testcaselist = self.model.getTestcaseScriptedList()
        if len(testcaselist) <= 0:
            wx.MessageBox(_('No testcases with scripts found.'), _('Error'), wx.OK | wx.ICON_HAND)
            return
        dlg.testcaselist.InitCheckableContent([], testcaselist)
        result = dlg.ShowModal()
        if result != wx.ID_OK: return
        # Get ID of all checked items
        idlist = dlg.testcaselist.GetItemIDByCheckState()[0]
        execorder = self.model.getTestsuiteExecOrder()
        if len(execorder) > 0:
            execorder = map(int, execorder.split(','))
            if len(execorder) == len(idlist):
                idlist = execorder
            else:
                answer = wx.MessageBox(_('Execution order will be ignored!\nProceed anyway?'), _('Warning'), wx.YES_NO |wx.ICON_QUESTION )
                if answer != wx.YES: return
        for id in idlist:
            testcase = self.model.getTestcase(id)
            logging.debug('ID=%d, execScript(%s)' % (id, testcase['scripturl']))
            (returncode, message) = execScript(testcase['scripturl'], dryrun=False)
            testcase['testremark'] = message
            testcase['timestamp'] = time.strftime(afresource.TIME_FORMAT)
            if returncode == 0:
                testcase['testresult'] = 1
            else:
                testcase['testresult'] = 0
                testcase['action'] = _('None (batch run)')
            self.model.saveTestresult(testcase)
        self.mainframe.testcaselist.InitContent(self.model.getTestcaseOverviewList())
        self.mainframe.SetStatusInfo(self.model.getStatusSummary())


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
    # Hmmm... If wxLocale is called in app.OnInit() it does not work. Why?
    mylocale = wx.Locale(app.wxLanguageCode)
    app.MainLoop()

if __name__=="__main__":
    main()
