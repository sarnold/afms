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
Export database to html output

@author: Achim Koehler
@version: $Rev$
"""

import codecs
from time import localtime, gmtime, strftime
import trmodel
import trconfig
import _afdocutils
import afresource
from afresource import _, ENCODING
from afexporthtml import HTMLFOOTER, htmlentities, specialchars, formatField, __

HTMLHEADER = \
"""
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=%s">
<title>%s</title>
<link href="afmsreport.css" rel="stylesheet" type="text/css">
</head>
<body>
""" % (ENCODING, _('AFMS Test Run Report'))

class trExportHTML():
    def __init__(self, outfilename, model):
        self.model = model
        self.of = codecs.open(outfilename, encoding=ENCODING, mode="w", errors='strict')
        self.writeHTMLHeader()
        self.writeTOC()

        self.of.write('<h1><a name="testruninfo">%s</a></h1>' % __(_('Test run information')))
        self.writeTestrunInfo()
        self.writeSummary()

        self.writeTestcases()

        self.writeHTMLFooter()
        self.of.close()


    def formatField(self, fstr):
        return formatField(fstr)


    def writeHTMLHeader(self):
        self.of.write(HTMLHEADER)


    def writeHTMLFooter(self):
        self.of.write('<hr />')
        footer = _("Created from %s at %s") % (self.model.getFilename(), strftime(afresource.TIME_FORMAT, localtime()))
        self.of.write('<p class="footer">%s</p>' % footer)
        self.of.write(HTMLFOOTER)


    def writeTOC(self):
        pass
    
    
    def writeTestrunInfo(self):
        infos = self.model.getInfo()
        labels = (_("Product title"), _("Creation date"), _("Description"), _("Tester"), _("AF Database"),
                  _("Test suite ID"), _("Test suite title"), _("Test suite description"), _("Test case order"))
        self.of.write('<table>')
        for label, info in zip(labels, infos):
            self.of.write('<tr>')
            self.of.write('<th>%s</th>' % __(label))
            self.of.write('<td>%s</td>' % self.formatField(info))
            self.of.write('</tr>')
        self.of.write('</table>')
    
    
    def writeSummary(self):
        status = self.model.getStatusSummary()
        (total, pending, failed, skipped) = status
        status = list(status)
        passed = total - pending - failed - skipped
        status.append(passed)

        labels = (_('Number of test cases'), _('Pending test cases'), _('Failed test cases'), _('Skipped test cases'), _('Passed test cases'))
        if failed == 0:
            c = "pass"
            msg = afresource.TEST_STATUS_NAME[afresource.PASSED]
        else:
            c = "fail"
            msg = afresource.TEST_STATUS_NAME[afresource.FAILED]
        self.of.write('<p class="%s">%s: %s</p>' % (c,_("Overall result"), msg))
        self.of.write('<table>')
        for label, s in zip(labels, status):
            self.of.write('<tr>')
            self.of.write('<th>%s</th>' % __(label))
            self.of.write('<td>%d</td>' % s)
            self.of.write('</tr>')
        self.of.write('</table>')

    
    def writeTestcases(self):
        tc_labels = (_('ID'), _('Title'), _('Purpose'), _('Prerequisite'), _('Test data'), _('Steps'), _('Notes'), _('Version'))
        tr_labels = (_('Test result'), _('Remark'), _('Action'), _('Time stamp'))
        headings = (_('Failed test cases'), _('Skipped test cases'), _('Pending test cases'), _('Passed test cases'))
        flags = (afresource.FAILED, afresource.SKIPPED, afresource.PENDING, afresource.PASSED)

        for heading, flag in zip(headings, flags):
            self.of.write('<h1>%s</h1>' % __(heading))
            id_list = self.model.getTestcaseIDs(flag)
            if len(id_list) <= 0:
                self.of.write('<p>%s</p>' % _('None'))
                continue
            for tc_id in id_list:
                tc = self.model.getTestcase(tc_id)
                tr = list(self.model.getTestresult(tc_id))
                tr[0] = afresource.TEST_STATUS_NAME[tr[0]]
                self.of.write("<h2>TC-%03d: %s</h2>" % (tc[0], __(tc[1])))
                self.of.write('<table>')
                for label, value in zip(tr_labels, tr):
                    self.of.write('<tr>')
                    self.of.write('<th>%s</th>' % __(label))
                    self.of.write('<td>%s</td>' % self.formatField(value))
                    self.of.write('</tr>')
                for label, value in zip(tc_labels[2:], tc[2:]):
                    self.of.write('<tr>')
                    self.of.write('<th>%s</th>' % __(label))
                    self.of.write('<td>%s</td>' % self.formatField(value))
                    self.of.write('</tr>')
                self.of.write('</table>')
