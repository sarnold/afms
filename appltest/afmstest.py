# test.py
# -*- coding: utf-8 -*-

import time
import subprocess, os.path, sys

import pywinauto
from pywinauto import application, clipboard
from pywinauto.controls.win32_controls import EditWrapper
from pywinauto.timings import Timings
import pywinauto.timings as timing

EXECUTABLE = r"../afeditor.py"
TESTDIR = 'testdir'
TESTFILE = 'test.af'
workdir = os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
testdbdir = os.path.join(os.getcwd(), TESTDIR)
testdbfile = os.path.join(os.getcwd(), TESTDIR, TESTFILE)


class afTestHelper(object):
    """Base helper class for testing afms applications"""    

    def execApplication(self, applicationpath):
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        process = subprocess.Popen(sys.executable + ' ' + applicationpath, stdout=stdout, stderr=stderr)
        return process
    
    
class afEditorTestHelper(afTestHelper):
    """Helper class for testing afeditor application"""

    def __init__(self, applicationpath, delay=1.0):
        self.process = self.execApplication(applicationpath)
        self.app = application.Application()
        
        def connect():
            self.app.connect_(title_re='AF Editor')
            
        timing.WaitUntilPasses(10, 0.5, connect, pywinauto.findwindows.WindowNotFoundError)
        self.delay = delay
        self.initTimings()
        self.afeditorwin = self.app.window_(process = self.process.pid)
        self.treeview = self.afeditorwin['TreeView']
        self.afeditor  = self.afeditorwin.WrapperObject()
        
        
    def initTimings(self):
        Timings.window_find_timeout = 10
        Timings.app_start_timeout = 10
        Timings.exists_timeout = 5
        Timings.after_click_wait = .5
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
        Timings.after_treeviewselect_wait = 0.5
        Timings.after_toobarpressbutton_wait = .01
        Timings.after_updownchange_wait = .001
        Timings.after_movewindow_wait = 0
        Timings.after_buttoncheck_wait = 0
        Timings.after_comboboxselect_wait = 0
        Timings.after_listboxselect_wait = 0
        Timings.after_listboxfocuschange_wait = 0
        Timings.after_editsetedittext_wait = 0
        Timings.after_editselect_wait = 0
        Timings.Slow()
        
        
    def setTiming(self, speed):
        if speed.lower() == 'slow':
            Timings.Slow()
        elif speed.lower() == 'fast':
            Timings.Fast()
        else:
            Timings.Defaults()


    def addTextSection(self, **kwargs):
        timing.WaitUntil(10, 1, self.afeditor.IsEnabled)
        self.afeditor.MenuSelect("New -> New text section ...")
        editwin = self.app['Edit section']
        editwin['Title:Edit'].SetText(kwargs['title'])
        editwin['Content:RICHEDIT50W'].SetText(kwargs['content'])
        editwin['Save'].Click()

    
    def getTextSection(self, n=5):
        for i in range(n):
            yield({'title'    : u'Section title %03d (ÄÖÜäöüß)' % i,
                   'content'  : u'.. REST\n\nContent of text section %03d (ÄÖÜäöüß)\n' % i,
                   'r_content': u'\nContent of text section %03d (ÄÖÜäöüß) ' % i,
                   'level'    : i+1,
                   'id'       : i+1 })
        
        
    def addTextSections(self, n = 5):
        for ts in self.getTextSection(5):
            self.addTextSection(**ts)
            ##time.sleep(self.delay)
        
    
    def addGlossaryEntry(self, **kwargs):
        timing.WaitUntil(10, 1, self.afeditor.IsEnabled)
        self.afeditor.MenuSelect("New -> New glossary entry ...")
        editwin = self.app['Edit glossary entry']
        editwin['Term:Edit'].SetText(kwargs['term'])
        editwin['Description:RICHEDIT50W'].SetText(kwargs['description'])
        editwin['Save'].Click()
        
    
    def getGlossaryEntry(self, n=5):
        for i in range(n):
            yield({'term'          : u'Glossary term %03d (ÄÖÜäöüß)' % i,
                   'description'   : u'.. REST\n\nDescription of glossary term %03d (ÄÖÜäöüß)\n' % i,
                   'r_description' : u'\nDescription of glossary term %03d (ÄÖÜäöüß) ' % i})

        
    def addGlossaryEntries(self, n = 5):
        for ge in self.getGlossaryEntry(5):
            self.addGlossaryEntry(**ge)
            ##time.sleep(self.delay)


    def addFeature(self, **kwargs):
        timing.WaitUntil(10, 1, self.afeditor.IsEnabled)
        self.afeditor.MenuSelect("New -> New feature ...")
        editwin = self.app['Edit feature']
        editwin['Title:Edit'].SetText(kwargs['title'])
        editwin['Description:RICHEDIT50W'].SetText(kwargs['description'])
        editwin['Key:Edit'].SetText(kwargs['key'])
        editwin['Priority:ComboBox'].Select(kwargs['priority'])
        editwin['Status:ComboBox'].Select(kwargs['status'])
        editwin['Risk:ComboBox'].Select(kwargs['risk'])
        editwin['Save'].Click()
        
    
    def getFeature(self):
        priority = (0, 1, 2, 3, 0)
        status   = (2, 1, 0, 2, 1)
        risk     = (4, 3, 2, 1, 0)
        related_requirements = ((5,), (), (2,3), (), ())
        related_usecases     = ((), (2,), (), (), (4,)) 
        for i in range(len(priority)):
            yield({'title'         : u'Feature title %03d (ÄÖÜäöüß)' % i, 
                   'description'   : u'.. REST\n\nDescription of feature %03d (ÄÖÜäöüß)\n' % i,
                   'r_description' : u'\nDescription of feature %03d (ÄÖÜäöüß) ' % i,
                   'key'           : u'Key of feature %03d (ÄÖÜäöüß)' % i, 
                   'priority'      : priority[i], 
                   'status'        : status[i],
                   'risk'          : risk[i],
                   'related_requirements' : related_requirements[i],
                   'related_usecases'     :  related_usecases[i]})
        
        
    def addFeatures(self):
        for ft in self.getFeature():
            self.addFeature(**ft)
            ##time.sleep(self.delay)
            

    def addRequirement(self, **kwargs):
        timing.WaitUntil(10, 1, self.afeditor.IsEnabled)
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
        editwin.TypeKeys('^+{TAB}')
        editwin['Save'].Click()
        
    
    def getRequirement(self):
        priority   = (0, 1, 2, 3, 0, 1, 2, 3, 0, 1,  2,  3,  0,  1,  2,  3,  0)
        status     = (2, 1, 0, 2, 1, 0, 2, 1, 0, 2,  1,  0,  2,  1,  0,  2,  1)
        complexity = (1, 2, 0, 1, 2, 0, 1, 2, 0, 1,  2,  0,  1,  2,  0,  1,  2)
        effort     = (3, 2, 1, 0, 3, 2, 1, 0, 3, 2,  1,  0,  3,  2,  1,  0,  3)
        category   = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
        related_requirements = ((), (),   (),    (), (),   (), (), (), (), (),   (), (), (), (), (), (), ())
        related_features     = ((), (3,), (3,),  (), (1,), (), (), (), (), (),   (), (), (), (), (), (), ())
        related_usecases     = ((), (3,), (),    (), (),   (), (), (), (), (5,), (), (), (), (), (), (), ())
        related_testcases    = ((2,), (), (3,4), (), (),   (), (), (), (), (),   (), (), (), (), (), (), (5,))
        for i in range(len(category)):
            data = {
                'title'         : u'Requirement title %03d (ÄÖÜäöüß)' % i,
                'description'   : u'.. HTML\n\nDescription of requirement %03d (ÄÖÜäöüß)\n' % i,
                'r_description' : u'Description of requirement %03d (ÄÖÜäöüß)' % i,
                'key'           : u'Key of requirement %03d (ÄÖÜäöüß)' % i, 
                'priority'      : priority[i],
                'status'        : status[i],
                'complexity'    : complexity[i],
                'assigned'      : u'Assignee %03d (ÄÖÜäöüß)' % i,
                'effort'        : effort[i],
                'category'      : category[i],
                'origin'        : u'Requirement origin %03d (ÄÖÜäöüß)' % i,
                'rationale'     : u'.. HTML\n\nRequirement rationale <b>%03d (ÄÖÜäöüß)</b>\n' % i,
                'r_rationale'   : u'Requirement rationale %03d (ÄÖÜäöüß)' % i,
                'priority'      : priority[i],
                'status'        : status[i],
                'complexity'    : complexity[i],
                'effort'        : effort[i],
                'category'      : category[i],
                'related_features'     : related_features[i],
                'related_requirements' : related_requirements[i],
                'related_usecases'     : related_usecases[i],
                'related_testcases'    : related_testcases[i]}
            yield(data)
                    
        
    def addRequirements(self):
        for r in self.getRequirement():
            if len(r['related_features']) != 0:
                fpos = r['related_features'][0]-1
                # select feature in treeview at fpos
                i = (0, 2, fpos)
            else:
                # don't select any feature in treeview 
                i = (0, 3)
            self.treeview.Select(i)
            self.addRequirement(**r)
            ##time.sleep(self.delay)
        
            
    def editProduct(self, title, description):
        self.treeview.Select((0,))
        self.treeview.TypeKeys('{ENTER}')
        editproductwin = self.app['Edit Product']
        editproductwin['Title:Edit'].SetText(title)
        editproductwin['Description:RICHEDIT50W'].SetEditText(description)
        editproductwin['Save'].Click()
        self.treeview.Select((0,))
        
    
    def addUsecase(self, **kwargs):
        timing.WaitUntil(10, 1, self.afeditor.IsEnabled)
        self.afeditor.MenuSelect("New -> New usecase ...")
        editwin = self.app['Edit usecase']
        editwin['Summary:Edit'].SetText(kwargs['summary'])
        editwin['Priority:ComboBox'].Select(kwargs['priority'])
        editwin['Use frequency:ComboBox'].Select(kwargs['usefrequency'])
        editwin['Actors:Edit'].SetText(kwargs['actors'])
        editwin['Stakeholders:Edit'].SetText(kwargs['stakeholders'])
        editwin['Prerequisites:Edit'].SetText(kwargs['prerequisites'])
        editwin['Main scenario:Edit'].SetText(kwargs['mainscenario'])
        editwin['Alt scenario:Edit'].SetText(kwargs['altscenario'])
        editwin['Notes:Edit'].SetText(kwargs['notes'])
        editwin['Save'].Click()
        
    
    def getUsecase(self):
        priority     = (3, 2, 1, 0, 3)
        usefrequency = (0, 1, 2, 3, 4)
        related_requirements = ((), (),   (2,), (),   (10,))
        related_features     = ((), (2,), (),   (5,), ())
        for i in range(len(usefrequency)):
            data = {'summary'         : u"Usecase summary %03d (ÄÖÜäöüß)" % i, 
                    'priority'        : priority[i],
                    'usefrequency'    : usefrequency[i],
                    'actors'          : u"Usecase actor %03d (ÄÖÜäöüß)" %i,
                    'stakeholders'    : u"Usecase stakeholders %03d (ÄÖÜäöüß)" %i,
                    'prerequisites'   : u"Usecase prerequisites %03d (ÄÖÜäöüß)" %i,
                    'mainscenario'    : u"Usecase mainscenario %03d (ÄÖÜäöüß)" %i,
                    'altscenario'     : u"Usecase altscenario %03d (ÄÖÜäöüß)" %i,
                    'notes'           : u"Usecase notes %03d (ÄÖÜäöüß)" %i,
                    'r_prerequisites' : u"\nUsecase prerequisites %03d (ÄÖÜäöüß)" %i,
                    'r_mainscenario'  : u"\nUsecase mainscenario %03d (ÄÖÜäöüß)" %i,
                    'r_altscenario'   : u"\nUsecase altscenario %03d (ÄÖÜäöüß)" %i,
                    'r_notes'         : u"\nUsecase notes %03d (ÄÖÜäöüß)" %i,
                    'related_features'     : related_features[i],
                    'related_requirements' : related_requirements[i]} 
            yield(data)
                

    def addUsecases(self):
        self.treeview.Select((0, 4))
        for uc in self.getUsecase():
            if len(uc['related_features']) == 0:
                fpos = -1
            else:
                fpos = uc['related_features'][0]-1
            if len(uc['related_requirements']) == 0:
                rpos = -1
            else:
                rpos = uc['related_requirements'][0]-1
            if fpos < 0 and rpos < 0:
                self.treeview.Select((0,))
            elif fpos > 0:
                self.treeview.Select((0,2))
                self.afeditorwin.leftwinListView.Select(fpos)
            else:
                self.treeview.Select((0,3))
                self.afeditorwin.leftwinListView.Select(rpos)
            self.addUsecase(**uc)


    def addTestcase(self, **kwargs):
        timing.WaitUntil(10, 1, self.afeditor.IsEnabled)
        self.afeditor.MenuSelect("New -> New testcase ...")
        editwin = self.app['Edit testcase']
        editwin['Title:Edit'].SetText(kwargs['title'])
        editwin['Key:Edit'].SetText(kwargs['key'])
        editwin['Purpose:Edit'].SetText(kwargs['purpose'])
        editwin['Prerequisite:Edit'].SetText(kwargs['prerequisite'])
        editwin['Testdata:Edit'].SetText(kwargs['testdata'])
        editwin['Steps:Edit'].SetText(kwargs['steps'])
        editwin['Script:Edit'].SetText(kwargs['script'])
        editwin['Notes && Questions:Edit'].SetText(kwargs['notes'])
        editwin['Save'].Click()
        
    
    def getTestcase(self):
        related_requirements = ((),    (1,),  (3,),  (3, ), (17,), ())
        related_testsuites   = ((1,3), (1,3), (1,3), (2,),  (2,3), ())
        for i in range(6):
            data = {'title'          : u"Testcase title %03d (ÄÖÜäöüß)" % i, 
                    'key'            : u"Testcase key %03d (ÄÖÜäöüß)" %i,
                    'purpose'        : u"Testcase purpose %03d (ÄÖÜäöüß)" %i,
                    'prerequisite'   : u"Testcase prerequisite %03d (ÄÖÜäöüß)" %i,
                    'testdata'       : u"Testcase testdata %03d (ÄÖÜäöüß)" %i,
                    'steps'          : u"Testcase steps %03d (ÄÖÜäöüß)" %i,
                    'script'         : u"samplescript.cmd %03d" %i,
                    'notes'          : u"Testcase notes %03d (ÄÖÜäöüß)" %i, 
                    'r_purpose'      : u"\nTestcase purpose %03d (ÄÖÜäöüß)" %i,
                    'r_prerequisite' : u"\nTestcase prerequisite %03d (ÄÖÜäöüß)" %i,
                    'r_testdata'     : u"\nTestcase testdata %03d (ÄÖÜäöüß)" %i,
                    'r_steps'        : u"\nTestcase steps %03d (ÄÖÜäöüß)" %i,
                    'r_notes'        : u"\nTestcase notes %03d (ÄÖÜäöüß)" %i,
                    'related_requirements' : related_requirements[i],
                    'related_testsuites'   : related_testsuites[i] }                      
            yield(data)
    
    
    def addTestcases(self):
        for tc in self.getTestcase():
            if len(tc['related_requirements']) == 0:
                self.treeview.Select((0,))
            else:
                rpos = tc['related_requirements'][0]-1
                self.treeview.Select((0,3))
                self.afeditorwin.leftwinListView.Select(rpos)
            self.addTestcase(**tc)


    def addTestsuite(self, **kwargs):
        timing.WaitUntil(10, 1, self.afeditor.IsEnabled)
        self.afeditor.MenuSelect("New -> New testsuite ...")
        editwin = self.app['Edit testsuite']
        editwin['Title:Edit'].SetText(kwargs['title'])
        editwin['Description:Edit'].SetText(kwargs['description'])
        editwin["Execution order ID's:Edit"].SetText(kwargs['execorder'])
        testcaselistview = editwin['Testcases:ListView']
        for tcpos in kwargs['testcasepos']:
            testcaselistview.Select(tcpos)
            testcaselistview.TypeKeys('{SPACE}')
        editwin['Save'].Click()
        
    
    def getTestsuite(self):
        testcaseids =  ((1,2,3), (4,5), (1,2,3,5), ())
        testcasepos = ((0,1,2), (3,4), (0,1,2,4), ())
        execorder =   ('3,2,1', '', '1,3,2,5', '')
        for i in range(len(testcasepos)):
            data = {'title'         : u"Testsuite title %03d (ÄÖÜäöüß)" % i, 
                    'description'   : u"Testsuite description %03d (ÄÖÜäöüß)" %i,
                    'r_description' : u"\nTestsuite description %03d (ÄÖÜäöüß)" %i,
                    'execorder'     : execorder[i],
                    'testcasepos'   : testcasepos[i],
                    'testcaseids'   : testcaseids[i],
                    'nbrtestcases'  : len(testcasepos[i])}
            yield(data)
    
    
    def addTestsuites(self):
        ##Timings.Slow()
        for ts in self.getTestsuite():
            self.addTestsuite(**ts)

    
    def newProduct(self, filename):
        self.afeditor.MenuSelect("File -> New product ...")
        savedlg = self.app['Save new product to file']
        savedlg.FileNameEdit.SetEditText(filename)
        savedlg.SpeichernButton.CloseClick()
        ##time.sleep(self.delay)
        
        
    def openProduct(self, filename):
        self.afeditor.MenuSelect("File -> Open product ...")
        dlg = self.app['Open product file']
        dlg.FileNameEdit.SetEditText(filename)
        dlg[u'Ö&ffnenButton'].CloseClick()
        
        
    def readArtefactList(self, coltypes, listview=None):
        if listview == None:
            listview = self.afeditorwin.leftwinListView
        nrows = listview.ItemCount()
        for r in range(nrows):
            item = {}
            for c, coltype in zip(range(len(coltypes)), coltypes):
                data = listview.GetItem(r,c)['text']
                item[coltype['key']] =  coltype['type'](data)
            yield(item)
            
            
    def getHTMLWindowContent(self, htmlwindow):
        htmlwindow.TypeKeys('^A^C')
        return clipboard.GetData()

        
    def count(self, start=0, incr=1):
        cnt = start-incr
        while(True):
            cnt = cnt + incr
            yield(cnt)

        
    def exitApp(self):
        self.afeditor.Close()

