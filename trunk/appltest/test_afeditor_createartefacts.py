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


class TestArtefactCreation(subunittest.TestCase):

    def test_0000_NumberOfArtefactsAtStart(self):
        """Number of artefacts at start"""
        self.assertEqual(helper.treeview.ItemCount(), 16)
        
    def test_0010_EditProduct(self):
        """Edit product"""
        helper.editProduct('Product title', '.. REST\n\nProduct description\n')
        
    def test_0020_AddTextSections(self):
        "Add text sections"
        helper.addTextSections(5)
        
    def test_0030_AddGlossaryEntries(self):
        "Add glossary entries"        
        helper.addGlossaryEntries(4)
        
    def test_0040_AddFeatures(self):
        "Add features"        
        helper.addFeatures()
        
    def test_0050_AddRequirements(self):
        "Add requirements"                
        helper.addRequirements()
        
    def test_0060_AddUsecases(self):
        "Add usecases"        
        helper.addUsecases()
        
    def test_0070_AddTestcases(self):
        "Add testcases"        
        helper.addTestcases()
        
    def test_0080_AddTestsuites(self):
        "Add testsuites"        
        helper.addTestsuites()
        
    def test_0090_NumberOfArtefactsAtEnd(self):
        """Number of artefacts at end"""        
        self.assertEqual(helper.treeview.ItemCount(), 16+32+5+10)

    def test_9999_tearDown(self):
        """No messages on stdout and stderr"""
        helper.exitApp()
        self.assertEqual('\n'.join(helper.process.stdout.readlines()), '')
        self.assertEqual('\n'.join(helper.process.stderr.readlines()), '')


class TestSuite(subunittest.TestSuite):
    def setUpSuite(self):
        global helper
        if not os.path.exists(afmstest.testdbdir):
            os.mkdir(afmstest.testdbdir)
        if os.path.exists(afmstest.testdbfile): 
            os.remove(afmstest.testdbfile)
        helper = afEditorTestHelper(afmstest.EXECUTABLE, delay=0.1)
        helper.newProduct(afmstest.testdbfile)


def getSuite():
    testloader = subunittest.TestLoader()
    testloader.testMethodPrefix = 'test_'
    suite = TestSuite()
    suite.addTests(testloader.loadTestsFromTestCase(TestArtefactCreation))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
