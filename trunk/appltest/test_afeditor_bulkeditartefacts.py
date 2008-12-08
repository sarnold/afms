#!/usr/bin/python
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

import os, os.path, sys, time, gettext, shutil 
import unittest, subunittest
from pywinauto import application
import pywinauto.timings as timing
import afmstest
from afmstest import afEditorTestHelper

LOCALEDIR = os.path.join('..', 'locale')
DOMAIN = "afms"
gettext.install(DOMAIN, LOCALEDIR, unicode=True)
t = gettext.translation(DOMAIN, LOCALEDIR, languages=['en'])
t.install(unicode=True)
sys.path.append('..')

import afresource, afconfig


class TestBulkEditArtefacts(subunittest.TestCase):
    """Test deletion and restoration of artefacts"""

    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 63)
    
        
    def test_0020_BulkEditTextSection(self):
        """Bulk edit text sections"""
        global numberofartefacts
        helper.treeview.Select((0,0))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit text sections']
        editwin.panelListView.Select(0)
        editwin.panelListView.TypeKeys('^a')
        editwin.leftwinListView.TypeKeys('^+a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        for i in range(5):
            helper.treeview.Select((0,0, i))
            p = helper.afeditorwin['Title:Edit'].Parent().Parent()
            p.TypeKeys('^{TAB}')
            nitems = helper.afeditorwin.leftwinListView.ItemCount()
            self.assertEqual(nitems, 0)
            p.TypeKeys(2 * '^{TAB}')  
        helper.treeview.Select((0,0))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit text sections']
        editwin.panelListView.Select(0)
        editwin.panelListView.TypeKeys('^a')
        editwin.leftwinListView.TypeKeys('^a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        for i in range(5):
            helper.treeview.Select((0,0, i))
            p = helper.afeditorwin['Title:Edit'].Parent().Parent()
            p.TypeKeys('^{TAB}')
            nitems = helper.afeditorwin.leftwinListView.ItemCount()
            self.assertEqual(nitems, 20)
            p.TypeKeys(2 * '^{TAB}')
        
        
    def test_0030_BulkEditFeatures(self):
        """Bulk edit features"""
        helper.treeview.Select((0,2))
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}, {'type':unicode, 'key':'priority'},
                    {'type':unicode, 'key':'status'}, {'type':unicode, 'key':'key'},
                    {'type':unicode, 'key':'risk'}, {'type':unicode, 'key':'date'},
                    {'type':unicode, 'key':'user'}, {'type':unicode, 'key':'description'}]
        ref_features = helper.readArtefactList(coltypes)
        helper.treeview.Select((0,2))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit features']
        editwin.panelListView.Select(0)
        editwin.panelListView.TypeKeys('^a')
        editwin['Key:ComboBox'].Select(0)
        editwin['Priority:ComboBox'].Select(4)
        editwin['Status:ComboBox'].Select(1)
        editwin['Risk:ComboBox'].Select(3)
        p = editwin['Title:Edit'].Parent().Parent()
        p.TypeKeys('^{TAB}')
        editwin.leftwinListView.TypeKeys('^+a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        helper.treeview.Select((0,2))
        act_features = helper.readArtefactList(coltypes)
        for act, ref in zip(act_features, ref_features):
            self.assertEqual(act['title'], ref['title'])
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['key'], ref['key'])
            self.assertEqual(act['description'], ref['description'])
            self.assertEqual(act['priority'], 'Optional')
            self.assertEqual(act['status'], 'Submitted')
            self.assertEqual(act['risk'], '2-Risk')
        # check tags for only one certain feature
        helper.treeview.Select((0,2,2))
        p = helper.afeditorwin['Title:Edit'].Parent().Parent()
        p.TypeKeys(3 * '^{TAB}')
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 0)
        p.TypeKeys(3 * '^+{TAB}')
        # and once again
        ref_features = act_features
        helper.treeview.Select((0,2))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit features']
        editwin.panelListView.Select(0)
        editwin.panelListView.TypeKeys('^a')
        editwin['Key:Edit'].SetText('All the keys are same')
        editwin['Priority:ComboBox'].Select(0)
        editwin['Status:ComboBox'].Select(0)
        editwin['Risk:ComboBox'].Select(0)
        p = editwin['Title:Edit'].Parent().Parent()
        p.TypeKeys('^{TAB}')
        editwin.leftwinListView.Select(3)
        editwin.leftwinListView.TypeKeys('{SPACE}')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        helper.treeview.Select((0,2))
        act_features = helper.readArtefactList(coltypes)
        for act, ref in zip(act_features, ref_features):
            self.assertEqual(act['title'], ref['title'])
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['key'], 'All the keys are same')
            self.assertEqual(act['description'], ref['description'])
            self.assertEqual(act['priority'], ref['priority'])
            self.assertEqual(act['status'], ref['status'])
            self.assertEqual(act['risk'], ref['risk'])
        # check tags for only one certain feature
        helper.treeview.Select((0,2,1))
        p = helper.afeditorwin['Title:Edit'].Parent().Parent()
        p.TypeKeys(3 * '^{TAB}')
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 1)
        p.TypeKeys(3 * '^+{TAB}')
        

    def test_0040_BulkEditRequirements(self):
        """Bulk edit requirements"""
        helper.treeview.Select((0,3))
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}, {'type':unicode, 'key':'priority'},
                    {'type':unicode, 'key':'status'}, {'type':unicode, 'key':'complexity'},
                    {'type':unicode, 'key':'assigned'}, {'type':unicode, 'key':'effort'},
                    {'type':unicode, 'key':'category'}, {'type':unicode, 'key':'key'}, {'type':unicode, 'key':'date'},
                    {'type':unicode, 'key':'user'}, {'type':unicode, 'key':'description'}]
        ref_requirements = [af for af in helper.readArtefactList(coltypes)]
        helper.treeview.Select((0,3))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit requirements']
        for i in range(5):
            editwin.panelListView.Select(i)
            editwin.panelListView.TypeKeys('{SPACE}')
        editwin['Key:ComboBox'].Select(1)
        editwin['Priority:ComboBox'].Select(2)
        editwin['Status:ComboBox'].Select(1)
        editwin['Complexity:ComboBox'].Select(3)
        editwin['Assigned:Edit'].SetText('Poor boy')
        editwin['Effort:ComboBox'].Select(2)
        editwin['Category:ComboBox'].Select(5)
        p = editwin['Title:Edit'].Parent().Parent()
        p.TypeKeys('^{TAB}')
        editwin.leftwinListView.TypeKeys('^+a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        helper.treeview.Select((0,3))
        act_requirements = [af for af in helper.readArtefactList(coltypes)]
        for i in range(5):
            act = act_requirements[i]
            ref = ref_requirements[i]
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['title'], ref['title'])
            self.assertEqual(act['priority'], 'Expected')
            self.assertEqual(act['status'], 'Submitted')
            self.assertEqual(act['complexity'], 'High')
            self.assertEqual(act['assigned'], 'Poor boy')
            self.assertEqual(act['effort'], 'Weeks')
            self.assertEqual(act['category'], 'Security')
            self.assertEqual(act['key'], ref_requirements[0]['key'])
            self.assertNotEqual(act['date'], ref['date'])
            self.assertEqual(act['description'], ref['description'])
        for i in range(5,17):
            act = act_requirements[i]
            ref = ref_requirements[i]
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['title'], ref['title'])
            self.assertEqual(act['priority'], ref['priority'])
            self.assertEqual(act['status'], ref['status'])
            self.assertEqual(act['complexity'], ref['complexity'])
            self.assertEqual(act['assigned'], ref['assigned'])
            self.assertEqual(act['effort'], ref['effort'])
            self.assertEqual(act['category'], ref['category'])
            self.assertEqual(act['key'], ref['key'])
            self.assertEqual(act['date'], ref['date'])
            self.assertEqual(act['user'], ref['user'])
            self.assertEqual(act['description'], ref['description'])
        # check tags for only one certain requirement
        helper.treeview.Select((0,3,1))
        p = helper.afeditorwin['Title:Edit'].Parent().Parent()
        p.TypeKeys(6 * '^{TAB}')
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 0)
        p.TypeKeys(2 * '^{TAB}')
        # and once again
        ref_requirements = act_requirements
        helper.treeview.Select((0,3))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit requirements']
        editwin.panelListView.TypeKeys('^a')
        editwin['Key:ComboBox'].Select(0)
        editwin['Priority:ComboBox'].Select(0)
        editwin['Status:ComboBox'].Select(1)
        editwin['Complexity:ComboBox'].Select(0)
        editwin['Assigned:Edit'].SetText('Another poor boy')
        editwin['Effort:ComboBox'].Select(0)
        editwin['Category:ComboBox'].Select(0)
        p = editwin['Title:Edit'].Parent().Parent()
        p.TypeKeys('^{TAB}')
        editwin.leftwinListView.TypeKeys('^a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        helper.treeview.Select((0,3))
        act_requirements = [af for af in helper.readArtefactList(coltypes)]
        for i in range(len(act_requirements)):
            act = act_requirements[i]
            ref = ref_requirements[i]
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['title'], ref['title'])
            self.assertEqual(act['priority'], ref['priority'])
            self.assertEqual(act['status'], 'Submitted')
            self.assertEqual(act['complexity'], ref['complexity'])
            self.assertEqual(act['assigned'], 'Another poor boy')
            self.assertEqual(act['effort'], ref['effort'])
            self.assertEqual(act['category'], ref['category'])
            self.assertEqual(act['key'], ref['key'])
            self.assertEqual(act['description'], ref['description'])
        # check tags for only one certain requirement
        helper.treeview.Select((0,3,10))
        p = helper.afeditorwin['Title:Edit'].Parent().Parent()
        p.TypeKeys(6 * '^{TAB}')
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 20)
        p.TypeKeys(2 * '^+{TAB}')
        

    def test_0050_BulkEditUsecases(self):
        """Bulk edit usecases"""
        helper.treeview.Select((0,4))
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'summary'}, {'type':unicode, 'key':'priority'},
                    {'type':unicode, 'key':'usefrequency'}, {'type':unicode, 'key':'actors'},
                    {'type':unicode, 'key':'stakeholders'}, {'type':unicode, 'key':'date'},
                    {'type':unicode, 'key':'user'}]
        ref_usecases = [af for af in helper.readArtefactList(coltypes)]
        helper.treeview.Select((0,4))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit usecases']
        editwin.panelListView.TypeKeys('^a')
        editwin['Priority:ComboBox'].Select(2)
        editwin['Use frequency:ComboBox'].Select(5)
        editwin['Actors:ComboBox'].Select(1)
        editwin['Stakeholders:ComboBox'].Select(1)
        p = editwin['Priority:Edit'].Parent().Parent()
        p.TypeKeys('^{TAB}')
        editwin.leftwinListView.TypeKeys('^a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        helper.treeview.Select((0,4))
        act_usecases = [af for af in helper.readArtefactList(coltypes)]
        for i in range(5):
            act = act_usecases[i]
            ref = ref_usecases[i]
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['summary'], ref['summary'])
            self.assertEqual(act['priority'], 'Expected')
            self.assertEqual(act['usefrequency'], 'Once')
            self.assertEqual(act['stakeholders'], ref_usecases[0]['stakeholders'])
        # check tags for only one certain usecase
        helper.treeview.Select((0,4,0))
        p = helper.afeditorwin['Summary:Edit'].Parent().Parent()
        p.TypeKeys(3 * '^{TAB}')
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 20)
        p.TypeKeys(2 * '^{TAB}')


    def test_0060_BulkEditTestcases(self):
        """Bulk edit testcases"""
        helper.treeview.Select((0,5))
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}, {'type':unicode, 'key':'key'},
                    {'type':unicode, 'key':'date'}, {'type':unicode, 'key':'user'},
                    {'type':unicode, 'key':'script'}, {'type':unicode, 'key':'purpose'}]
        ref_testcases = [af for af in helper.readArtefactList(coltypes)]
        helper.treeview.Select((0,5))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit testcases']
        editwin.panelListView.TypeKeys('^a')
        editwin['Key:ComboBox'].Select(2)
        p = editwin['Key:Edit'].Parent().Parent()
        p.TypeKeys('^{TAB}')
        editwin.leftwinListView.Select(0)
        editwin.leftwinListView.TypeKeys('{SPACE}')
        editwin.leftwinListView.Select(1)
        editwin.leftwinListView.TypeKeys('{SPACE}')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        helper.treeview.Select((0,5))
        act_testcases = [af for af in helper.readArtefactList(coltypes)]
        for i in range(len(act_testcases)):
            act = act_testcases[i]
            ref = ref_testcases[i]
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['title'], ref['title'])
            self.assertEqual(act['key'], ref_testcases[1]['key'])
        # check tags for only certain testcases
        for pos, ntags in zip((0,3,4), (3,4,2)):
            helper.treeview.Select((0,5,pos))
            p = helper.afeditorwin['Title:Edit'].Parent().Parent()
            p.TypeKeys(3 * '^{TAB}')
            nitems = helper.afeditorwin.leftwinListView.ItemCount()
            self.assertEqual(nitems, ntags)
            p.TypeKeys(2 * '^{TAB}')
        
    
    def test_0070_BulkEditTestSuites(self):
        """Bulk edit test suites"""
        helper.treeview.Select((0,6))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit test suites']
        editwin.panelListView.Select(0)
        editwin.panelListView.TypeKeys('^a')
        editwin.leftwinListView.TypeKeys('^+a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        for i in range(4):
            helper.treeview.Select((0,6,i))
            p = helper.afeditorwin['Title:Edit'].Parent().Parent()
            p.TypeKeys(2 * '^{TAB}')
            nitems = helper.afeditorwin.leftwinListView.ItemCount()
            self.assertEqual(nitems, 0)
            p.TypeKeys(1 * '^{TAB}')  
        helper.treeview.Select((0,6))
        helper.treeview.TypeKeys('{ENTER}')
        editwin = helper.app['Edit test suites']
        editwin.panelListView.Select(0)
        editwin.panelListView.TypeKeys('^a')
        editwin.leftwinListView.TypeKeys('^a')
        editwin['Save && Close'].Click()
        timing.WaitUntil(10, 1, helper.afeditor.MenuItem('New').IsEnabled)
        for i in range(4):
            helper.treeview.Select((0,6,i))
            p = helper.afeditorwin['Title:Edit'].Parent().Parent()
            p.TypeKeys(2 * '^{TAB}')
            nitems = helper.afeditorwin.leftwinListView.ItemCount()
            self.assertEqual(nitems, 20)
            p.TypeKeys(1 * '^{TAB}')


    def test_9999_tearDown(self):
        """No messages on stdout and stderr"""
        helper.exitApp()
        self.assertEqual('\n'.join(helper.process.stdout.readlines()), '')
        self.assertEqual('\n'.join(helper.process.stderr.readlines()), '')


class TestSuite(subunittest.TestSuite):
    def setUpSuite(self):
        global helper
        global numberofartefacts
        numberofartefacts = 63
        (dirname, basename) = os.path.split(afmstest.testdbfile)
        testdbfile = os.path.join(dirname, 'tmp_' + basename)
        shutil.copyfile(afmstest.testdbfile, testdbfile)        
        helper = afEditorTestHelper(afmstest.EXECUTABLE, delay=0.01)
        helper.setTiming('slow')
        helper.openProduct(testdbfile)


def getSuite():
    testloader = subunittest.TestLoader()
    testloader.testMethodPrefix = 'test'
    suite = TestSuite()
    suite.addTests(testloader.loadTestsFromTestCase(TestBulkEditArtefacts))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
