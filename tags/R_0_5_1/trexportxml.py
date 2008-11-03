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
Export database to xml output

@author: Achim Koehler
@version: $Rev$
"""

from time import localtime, gmtime, strftime
import logging

if __name__=="__main__":
    import sys, gettext, os, getopt
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)

import trmodel
import afresource, afconfig
import afexportxml


class trExportXML(afexportxml.afExportXML):
    def __init__(self, model, stylesheet, title='AFMS Test Report'):
        afexportxml.afExportXML.__init__(self, model, stylesheet, title)


    def run(self):
        self.root.appendChild(self.renderTestrunInfo())
        self.root.appendChild(self.renderSummary())
        self.root.appendChild(self.renderTestcases())


    def renderTestrunInfo(self):
        info = self.model.getInfo()
        node = self._createElement('testruninfo')
        for key in ("product_title", "description", "testsuite_description"):
            node.appendChild(self._render(info[key], enclosingtag=key))
        for key in ("creation_date", "tester", "afdatabase", "testsuite_id", "testsuite_title", "testsuite_execorder"):
            node.appendChild(self._createTextElement(key, info[key]))
        return node


    def renderSummary(self):
        status = self.model.getStatusSummary()
        (total, pending, failed, skipped) = status
        status = list(status)
        passed = total - pending - failed - skipped
        status.append(passed)
        labels = ('total', 'pending', 'failed', 'skipped', 'passed')
        node = self._createElement('summary')
        node.appendChild(self._createTextElement('overall_passed', str(int(failed == 0))))
        for label, s in zip(labels, status):
            node.appendChild(self._createTextElement(label, str(s)))
        return node


    def renderTestcases(self):
        node = self._createElement('testcases')
        flags = (afresource.FAILED, afresource.SKIPPED, afresource.PENDING, afresource.PASSED)
        labels = ('testcases_failed', 'testcases_skipped', 'testcases_pending', 'testcases_passed')
        for flag, label in zip(flags, labels):
            subnode = self._createElement(label)
            node.appendChild(subnode)
            id_list = self.model.getTestcaseIDs(flag)
            if len(id_list) <= 0:
                continue
            for tc_id in id_list:
                testcase = self.model.getTestcase(tc_id)
                basedata = testcase.getPrintableDataDict()
                tcnode = self._createElement('testcase', {'ID': str(tc_id)})
                subnode.appendChild(tcnode)
                for key in ('action', 'testremark'):
                    tcnode.appendChild(self._render(basedata[key], enclosingtag=key))    
                for key in ('testresult','timestamp'):
                    tcnode.appendChild(self._createTextElement(key, basedata[key]))
                self._renderTestcaseBasedata(tcnode, basedata)
        return node


def doExportXML(path, model, stylesheet):
    export = trExportXML(model, stylesheet)
    export.run()
    export.write(path)


class CommandLineProcessor(afexportxml.CommandLineProcessor):
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

        doExportXML(self.output, model, self.stylesheet)


if __name__=="__main__":
    clp = CommandLineProcessor(afresource.getDefaultXSLFile())
    clp.parseOpts()
    clp.run()

