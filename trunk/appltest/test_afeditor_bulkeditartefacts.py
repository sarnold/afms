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
        """Bulk edit text sections"""
        ref_features = [helper.readFeatureAtPosition(i) for i in range(5)]
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
        act_features = [helper.readFeatureAtPosition(i) for i in range(5)]
        for act, ref in zip(act_features, ref_features):
            self.assertEqual(act['title'], ref['title'])
            self.assertEqual(act['id'], ref['id'])
            self.assertEqual(act['key'], ref['key'])
            self.assertEqual(act['description'], ref['description'])
            self.assertEqual(act['priority'], 'Optional')
            self.assertEqual(act['status'], 'Submitted')
            self.assertEqual(act['risk'], '2-Risk')
        

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
