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
            helper.treeview.Select((0,2,i))
            title = helper.afeditorwin['Title:Edit'].TextBlock()
            id = int(helper.afeditorwin.window_(enabled_only=False, best_match='ID:Edit').TextBlock())
            key = helper.afeditorwin['Key:Edit'].TextBlock()
            priority = helper.afeditorwin['Priority:Edit'].TextBlock()
            status = helper.afeditorwin['Status:Edit'].TextBlock()
            risk = helper.afeditorwin['Risk:Edit'].TextBlock()
            description = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            p = helper.afeditorwin['Priority:Edit'].Parent().Parent()
            # related requirements
            p.TypeKeys('^{TAB}')
            actual_related_requirements = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for requirement in helper.readArtefactList(coltypes, helper.afeditorwin['Requirements:ListView']):
                actual_related_requirements.append(requirement['id'])
            # attached usecases
            p.TypeKeys('^{TAB}')
            actual_attached_usecases = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for usecase in helper.readArtefactList(coltypes, helper.afeditorwin['Usecases:ListView']):
                actual_attached_usecases.append(usecase['id'])
            p.TypeKeys(2*'^+{TAB}')
            self.assertEqual(af['title'], title)
            self.assertEqual(i+1, id)
            self.assertEqual(af['key'], key)
            self.assertEqual(priority, afresource.PRIORITY_NAME[af['priority']])
            self.assertEqual(status, afresource.STATUS_NAME[af['status']])
            self.assertEqual(risk, afresource.RISK_NAME[af['risk']])
            self.assertEqual(description, af['r_description'])
            self.assertEqual(actual_related_requirements, list(af['related_requirements']))
            self.assertEqual(actual_attached_usecases, list(af['related_usecases']))
    
    
    def test_0060_RequirementContents(self):
        """Inspect requirement contents"""
        for af, i in  zip(helper.getRequirement(), helper.count(0)):
            helper.treeview.Select((0,3,i))
            title = helper.afeditorwin['Title:Edit'].TextBlock()
            id = int(helper.afeditorwin.window_(enabled_only=False, best_match='ID:Edit').TextBlock())
            key = helper.afeditorwin['Key:Edit'].TextBlock()
            priority = helper.afeditorwin['Priority:Edit'].TextBlock()
            status = helper.afeditorwin['Status:Edit'].TextBlock()
            complexity = helper.afeditorwin['Complexity:Edit'].TextBlock()
            assigned = helper.afeditorwin['Assigned:Edit'].TextBlock()
            effort = helper.afeditorwin['Effort:Edit'].TextBlock()
            category = helper.afeditorwin['Category:Edit'].TextBlock()
            description = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow']).strip(' \n')  
            p = helper.afeditorwin['Priority:Edit'].Parent().Parent()
            p.TypeKeys('^{TAB}')
            origin = helper.getHTMLWindowContent(helper.afeditorwin['oridin_edit']).strip(' \n')
            rationale = helper.getHTMLWindowContent(helper.afeditorwin['rationale_edit']).strip(' \n')
            # attached testcases
            p.TypeKeys('^{TAB}')
            actual_attached_testcases = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Testcases:ListView']):
                actual_attached_testcases.append(afitem['id'])
            # attached usecases
            p.TypeKeys('^{TAB}')
            actual_attached_usecases = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Usecases:ListView']):
                actual_attached_usecases.append(afitem['id'])
            # releated features
            p.TypeKeys('^{TAB}')
            actual_related_features = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Features:ListView']):
                actual_related_features.append(afitem['id'])
            # related requirements
            p.TypeKeys('^{TAB}')
            actual_related_requirements = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Requirements:ListView']):
                actual_related_requirements.append(afitem['id'])
            p.TypeKeys(2 * '^{TAB}')
            self.assertEqual(af['title'], title)
            self.assertEqual(i+1, id)
            self.assertEqual(af['key'], key)
            self.assertEqual(priority, afresource.PRIORITY_NAME[af['priority']])
            self.assertEqual(status, afresource.STATUS_NAME[af['status']])
            self.assertEqual(complexity, afresource.COMPLEXITY_NAME[af['complexity']])
            self.assertEqual(assigned, af['assigned'])
            self.assertEqual(effort, afresource.EFFORT_NAME[af['effort']])
            self.assertEqual(category, afresource.CATEGORY_NAME[af['category']])
            self.assertEqual(af['r_description'], description)
            self.assertEqual(origin, af['origin'])
            self.assertEqual(rationale, af['r_rationale'])
            self.assertEqual(actual_attached_testcases, list(af['related_testcases']))
            self.assertEqual(actual_attached_usecases, list(af['related_usecases']))
            self.assertEqual(actual_related_features, list(af['related_features']))
            self.assertEqual(actual_related_requirements, list(af['related_requirements']))
            

    def test_0070_UsecaseContents(self):
        """Inspect usecase contents"""
        for af, i in  zip(helper.getUsecase(), helper.count(0)):
            helper.treeview.Select((0,4,i))
            summary = helper.afeditorwin['Summary:Edit'].TextBlock()
            id = int(helper.afeditorwin.window_(enabled_only=False, best_match='ID:Edit').TextBlock())
            priority = helper.afeditorwin['Priority:Edit'].TextBlock()
            usefrequency = helper.afeditorwin['Use frequency:Edit'].TextBlock()
            actors = helper.afeditorwin['Actors:Edit'].TextBlock()
            stakeholders = helper.afeditorwin['Stakeholders:Edit'].TextBlock()            
            prerequisites = helper.getHTMLWindowContent(helper.afeditorwin['prerequisites'])
            mainscenario = helper.getHTMLWindowContent(helper.afeditorwin['mainscenario'])
            altscenario = helper.getHTMLWindowContent(helper.afeditorwin['altscenario'])
            notes = helper.getHTMLWindowContent(helper.afeditorwin['notes'])
            p = helper.afeditorwin['Priority:Edit'].Parent().Parent()
            # releated features
            p.TypeKeys('^{TAB}')
            actual_related_features = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Features:ListView']):
                actual_related_features.append(afitem['id'])
            # related requirements
            p.TypeKeys('^{TAB}')
            actual_related_requirements = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Requirements:ListView']):
                actual_related_requirements.append(afitem['id'])
            p.TypeKeys(2 * '^{TAB}')
            self.assertEqual(af['summary'], summary)
            self.assertEqual(i+1, id)
            self.assertEqual(priority, afresource.PRIORITY_NAME[af['priority']])
            self.assertEqual(usefrequency, afresource.USEFREQUENCY_NAME[af['usefrequency']])
            self.assertEqual(actors, af['actors'])
            self.assertEqual(stakeholders, af['stakeholders'])
            self.assertEqual(prerequisites, af['r_prerequisites'])
            self.assertEqual(mainscenario, af['r_mainscenario'])
            self.assertEqual(altscenario, af['r_altscenario'])
            self.assertEqual(notes, af['r_notes'])
            self.assertEqual(actual_related_features, list(af['related_features']))
            self.assertEqual(actual_related_requirements, list(af['related_requirements']))


    def test_0080_TestcaseContents(self):
        """Inspect testcase contents"""
        for af, i in  zip(helper.getTestcase(), helper.count(0)):
            helper.treeview.Select((0,5,i))
            title = helper.afeditorwin['Title:Edit'].TextBlock()
            id = int(helper.afeditorwin.window_(enabled_only=False, best_match='ID:Edit').TextBlock())
            key = helper.afeditorwin['Key:Edit'].TextBlock()
            script = helper.afeditorwin['Script:Edit'].TextBlock()
            purpose = helper.getHTMLWindowContent(helper.afeditorwin['purpose'])
            prerequisite = helper.getHTMLWindowContent(helper.afeditorwin['prerequisite'])
            testdata = helper.getHTMLWindowContent(helper.afeditorwin['testdata'])
            steps = helper.getHTMLWindowContent(helper.afeditorwin['steps'])
            notes = helper.getHTMLWindowContent(helper.afeditorwin['notes'])
            p = helper.afeditorwin['Key:Edit'].Parent().Parent()
            # related requirements
            p.TypeKeys('^{TAB}')
            actual_related_requirements = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Requirements:ListView']):
                actual_related_requirements.append(afitem['id'])
            # releated testsuites
            p.TypeKeys('^{TAB}')
            actual_related_testsuites = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for afitem in helper.readArtefactList(coltypes, helper.afeditorwin['Testsuites:ListView']):
                actual_related_testsuites.append(afitem['id'])
            p.TypeKeys(2 * '^{TAB}')
            self.assertEqual(title, af['title'])
            self.assertEqual(id, i+1)
            self.assertEqual(key, af['key'])
            self.assertEqual(script, af['script'])
            self.assertEqual(purpose, af['r_purpose'])
            self.assertEqual(prerequisite, af['r_prerequisite'])
            self.assertEqual(testdata, af['r_testdata'])
            self.assertEqual(steps, af['r_steps'])
            self.assertEqual(notes, af['r_notes'])
            self.assertEqual(actual_related_requirements, list(af['related_requirements']))
            self.assertEqual(actual_related_testsuites, list(af['related_testsuites']))


    def test_0090_TestsuiteContents(self):
        """Inspect testsuite contents"""
        for af, i in  zip(helper.getTestsuite(), helper.count(0)):
            helper.treeview.Select((0,6,i))
            title = helper.afeditorwin['Title:Edit'].TextBlock()
            id = int(helper.afeditorwin.window_(enabled_only=False, best_match='ID:Edit').TextBlock())
            execorder = helper.afeditorwin["Execution order ID's:Edit"].TextBlock()
            description = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            testcaseids = []
            coltypes = [{'type':int, 'key':'id'}, ]
            for testcaseid in helper.readArtefactList(coltypes, helper.afeditorwin['Testcases:ListView']):
                testcaseids.append(testcaseid['id'])
            testcaseids = tuple(testcaseids)
            self.assertEqual(af['title'], title)
            self.assertEqual(i+1, id)
            self.assertEqual(execorder, af['execorder'])
            self.assertEqual(description, af['r_description'])
            self.assertEqual(testcaseids, af['testcaseids'])


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
