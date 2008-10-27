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

import shutil, os.path, sys, time
import unittest, subunittest
from pywinauto import application
import afmstest


class myEditorTestHelper(afmstest.afEditorTestHelper):
    
    def getTextSection(self, n=5):
        for af in super(myEditorTestHelper, self).getTextSection(n):
            yield self.modifyTextSection(af)
            

    def modifyTextSection(self, af):
        af['title'] = 'MODTS ' + af['title']
        return af
        
    
    def getGlossaryEntry(self, n=5):
        for af in super(myEditorTestHelper, self).getGlossaryEntry(n):
            yield self.modifyGlossaryEntry(af)
            
    
    def modifyGlossaryEntry(self, af):
        af['term'] = 'MODGE ' + af['term']
        return af
    

    def getFeature(self):
        for af in super(myEditorTestHelper, self).getFeature():
            yield self.modifyFeature(af)


    def modifyFeature(self, af):
        af['title'] = 'MODFT ' + af['title']
        return af


    def getRequirement(self):
        for af in super(myEditorTestHelper, self).getRequirement():
            # Hmm...
            # Ask a wizard why I have to do this here and why 
            # test_afeditor_verifyartefactcontents.py is running without that
            af['r_description'] = '\n' + af['r_description']
            yield self.modifyRequirement(af)


    def modifyRequirement(self, af):
        af['title'] = 'MODRQ ' + af['title']
        return af
            

class TestArtefactEditing(subunittest.TestCase):
    """Test editing of artefacts"""
    
    def test_0010_NumberOfArtefacts(self):
        """Check number of artefacts in database"""
        self.assertEqual(helper.treeview.ItemCount(), 63)
        
        
    def test_0020_EditTextSection(self):
        """Verify text section editing"""
        for n in range(5):
            helper.editTextSection(n, helper.modifyTextSection)
        for af, i in  zip(helper.getTextSection(5), helper.count(0)):
            helper.treeview.Select((0,0,i))
            self.assertEqual(af['title'], helper.afeditorwin['Title:Edit'].TextBlock())
            content = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            self.assertEqual(content, af['r_content'])
            level = int(helper.afeditorwin.window_(enabled_only=False, best_match='Level:Edit').TextBlock())
            self.assertEqual(af['level'], level)
            id = int(helper.afeditorwin.window_(enabled_only=False, best_match='ID:Edit').TextBlock())
            self.assertEqual(af['id'], id)


    def test_0030_EditGlossaryEntry(self):
        """Verify glossary entry editing"""
        for n in range(5):
            helper.editGlossaryEntry(n, helper.modifyGlossaryEntry)
        for af, i in  zip(helper.getGlossaryEntry(5), helper.count(0)):
            helper.treeview.Select((0,1,i))
            self.assertEqual(af['term'], helper.afeditorwin['Term:Edit'].TextBlock())
            description = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            self.assertEqual(description, af['r_description'])


    def test_0040_EditFeature(self):
        """Verify feature editing"""
        for n in range(5):
            helper.editFeature(n, helper.modifyFeature)
        for af, i in  zip(helper.getFeature(), helper.count(0)):
            helper.treeview.Select((0,2,i))
            self.assertEqual(af['title'], helper.afeditorwin['Title:Edit'].TextBlock())
            description = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            self.assertEqual(description, af['r_description'])


    def test_0050_EditRequirement(self):
        """Verify requirement editing"""
        for n in range(17):
            helper.editRequirement(n, helper.modifyRequirement)
        for af, i in  zip(helper.getRequirement(), helper.count(0)):
            helper.treeview.Select((0,3,i))
            self.assertEqual(af['title'], helper.afeditorwin['Title:Edit'].TextBlock())
            description = helper.getHTMLWindowContent(helper.afeditorwin['htmlWindow'])
            self.assertEqual(description, af['r_description'])


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
        helper = myEditorTestHelper(afmstest.EXECUTABLE, delay=0.01)
        helper.setTiming('slow')
        helper.openProduct(testdbfile)



def getSuite():
    testloader = subunittest.TestLoader()
    testloader.testMethodPrefix = 'test_'
    suite = TestSuite()
    suite.addTests(testloader.loadTestsFromTestCase(TestArtefactEditing))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
