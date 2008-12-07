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


class TestDeleteRestoreArtefactContents(subunittest.TestCase):
    """Test deletion and restoration of artefacts"""

    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 63)
    
    
    def _deleteSelectedItem(self, msg=None):
        helper.treeview.TypeKeys('{DEL}')
        helper.afeditorwin['&Yes'].Click()
        if msg is not None:
            helper.afeditorwin['Edit0'].SetText(msg)
            helper.afeditorwin['OK'].Click()
        
        
    def test_0020_DeleteTextSection(self):
        """Deleting text sections"""
        global numberofartefacts
        helper.treeview.Select((0,0,2))
        self._deleteSelectedItem('deleted by test_0020_DeleteTextSection (1)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,0,0))
        self._deleteSelectedItem('deleted by test_0020_DeleteTextSection (2)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,0,2))
        self._deleteSelectedItem('deleted by test_0020_DeleteTextSection (3)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
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
        

    def test_0030_DeleteGlossaryEntry(self):
        """Deleting glossary entries"""
        global numberofartefacts
        helper.treeview.Select((0,1,2))
        self._deleteSelectedItem()
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,1,2))
        self._deleteSelectedItem()
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,1))        
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 3)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'term'}, {'type':unicode, 'key':'description'}]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (1,2,5)):
            self.assertEqual(actual['id'], refid)
        self.failUnless(helper.treeview.GetItem((0,1,0)))
        self.failUnless(helper.treeview.GetItem((0,1,1)))
        self.failUnless(helper.treeview.GetItem((0,1,2)))
        self.failUnlessRaises(AttributeError, helper.treeview.GetItem, (0,1,3))
        
        
    def test_040_DeleteFeature(self):
        """Deleting features"""
        global numberofartefacts
        helper.treeview.Select((0,2,2))
        self._deleteSelectedItem('deleted by test_040_DeleteFeature (1)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,2,2))
        self._deleteSelectedItem('deleted by test_040_DeleteFeature (2)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,2))        
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 3)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (1,2,5)):
            self.assertEqual(actual['id'], refid)
        self.failUnless(helper.treeview.GetItem((0,2,0)))
        self.failUnless(helper.treeview.GetItem((0,2,1)))
        self.failUnless(helper.treeview.GetItem((0,2,2)))
        self.failUnlessRaises(AttributeError, helper.treeview.GetItem, (0,2,3))
    
    
    def test_050_DeleteRequirement(self):
        """Deleting requirements"""    
        global numberofartefacts
        helper.treeview.Select((0,3,2))
        self._deleteSelectedItem('deleted by test_050_DeleteRequirement (1)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,3))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 16)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17)):
            self.assertEqual(actual['id'], refid)
    
    
    def test_060_DeleteUsecase(self):
        """Deleting usecases"""
        global numberofartefacts
        helper.treeview.Select((0,4,0))
        self._deleteSelectedItem('deleted by test_060_DeleteUsecase (1)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,4))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 4)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (2,3,4,5)):
            self.assertEqual(actual['id'], refid)
    
    
    def test_070_DeleteTestcase(self):
        """Deleting testcases"""
        global numberofartefacts
        helper.treeview.Select((0,5,1))
        self._deleteSelectedItem('deleted by test_070_DeleteTestcase (1)')
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,5))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 5)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (1,3,4,5,6)):
            self.assertEqual(actual['id'], refid)


    def test_080_DeleteTestsuite(self):
        """Deleting testsuites"""
        global numberofartefacts
        helper.treeview.Select((0,6,3))
        self._deleteSelectedItem()
        numberofartefacts -= 1
        self.assertEqual(helper.treeview.ItemCount(), numberofartefacts)
        helper.treeview.Select((0,6))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 3)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'}, {'type':unicode, 'key':'title'}]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (1,2,3)):
            self.assertEqual(actual['id'], refid)
    
    
    def test_100_InspectTrash(self):
        """Inspect contents of trash"""
        helper.treeview.Select((0,7))
        self.assertEqual(2, int(helper.afeditorwin['Number of Features in Trash:Edit'].TextBlock()))
        self.assertEqual(1, int(helper.afeditorwin['Number of Requirements in Trash:Edit'].TextBlock()))
        self.assertEqual(1, int(helper.afeditorwin['Number of Usecases in Trash:Edit'].TextBlock()))
        self.assertEqual(1, int(helper.afeditorwin['Number of Testcases in Trash:Edit'].TextBlock()))
        self.assertEqual(1, int(helper.afeditorwin['Number of Testsuites in Trash:Edit'].TextBlock()))
        self.assertEqual(3, int(helper.afeditorwin['Number of Text Sections in Trash:Edit'].TextBlock()))
        self.assertEqual(2, int(helper.afeditorwin['Number of Glossary Entries in Trash:Edit'].TextBlock()))
        

    def test_110_InspectTrashTextsections(self):
        """ Inspect deleted text sections """
        helper.treeview.Select((0,7,0))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 3)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'},]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (1,3,5)):
            self.assertEqual(actual['id'], refid)
        

    def test_120_InspectTrashGlossaryentries(self):
        """ Inspect deleted glossary entries """
        helper.treeview.Select((0,7,1))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 2)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'},]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (3,4)):
            self.assertEqual(actual['id'], refid)
            

    def test_130_InspectTrashFeatures(self):
        """ Inspect deleted features """
        helper.treeview.Select((0,7,2))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 2)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'},]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (3,4)):
            self.assertEqual(actual['id'], refid)


    def test_140_InspectTrashRequirements(self):
        """ Inspect deleted features """
        helper.treeview.Select((0,7,3))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 1)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'},]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (3,)):
            self.assertEqual(actual['id'], refid)
            

    def test_150_InspectTrashUsecases(self):
        """ Inspect deleted usecases """
        helper.treeview.Select((0,7,4))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 1)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'},]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (1,)):
            self.assertEqual(actual['id'], refid)


    def test_160_InspectTrashTestcases(self):
        """ Inspect deleted usecases """
        helper.treeview.Select((0,7,5))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 1)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'},]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (2,)):
            self.assertEqual(actual['id'], refid)


    def test_170_InspectTrashTestsuites(self):
        """ Inspect deleted usecases """
        helper.treeview.Select((0,7,6))
        nitems = helper.afeditorwin.leftwinListView.ItemCount()
        self.assertEqual(nitems, 1)
        helper.afeditorwin.leftwinListView.Select(0)
        coltypes = [{'type':int, 'key':'id'},]
        for actual, refid, in zip(helper.readArtefactList(coltypes), (4,)):
            self.assertEqual(actual['id'], refid)


    def test_200_InspectStatistics(self):
        """Inspect statistics dialog"""
        timing.WaitUntil(10, 1, helper.afeditor.IsEnabled)
        helper.afeditor.MenuSelect("File -> Statistics ...")
        listitems = []
        coltypes = [{'type':unicode, 'key':'label'}, {'type':unicode, 'key':'value'}]
        for listitem in helper.readArtefactList(coltypes, helper.afeditorwin['ListView']):
            listitems.append(listitem)
        helper.afeditorwin['OKButton'].Click()
        statistics = [
            {'value': u'2 (2,5)', 'label': u'Features without requirements'}, 
            {'value': u'15 (1,2,4,5,6,7,8,9,10,11,12,13,14,15,16)', 'label': u'Requirements without testcases'}, 
            {'value': u'4 (1,3,4,6)', 'label': u'Testcases without requirements'}, 
            {'value': u'1 (6)', 'label': u'Test cases without test suites'}, 
            {'value': u'0', 'label': u'Testsuites without testcases'}, 
            {'value': u'0', 'label': u'Usecases without features or requirements'}, 
            {'value': u'2', 'label': u'Text sections'}, 
            {'value': u'3', 'label': u'Glossary entries'},
            {'value': u'3', 'label': u'Features'}, 
            {'value': u'16', 'label': u'Requirements'}, 
            {'value': u'4', 'label': u'Usecases'}, 
            {'value': u'5', 'label': u'Testcases'},
            {'value': u'3', 'label': u'Testsuites'}]
        for expected_item, actual_item in zip(statistics, listitems):
            self.assertEqual(expected_item['label'], actual_item['label'])
            self.assertEqual(expected_item['value'], actual_item['value'])
            
    
    def _restoreSelectedItem(self, msg=None):
        helper.afeditorwin.leftwinListView.TypeKeys('{ENTER}')
        helper.afeditorwin['&Yes'].Click()
        if msg is not None:
            helper.afeditorwin['Edit0'].SetText(msg)
            helper.afeditorwin['OK'].Click()
            

    def test_300_RestoreTextsections(self):
        """ Restore text sections """
        helper.treeview.Select((0,7,0))
        for i in range(3):
            helper.afeditorwin.leftwinListView.Select(0)
            self._restoreSelectedItem('restored by test_300_RestoreTextsections (%d)' % i)
            
    
    def test_310_RestoreGlossaryentries(self):
        """ Restore glossary entries """
        helper.treeview.Select((0,7,1))
        for i in range(2):
            helper.afeditorwin.leftwinListView.Select(0)
            self._restoreSelectedItem()
            

    def test_320_RestoreFeatures(self):
        """ Restore features """
        helper.treeview.Select((0,7,2))
        for i in range(2):
            helper.afeditorwin.leftwinListView.Select(0)
            self._restoreSelectedItem('restored by test_320_RestoreFeatures (%d)' % i)
            
            
    def test_330_RestoreRequirements(self):
        """ Restore requirements"""
        helper.treeview.Select((0,7,3))
        for i in range(1):
            helper.afeditorwin.leftwinListView.Select(0)
            self._restoreSelectedItem('restored by test_330_RestoreRequirements (%d)' % i)
    

    def test_340_RestoreUsecases(self):
        """ Restore usecases """
        helper.treeview.Select((0,7,4))
        for i in range(1):
            helper.afeditorwin.leftwinListView.Select(0)
            self._restoreSelectedItem('restored by test_340_RestoreUsecases (%d)' % i)


    def test_350_RestoreTestcases(self):
        """ Restore testcases """
        helper.treeview.Select((0,7,5))
        for i in range(1):
            helper.afeditorwin.leftwinListView.Select(0)
            self._restoreSelectedItem('restored by test_350_RestoreTestcases (%d)' % i)


    def test_360_RestoreTestsuites(self):
        """ Restore testsuites """
        helper.treeview.Select((0,7,6))
        for i in range(1):
            helper.afeditorwin.leftwinListView.Select(0)
            self._restoreSelectedItem()
            
            
    def test_370_InspectStatistics(self):
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


    def test_380_InspectTrash(self):
        """Inspect contents of trash"""
        helper.treeview.Select((0,7))
        self.assertEqual(0, int(helper.afeditorwin['Number of Features in Trash:Edit'].TextBlock()))
        self.assertEqual(0, int(helper.afeditorwin['Number of Requirements in Trash:Edit'].TextBlock()))
        self.assertEqual(0, int(helper.afeditorwin['Number of Usecases in Trash:Edit'].TextBlock()))
        self.assertEqual(0, int(helper.afeditorwin['Number of Testcases in Trash:Edit'].TextBlock()))
        self.assertEqual(0, int(helper.afeditorwin['Number of Testsuites in Trash:Edit'].TextBlock()))
        self.assertEqual(0, int(helper.afeditorwin['Number of Text Sections in Trash:Edit'].TextBlock()))
        self.assertEqual(0, int(helper.afeditorwin['Number of Glossary Entries in Trash:Edit'].TextBlock()))
        

    def test_390_InspectTrashItems(self):
        """ Inspect trash items """
        for i in range(7):
            helper.treeview.Select((0,7,i))
            nitems = helper.afeditorwin.leftwinListView.ItemCount()
            self.assertEqual(nitems, 0)
        

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
    suite.addTests(testloader.loadTestsFromTestCase(TestDeleteRestoreArtefactContents))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
