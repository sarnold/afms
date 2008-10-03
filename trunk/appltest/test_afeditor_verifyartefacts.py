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

import os.path, sys, time
import unittest, subunittest
from pywinauto import application
import afmstest
from afmstest import afEditorTestHelper


class TestCreatedArtefacts(subunittest.TestCase):
            
    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 48)
    
        
    def test_0020_TextSectionList(self):
        """Inspect text sections list"""
        helper.treeview.Select((0,0))
        nitems = helper.afeditor.leftwinListView.ItemCount()
        self.assertEqual(nitems, 5)
        helper.afeditor.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':int, 'key':'level'}, {'type':unicode, 'key':'title'}]
        for actual, ref, cnt in zip(helper.readArtefactList(coltypes), helper.getTextSection(), helper.count(1)):
            self.assertEqual(actual['id'], cnt)
            self.assertEqual(actual['level'], cnt)
            self.assertEqual(actual['title'], ref['title'])


    def test_0030_GlossaryEntryList(self):
        """Inspect glossary entry list"""
        helper.treeview.Select((0,1))
        nitems = helper.afeditor.leftwinListView.ItemCount()
        self.assertEqual(nitems, 5)
        helper.afeditor.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'term'}, {'type':unicode, 'key':'description'}]
        for actual, ref, id in zip(helper.readArtefactList(coltypes), helper.getGlossaryEntry(), helper.count(1)):
            self.assertEqual(actual['term'], ref['term'])
            # ignore ..REST\n\n at beginning and \n at end of ref string
            self.assertNotEqual(ref['description'].find(actual['description']), -1)
            self.assertEqual(actual['id'], id)


    def test_9999_tearDown(self):
        """No messages on stdout and stderr"""
        helper.exitApp()
        self.assertEqual('\n'.join(helper.process.stdout.readlines()), '')
        self.assertEqual('\n'.join(helper.process.stderr.readlines()), '')


class TestSuite(subunittest.TestSuite):
    def setUpSuite(self):
        global helper
        helper = afEditorTestHelper(afmstest.EXECUTABLE, delay=0.01)
        helper.openProduct(afmstest.testdbfile)


def getSuite():
    testloader = subunittest.TestLoader()
    suite = TestSuite()
    suite.addTests(testloader.loadTestsFromTestCase(TestCreatedArtefacts))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
