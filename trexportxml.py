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

"""
Export database to xml output

@author: Achim Koehler
@version: $Rev$
"""

import codecs
from time import localtime, gmtime, strftime
import trmodel
import afresource
from afresource import ENCODING


class trExportXML():
    def __init__(self, outfilename, model):
        self.model = model
        self.of = codecs.open(outfilename, encoding=ENCODING, mode="w", errors='strict')
        self.writeXMLHeader()
        self.writeTestrunInfo()
        self.writeSummary()
        self.writeTestcases()
        self.writeXMLFooter()
        self.of.close()


    def writeTag(self, tag, content):
        self.of.write("<%s><![CDATA[%s]]></%s>" % (tag, content, tag))


    def writeSimpleTag(self, tag, content):
        self.of.write("<%s>%s</%s>" % (tag, content, tag))


    def writeXMLHeader(self):
        self.of.write('<?xml version="1.0" encoding="UTF-8"?>')
        self.of.write('<!-- Created from %s at %s -->' % (self.model.getFilename(), strftime(afresource.TIME_FORMAT, localtime())))
        self.of.write('<testrun>')


    def writeXMLFooter(self):
        self.of.write('</testrun>')

    
    def writeTestrunInfo(self):
        infos = self.model.getInfo()
        labels = ("product_title", "creation_date", "description", "tester", "af_database",
                  "testsuite_id", "testsuite_title", "testsuite_description", "testcase_order")
        self.of.write('<testruninfo>')
        for label, info in zip(labels, infos):
            self.writeTag(label, info)
        self.of.write('</testruninfo>')
    
    
    def writeSummary(self):
        status = self.model.getStatusSummary()
        (total, pending, failed, skipped) = status
        status = list(status)
        passed = total - pending - failed - skipped
        status.append(passed)

        labels = ('total', 'pending', 'failed', 'skipped', 'passed')
        self.of.write('<summary>')
        self.writeSimpleTag('overall_passed', int(failed == 0))
        for label, s in zip(labels, status):
            self.writeSimpleTag(label, s)
        self.of.write('</summary>')

    
    def writeTestcases(self):
        tc_labels = ('id', 'title', 'purpose', 'prerequisite', 'test_data', 'steps', 'notes', 'version')
        tr_labels = ('test_result', 'remark', 'action', 'time_stamp')
        flags = (afresource.FAILED, afresource.SKIPPED, afresource.PENDING, afresource.PASSED)

        for flag in flags:
            id_list = self.model.getTestcaseIDs(flag)
            if len(id_list) <= 0:
                continue
            
            for tc_id in id_list:
                self.of.write('<testcase>')
                tc = self.model.getTestcase(tc_id)
                tr = list(self.model.getTestresult(tc_id))
                self.writeSimpleTag(tc_labels[0], tc[0])
                for label, value in zip(tr_labels, tr):
                    self.writeTag(label, value)
                for label, value in zip(tc_labels[1:], tc[1:]):
                    self.writeTag(label, value)
                self.of.write('</testcase>')
