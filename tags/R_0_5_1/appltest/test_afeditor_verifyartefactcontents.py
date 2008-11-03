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


class TestCreatedArtefactContents(subunittest.TestCase):
    """Test details of all created artefacts"""
    
    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 63)
    
        
    def test_0020_ProductDescription(self):
        """Inspect product description"""
        helper.treeview.Select((0,))
        self.assertEqual('Product title', helper.afeditorwin['Title:Edit'].TextBlock())
        self.assertEqual(helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow']).strip(' \n'), 'Product description')


    def test_0030_TextSectionContents(self):
        """Inspect text section contents"""
        for af, i in  zip(helper.getTextSection(5), helper.count(0)):
            helper.treeview.Select((0,0,i))
            self.assertEqual(af['title'], helper.afeditorwin['Title:Edit'].TextBlock())
            content = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            self.assertEqual(content, af['r_content'])
            level = int(helper.afeditorwin.window_(enabled_only=False, best_match='Level:Edit').TextBlock())
            self.assertEqual(af['level'], level)
            id = int(helper.afeditorwin.window_(enabled_only=False, best_match='ID:Edit').TextBlock())
            self.assertEqual(af['id'], id)


    def test_0040_GlossaryEntryContents(self):
        """Inspect glossary entry contents"""
        for af, i in  zip(helper.getGlossaryEntry(5), helper.count(0)):
            helper.treeview.Select((0,1,i))
            self.assertEqual(af['term'], helper.afeditorwin['Term:Edit'].TextBlock())
            description = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            self.assertEqual(description, af['r_description'])


    def test_0050_FeatureContents(self):
        """Inspect feature contents"""
        for af, i in  zip(helper.getFeature(), helper.count(0)):
            actual_af = helper.readFeatureAtPosition(i)
            self.assertEqual(af['title'], actual_af['title'])
            self.assertEqual(i+1, actual_af['id'])
            self.assertEqual(af['key'], actual_af['key'])
            self.assertEqual(actual_af['priority'], afresource.PRIORITY_NAME[af['priority']])
            self.assertEqual(actual_af['status'], afresource.STATUS_NAME[af['status']])
            self.assertEqual(actual_af['risk'], afresource.RISK_NAME[af['risk']])
            self.assertEqual(actual_af['description'], af['r_description'])
            self.assertEqual(actual_af['related_requirements'], list(af['related_requirements']))
            self.assertEqual(actual_af['related_usecases'], list(af['related_usecases']))
    
    
    def test_0060_RequirementContents(self):
        """Inspect requirement contents"""
        for af, i in  zip(helper.getRequirement(), helper.count(0)):
            actual_af = helper.readRequirementAtPosition(i)
            self.assertEqual(af['title'], actual_af['title'])
            self.assertEqual(i+1, actual_af['id'])
            self.assertEqual(af['key'], actual_af['key'])
            self.assertEqual(actual_af['priority'], afresource.PRIORITY_NAME[af['priority']])
            self.assertEqual(actual_af['status'], afresource.STATUS_NAME[af['status']])
            self.assertEqual(actual_af['complexity'], afresource.COMPLEXITY_NAME[af['complexity']])
            self.assertEqual(actual_af['assigned'], af['assigned'])
            self.assertEqual(actual_af['effort'], afresource.EFFORT_NAME[af['effort']])
            self.assertEqual(actual_af['category'], afresource.CATEGORY_NAME[af['category']])
            self.assertEqual(af['r_description'], actual_af['description'])
            self.assertEqual(actual_af['origin'], af['origin'])
            self.assertEqual(actual_af['rationale'], af['r_rationale'])
            self.assertEqual(actual_af['related_testcases'], list(af['related_testcases']))
            self.assertEqual(actual_af['related_usecases'], list(af['related_usecases']))
            self.assertEqual(actual_af['related_features'], list(af['related_features']))
            self.assertEqual(actual_af['related_requirements'], list(af['related_requirements']))
            

    def test_0070_UsecaseContents(self):
        """Inspect usecase contents"""
        for af, i in  zip(helper.getUsecase(), helper.count(0)):
            actual_af = helper.readUsecaseAtPosition(i)
            self.assertEqual(actual_af['summary'], af['summary'])
            self.assertEqual(actual_af['id'], i+1)
            self.assertEqual(actual_af['priority'], afresource.PRIORITY_NAME[af['priority']])
            self.assertEqual(actual_af['usefrequency'], afresource.USEFREQUENCY_NAME[af['usefrequency']])
            self.assertEqual(actual_af['actors'], af['actors'])
            self.assertEqual(actual_af['stakeholders'], af['stakeholders'])
            self.assertEqual(actual_af['prerequisites'], af['r_prerequisites'])
            self.assertEqual(actual_af['mainscenario'], af['r_mainscenario'])
            self.assertEqual(actual_af['altscenario'], af['r_altscenario'])
            self.assertEqual(actual_af['notes'], af['r_notes'])
            self.assertEqual(actual_af['related_features'], list(af['related_features']))
            self.assertEqual(actual_af['related_requirements'], list(af['related_requirements']))


    def test_0080_TestcaseContents(self):
        """Inspect testcase contents"""
        for af, i in  zip(helper.getTestcase(), helper.count(0)):
            data = helper.readTestcaseAtPosition(i)
            self.assertEqual(data['title'], af['title'])
            self.assertEqual(data['id'], i+1)
            self.assertEqual(data['key'], af['key'])
            self.assertEqual(data['script'], af['script'])
            self.assertEqual(data['purpose'], af['r_purpose'])
            self.assertEqual(data['prerequisite'], af['r_prerequisite'])
            self.assertEqual(data['testdata'], af['r_testdata'])
            self.assertEqual(data['steps'], af['r_steps'])
            self.assertEqual(data['notes'], af['r_notes'])
            self.assertEqual(data['related_requirements'], list(af['related_requirements']))
            self.assertEqual(data['related_testsuites'], list(af['related_testsuites']))


    def test_0090_TestsuiteContents(self):
        """Inspect testsuite contents"""
        for af, i in  zip(helper.getTestsuite(), helper.count(0)):
            data = helper.readTestsuiteAtPosition(i)
            self.assertEqual(data['title'], af['title'])
            self.assertEqual(data['id'], i+1)
            self.assertEqual(data['execorder'], af['execorder'])
            self.assertEqual(data['description'], af['r_description'])
            self.assertEqual(data['testcaseids'], af['testcaseids'])


    def test_9999_tearDown(self):
        """No messages on stdout and stderr"""
        helper.exitApp()
        self.assertEqual('\n'.join(helper.process.stdout.readlines()), '')
        self.assertEqual('\n'.join(helper.process.stderr.readlines()), '')


class TestSuite(subunittest.TestSuite):
    def setUpSuite(self):
        global helper
        helper = afEditorTestHelper(afmstest.EXECUTABLE, delay=0.01)
        helper.setTiming('slow')
        helper.openProduct(afmstest.testdbfile)


def getSuite():
    testloader = subunittest.TestLoader()
    testloader.testMethodPrefix = 'test'
    suite = TestSuite()
    suite.addTests(testloader.loadTestsFromTestCase(TestCreatedArtefactContents))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
