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

import os, os.path, sys, time, subprocess
import unittest, subunittest
import xml.dom
from xml.dom.minidom import parse
import afmstest


class TestExportXML(subunittest.TestCase):
    """ Test xml export"""
    
    def test_0050_FeatureTags(self):
        """Check that features have the correct tags"""
        nodes = dom.getElementsByTagName('feature')
        self.assertEqual(len(nodes), 5)
        nodenames = ['title', 'priority', 'status', 'version', 'risk', 'description', 'relatedrequirements', 'relatedusecases', 'changelist', 'taglist']
        for node in nodes[0].childNodes:
            if node.nodeType == node.TEXT_NODE: continue
            self.failUnless(node.nodeName in nodenames, 'invalid node %s' % node.nodeName)
            nodenames.remove(node.nodeName)
        self.failUnlessEqual(len(nodenames), 0, str(nodenames))
        
    

    def test_0060_RequirementTags(self):
        """Check that requirements have the correct tags"""
        nodes = dom.getElementsByTagName('requirement')
        self.assertEqual(len(nodes), 17)
        nodenames = ['title', 'priority', 'status', 'version', 'complexity', 'assigned', 'effort', 'category', 'description', 'origin', 'rationale', 'relatedfeatures', 'relatedrequirements', 'relatedusecases', 'relatedtestcases', 'changelist', 'taglist']
        for node in nodes[0].childNodes:
            if node.nodeType == node.TEXT_NODE: continue
            self.failUnless(node.nodeName in nodenames, 'invalid node <%s>' % node.nodeName)
            nodenames.remove(node.nodeName)
        self.failUnlessEqual(len(nodenames), 0, 'missing nodes %s' % str(nodenames))
        


class TestSuite(subunittest.TestSuite):
    def setUpSuite(self):
        global xmlfile
        global dom
        xmlfile = os.path.splitext(afmstest.testdbfile)[0] + '.xml'
        cmd = sys.executable + ' ' + r"../afexportxml.py -o %s %s" % (xmlfile, afmstest.testdbfile)
        process = subprocess.call(cmd)
        dom = parse(xmlfile)



def getSuite():
    testloader = subunittest.TestLoader()
    suite = TestSuite()
    suite.addTests(testloader.loadTestsFromTestCase(TestExportXML))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(getSuite())
