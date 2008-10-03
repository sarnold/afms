# test.py
# -*- coding: utf-8 -*-

import time
import subprocess, os.path, sys

import pywinauto
from pywinauto import application
from pywinauto.controls.win32_controls import EditWrapper
from pywinauto.timings import Timings


EXECUTABLE = r"../afeditor.py"
TESTDIR = 'testdir'
TESTFILE = 'test.af'
workdir = os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
testdbdir = os.path.join(os.getcwd(), TESTDIR)
testdbfile = os.path.join(os.getcwd(), TESTDIR, TESTFILE)


class afTestHelper(object):
    
    def execApplication(self, applicationpath):
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        process = subprocess.Popen(sys.executable + ' ' + applicationpath, stdout=stdout, stderr=stderr)
        return process
    
    
class afEditorTestHelper(afTestHelper):

    def __init__(self, applicationpath, delay=1.0):
        self.process = self.execApplication(applicationpath)
        self.app = application.Application()
        cnt = 0
        while True:
            try:
                self.app.connect_(title_re='AF Editor')
                break
            except pywinauto.findwindows.WindowNotFoundError:
                if cnt < 15:
                    time.sleep(1.0)
                else:
                    raise
            cnt = cnt + 1
        self.delay = delay
        self.initTimings()
        self.afeditor = self.app.window_(process = self.process.pid)
        self.treeview = self.afeditor['TreeView']
        
        
    def initTimings(self):
        Timings.window_find_timeout = 10
        Timings.app_start_timeout = 10
        Timings.exists_timeout = 5
        Timings.after_click_wait = .1
        Timings.after_clickinput_wait = .01
        Timings.after_menu_wait = .05
        Timings.after_sendkeys_key_wait = .01
        Timings.after_button_click_wait = 0
        Timings.before_closeclick_wait = 0.1
        Timings.closeclick_dialog_close_wait = 1.0
        Timings.after_closeclick_wait = 1.0
        Timings.after_windowclose_timeout = 2
        Timings.after_setfocus_wait = .06
        Timings.after_setcursorpos_wait = .01
        Timings.sendmessagetimeout_timeout = .001
        Timings.after_tabselect_wait = 1
        Timings.after_listviewselect_wait = .01
        Timings.after_listviewcheck_wait = .001
        Timings.after_treeviewselect_wait = .001
        Timings.after_toobarpressbutton_wait = .01
        Timings.after_updownchange_wait = .001
        Timings.after_movewindow_wait = 0
        Timings.after_buttoncheck_wait = 0
        Timings.after_comboboxselect_wait = 0
        Timings.after_listboxselect_wait = 0
        Timings.after_listboxfocuschange_wait = 0
        Timings.after_editsetedittext_wait = 0
        Timings.after_editselect_wait = 0


    def addTextSection(self, **kwargs):
        self.afeditor.MenuSelect("New -> New text section ...")
        editwin = self.app['Edit section']
        editwin['Title:Edit'].SetText(kwargs['title'])
        editwin['Content:RICHEDIT50W'].SetText(kwargs['content'])
        editwin['Save'].CloseClick()
    
    
    def getTextSection(self, n=5):
        for i in range(n):
            yield({'title'   : 'Section title %03d' % i,
                   'content' : '.. REST\n\nContent of text section %3d\n' % i})
        
        
    def addTextSections(self, n = 5):
        for ts in self.getTextSection(5):
            self.addTextSection(**ts)
            time.sleep(self.delay)
        
    
    def addGlossaryEntry(self, **kwargs):
        self.afeditor.MenuSelect("New -> New glossary entry ...")
        editwin = self.app['Edit glossary entry']
        editwin['Term:Edit'].SetText(kwargs['term'])
        editwin['Description:RICHEDIT50W'].SetText(kwargs['description'])
        editwin['Save'].CloseClick()
        
    
    def getGlossaryEntry(self, n=5):
        for i in range(n):
            yield({'term'        : 'Glossary term %03d' % i,
                   'description' : '.. REST\n\nDescription of glossary term %3d\n' % i})

        
    def addGlossaryEntries(self, n = 5):
        for ge in self.getGlossaryEntry(5):
            self.addGlossaryEntry(**ge)
            time.sleep(self.delay)


    def addFeature(self, **kwargs):
        self.afeditor.MenuSelect("New -> New feature ...")
        editwin = self.app['Edit feature']
        editwin['Title:Edit'].SetText(kwargs['title'])
        editwin['Description:RICHEDIT50W'].SetText(kwargs['description'])
        editwin['Key:Edit'].SetText(kwargs['key'])
        editwin['Priority:ComboBox'].Select(kwargs['priority'])
        editwin['Status:ComboBox'].Select(kwargs['status'])
        editwin['Risk:ComboBox'].Select(kwargs['risk'])
        editwin['Save'].CloseClick()
        
    
    def getFeature(self):
        priority = (0, 1, 2, 3, 0)
        status   = (2, 1, 0, 2, 1)
        risk     = (4, 3, 2, 1, 0)
        for i in range(len(priority)):
            yield({'title'       : 'Feature title %03d' % i, 
                   'description' : '.. REST\n\nDescription of feature %03d\n' % i, 
                   'key'         : 'Key of feature %03d' % i, 
                   'priority'    : priority[i], 
                   'status'      : status[i],
                   'risk'        : risk[i]})
        
        
    def addFeatures(self):
        for ft in self.getFeature():
            self.addFeature(**ft)
            time.sleep(self.delay)
            

    def addRequirement(self, **kwargs):
        self.afeditor.MenuSelect("New -> New requirement ...")
        editwin = self.app['Edit requirement']
        editwin['Title:Edit'].SetText(kwargs['title'])
        editwin['Description:RICHEDIT50W'].SetText(kwargs['description'])
        editwin['Key:Edit'].SetText(kwargs['key'])
        editwin['Priority:ComboBox'].Select(kwargs['priority'])
        editwin['Status:ComboBox'].Select(kwargs['status'])
        editwin['Complexity:ComboBox'].Select(kwargs['complexity'])
        editwin['Assigned:Edit'].SetText(kwargs['assigned'])
        editwin['Effort:ComboBox'].Select(kwargs['effort'])
        editwin['Category:ComboBox'].Select(kwargs['category'])
        editwin.TypeKeys('^{TAB}')
        editwin['Origin:RICHEDIT50W'].SetText(kwargs['origin'])
        editwin['Rationale:RICHEDIT50W'].SetText(kwargs['rationale'])
        editwin['Save'].CloseClick()
        
    
    def getRequirement(self):
        priority   = (0, 1, 2, 3, 0, 1, 2, 3, 0, 1,  2,  3,  0,  1,  2,  3,  0)
        status     = (2, 1, 0, 2, 1, 0, 2, 1, 0, 2,  1,  0,  2,  1,  0,  2,  1)
        complexity = (1, 2, 0, 1, 2, 0, 1, 2, 0, 1,  2,  0,  1,  2,  0,  1,  2)
        effort     = (3, 2, 1, 0, 3, 2, 1, 0, 3, 2,  1,  0,  3,  2,  1,  0,  3)
        category   = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
        for i in range(len(category)):
            data = {
                'title'       : 'Requirement title %03d' % i,
                'description' : '.. HTML\n\nDescription of requirement %03d\n' % i,
                'key'         : 'Key of requirement %03d' % i, 
                'priority'    : priority[i],
                'status'      : status[i],
                'complexity'  : complexity[i],
                'assigned'    : 'Assignee %03d' % i,
                'effort'      : effort[i],
                'category'    : category[i],
                'origin'      : 'Requirement origin %03d' % i,
                'rationale'   : '.. HTML\n\nRequirement rationale <b>%03d</b>\n' % i,
                'priority'    : priority[i],
                'status'      : status[i],
                'complexity'  : complexity[i],
                'effort'      : effort[i],
                'category'    : category[i]}
            yield(data)
        
        
    def addRequirements(self):
        for r in self.getRequirement():
            self.addRequirement(**r)
            time.sleep(self.delay)
            
            
    def editProduct(self, title, description):
        self.treeview.Select((0,))
        self.treeview.TypeKeys('{ENTER}')
        editproductwin = self.app['Edit Product']
        editproductwin['Title:Edit'].SetText(title)
        editproductwin['Description:RICHEDIT50W'].SetEditText(description)
        editproductwin['Save'].CloseClick()
        self.treeview.Select((0,))

    
    def newProduct(self, filename):
        self.afeditor.MenuSelect("File -> New product ...")
        savedlg = self.app['Save new product to file']
        savedlg.FileNameEdit.SetEditText(filename)
        savedlg.SpeichernButton.CloseClick()
        time.sleep(self.delay)
        
        
    def openProduct(self, filename):
        self.afeditor.MenuSelect("File -> Open product ...")
        dlg = self.app['Open product file']
        dlg.FileNameEdit.SetEditText(filename)
        dlg[u'Ö&ffnenButton'].CloseClick()
        
        
    def readArtefactList(self, coltypes):
        nrows = self.afeditor.leftwinListView.ItemCount()
        for r in range(nrows):
            item = {}
            for c, coltype in zip(range(len(coltypes)), coltypes):
                data = self.afeditor.leftwinListView.GetItem(r,c)['text']
                item[coltype['key']] =  coltype['type'](data)
            yield(item)
            
            
    def count(self, start=0, incr=1):
        cnt = start-incr
        while(True):
            cnt = cnt + incr
            yield(cnt)

        
    def exitApp(self):
        self.afeditor.Close()

