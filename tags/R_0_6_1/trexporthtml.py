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

"""
Export testrunner database to html output

@author: Achim Koehler
@version: $Rev$
"""

import os
import codecs, logging
from xml.dom.minidom import getDOMImplementation, XMLNS_NAMESPACE, parseString, parse
from time import localtime, gmtime, strftime

if __name__=="__main__":
    import sys, gettext, os, getopt
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)

import afexporthtml
if __name__=="__main__":
    afexporthtml.DOMAIN = DOMAIN
    afexporthtml.LOCALEDIR = LOCALEDIR

import afmodel, trmodel
import afconfig
import afresource, _afartefact
from afresource import ENCODING
import _afhtmlwindow



class trExportHTML(afexporthtml.afExportHTML):
    def __init__(self, model, cssfile, title=_('AFMS Test Report')):
        afexporthtml.afExportHTML.__init__(self, model, cssfile, title)


    def run(self):
        self.body.appendChild(self._createHeadline('h1', _('Test run information'), {'name': 'testruninfo'}))
        self.body.appendChild(self.renderTestrunInfo())
        self.body.appendChild(self.renderSummary())
        self.body.appendChild(self.renderTestcases())


    def renderTestrunInfo(self):
        info = self.model.getInfo()
        labels = (_("Product title"), _("Creation date"), _("Description"), _("Tester"), _("AF Database"),
                  _("Test suite ID"), _("Test suite title"), _("Test suite description"), _("Test case order"))
        keys = ("product_title", "creation_date", "description", "tester", "afdatabase", "testsuite_id", "testsuite_title", "testsuite_description", "testsuite_execorder")        
        node = self._createElement('div', {'class': 'testruninfo'})
        table = self._createElement('table', {'class': 'aftable'})
        node.appendChild(table)
        for label, key in zip(labels, keys):
            table.appendChild(self._createTableRow(label, self._render(info[key])))
        return node


    def renderSummary(self):
        status = self.model.getStatusSummary()
        (total, pending, failed, skipped) = status
        status = list(status)
        passed = total - pending - failed - skipped
        status.append(passed)
        labels = (_('Number of test cases'), _('Pending test cases'), _('Failed test cases'), _('Skipped test cases'), _('Passed test cases'))
        hrefs  = ('', '#pendingtestcases', '#failedtestcases', '#skippedtestcases', '#passedtestcases')
        if pending != 0:
            c = "pending"
            msg = _(afresource.TEST_STATUS_NAME[afresource.PENDING])
        elif failed == 0:
            c = "pass"
            msg = _(afresource.TEST_STATUS_NAME[afresource.PASSED])
        else:
            c = "fail"
            msg = _(afresource.TEST_STATUS_NAME[afresource.FAILED])
        node = self._createElement('div', {'class': 'testrunsummary'})
        msg = '%s: %s' % (_("Overall result"), msg)
        subnode = self._createTextElement('p', msg, {'class' : c})
        node.appendChild(subnode)
        table = self._createElement('table', {'class': 'aftable'})
        node.appendChild(table)
        for label, href, s in zip(labels, hrefs, status):
            if href != '':
                subnode = self._createTextElement('a', label, {'href' : href})
            else:
                subnode = label
            table.appendChild(self._createTableRow(subnode, str(s)))
        return node


    def renderTestcases(self):
        headings = (_('Failed test cases'), _('Skipped test cases'), _('Pending test cases'), _('Passed test cases'))
        hrefs  = ('failedtestcases', 'skippedtestcases', 'pendingtestcases', 'passedtestcases')
        flags = (afresource.FAILED, afresource.SKIPPED, afresource.PENDING, afresource.PASSED)
        node = self._createElement('div')
        for heading, flag, href in zip(headings, flags, hrefs):
            node.appendChild(self._createHeadline('h1', heading, {'name': href}))
            id_list = self.model.getTestcaseIDs(flag)
            if len(id_list) <= 0:
                node.appendChild(self._createTextElement('p', _('None')))
                continue
            for tc_id in id_list:
                testcase = self.model.getTestcase(tc_id)
                basedata = testcase.getPrintableDataDict()
                node.appendChild(self._createTextElement('h2', 'TC-%(ID)03d: %(title)s' % basedata))
                table = self._createElement('table', {'class': 'aftable'})
                node.appendChild(table)
                table.appendChild(self._createTableRow(_('Result'),      basedata['testresult']))
                table.appendChild(self._createTableRow(_('Action'),      self._render(basedata['action'])))
                table.appendChild(self._createTableRow(_('Remark'),      self._render(basedata['testremark'])))
                table.appendChild(self._createTableRow(_('Time stamp'),  basedata['timestamp']))
                self._renderTestcaseBasedata(table, basedata)
        return node


def doExportHTML(path, model, cssfile):
    export = trExportHTML(model, cssfile)
    export.run()
    export.write(path)


class CommandLineProcessor(afexporthtml.CommandLineProcessor):
    def run(self):
        logging.basicConfig(level=afconfig.loglevel, format=afconfig.logformat)
        logging.disable(afconfig.loglevel)

        model = trmodel.trModel()
        try:
            cwd = os.getcwd()
            model.OpenTestrun(self.databasename)
            os.chdir(cwd)
        except:
            print("Error opening database file %s" % self.databasename)
            print(sys.exc_info())
            sys.exit(1)

        doExportHTML(self.output, model, self.stylesheet)


if __name__=="__main__":
    clp = CommandLineProcessor(afresource.getDefaultCSSFile())
    clp.parseOpts()
    clp.run()






