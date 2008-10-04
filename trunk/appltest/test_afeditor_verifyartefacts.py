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

import os, os.path, sys, time, gettext
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


class TestCreatedArtefacts(subunittest.TestCase):
            
    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 63)
    
        
    def test_0020_TextSectionList(self):
        """Inspect text sections list"""
        helper.treeview.Select((0,0))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 5)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':int, 'key':'level'}, {'type':unicode, 'key':'title'}]
        for actual, ref, cnt in zip(helper.readArtefactList(coltypes), helper.getTextSection(), helper.count(1)):
            self.assertEqual(actual['id'], cnt)
            self.assertEqual(actual['level'], cnt)
            self.assertEqual(actual['title'], ref['title'])


    def test_0030_GlossaryEntryList(self):
        """Inspect glossary entry list"""
        helper.treeview.Select((0,1))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 5)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'term'}, {'type':unicode, 'key':'description'}]
        for actual, ref, id in zip(helper.readArtefactList(coltypes), helper.getGlossaryEntry(), helper.count(1)):
            self.assertEqual(actual['term'], ref['term'])
            # ignore ..REST\n\n at beginning and \n at end of ref string
            self.assertNotEqual(ref['description'].find(actual['description']), -1)
            self.assertEqual(actual['id'], id)
            
            
    def test_0040_FeatureList(self):
        "Inspect feature list"
        helper.treeview.Select((0,2))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 5)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}, {'type':unicode, 'key':'priority'},
                    {'type':unicode, 'key':'status'}, {'type':unicode, 'key':'key'},
                    {'type':unicode, 'key':'risk'}, {'type':unicode, 'key':'date'},
                    {'type':unicode, 'key':'user'}, {'type':unicode, 'key':'description'}]
        for actual, ref, id in zip(helper.readArtefactList(coltypes), helper.getFeature(), helper.count(1)):
            self.assertEqual(actual['id'], id)
            self.assertEqual(actual['title'], ref['title'])
            self.assertEqual(actual['priority'], afresource.PRIORITY_NAME[ref['priority']])
            self.assertEqual(actual['status'], afresource.STATUS_NAME[ref['status']])
            self.assertEqual(actual['key'], ref['key'])
            self.assertEqual(actual['risk'], afresource.RISK_NAME[ref['risk']])
            self.assertEqual(type(time.strptime(actual['date'], afresource.TIME_FORMAT)), type(time.gmtime()))
            self.assertEqual(actual['user'], afconfig.CURRENT_USER)
            # ignore ..REST\n\n at beginning and \n at end of ref string
            self.assertNotEqual(ref['description'].find(actual['description']), -1)



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
