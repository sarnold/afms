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

    def test_0000_ArtefactCreation(self):
        """Creating artifacts"""
        self.assertEqual(helper.treeview.ItemCount(), 16)
        helper.editProduct('Product title', '.. REST\n\nProduct description\n')
        helper.addTextSections(5)
        helper.addGlossaryEntries(4)
        helper.addFeatures()
        helper.addRequirements()
        self.assertEqual(helper.treeview.ItemCount(), 16+32)
    
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
        helper = afEditorTestHelper(afmstest.EXECUTABLE, delay=0.01)
        helper.newProduct(afmstest.testdbfile)


def getSuite():
    testloader = subunittest.TestLoader()
    suite = TestSuite()
    suite.addTests(testloader.loadTestsFromTestCase(TestArtefactCreation))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
