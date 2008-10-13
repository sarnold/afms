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
import afmstest
from afmstest import afEditorTestHelper

LOCALEDIR = os.path.join('..', 'locale')
DOMAIN = "afms"
gettext.install(DOMAIN, LOCALEDIR, unicode=True)
t = gettext.translation(DOMAIN, LOCALEDIR, languages=['en'])
t.install(unicode=True)
sys.path.append('..')

import afresource, afconfig


class TestDeleteRestoreArtefactContents(subunittest.TestCase):
    """Test deletion and restoration of artefacts"""
    
    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 63)
    
    
    def _deleteSelectedItem(self, msg):
        helper.treeview.TypeKeys('{DEL}')
        helper.afeditorwin['&Yes'].Click()
        helper.afeditorwin['Edit0'].SetText(msg)
        helper.afeditorwin['OK'].Click()
        
        
    def test_0020_DeleteTextSection(self):
        helper.treeview.Select((0,0,2))
        self._deleteSelectedItem('deleted by test_0020_DeleteTextSection (1)')
        self.assertEqual(helper.treeview.ItemCount(), 62)
        helper.treeview.Select((0,0,0))
        self._deleteSelectedItem('deleted by test_0020_DeleteTextSection (2)')
        self.assertEqual(helper.treeview.ItemCount(), 61)
        helper.treeview.Select((0,0,2))
        self._deleteSelectedItem('deleted by test_0020_DeleteTextSection (3)')
        self.assertEqual(helper.treeview.ItemCount(), 60)
        helper.treeview.Select((0,0))        
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 2)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':int, 'key':'level'}, {'type':unicode, 'key':'title'}]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (2,4)):
            self.assertEqual(actual['id'], refid)
        self.failUnless(helper.treeview.GetItem((0,0,0)))
        self.failUnless(helper.treeview.GetItem((0,0,1)))
        self.failUnlessRaises(AttributeError, helper.treeview.GetItem, (0,0,2))
        

    def xxtest_9999_tearDown(self):
        """No messages on stdout and stderr"""
        helper.exitApp()
        self.assertEqual('\n'.join(helper.process.stdout.readlines()), '')
        self.assertEqual('\n'.join(helper.process.stderr.readlines()), '')


class TestSuite(subunittest.TestSuite):
    def setUpSuite(self):
        global helper
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
    suite.addTests(testloader.loadTestsFromTestCase(TestDeleteRestoreArtefactContents))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
