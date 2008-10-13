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


class TestStatistics(subunittest.TestCase):
    """ Test statistics information"""
    
    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 63)
    
        
    def test_0020_InspectStatistics(self):
        """Inspect statistics dialog"""
        timing.WaitUntil(10, 1, helper.afeditor.IsEnabled)
        helper.afeditor.MenuSelect("File -> Statistics ...")
        listitems = []
        coltypes = [{'type':unicode, 'key':'label'}, {'type':unicode, 'key':'value'}]
        for listitem in helper.readArtefactList(coltypes, helper.afeditorwin['ListView']):
            listitems.append(listitem)
        helper.afeditorwin['OKButton'].Click()
        statistics = [
            {'value': u'3 (2,4,5)', 'label': u'Features without requirements'}, 
            {'value': u'14 (2,4,5,6,7,8,9,10,11,12,13,14,15,16)', 'label': u'Requirements without testcases'}, 
            {'value': u'2 (1,6)', 'label': u'Testcases without requirements'}, 
            {'value': u'1 (6)', 'label': u'Test cases without test suites'}, 
            {'value': u'1 (4)', 'label': u'Testsuites without testcases'}, 
            {'value': u'1 (1)', 'label': u'Usecases without features or requirements'}, 
            {'value': u'5', 'label': u'Text sections'}, 
            {'value': u'5', 'label': u'Glossary entries'},
            {'value': u'5', 'label': u'Features'}, 
            {'value': u'17', 'label': u'Requirements'}, 
            {'value': u'5', 'label': u'Usecases'}, {'value': u'6', 'label': u'Testcases'},
            {'value': u'4', 'label': u'Testsuites'}]
        for expected_item, actual_item in zip(statistics, listitems):
            self.assertEqual(expected_item['label'], actual_item['label'])
            self.assertEqual(expected_item['value'], actual_item['value'])
        

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
    suite.addTests(testloader.loadTestsFromTestCase(TestStatistics))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
