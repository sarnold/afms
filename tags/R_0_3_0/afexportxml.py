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

import os
if __name__=="__main__":
    import sys, gettext
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)

import codecs
from time import localtime, gmtime, strftime
import afmodel
import afconfig, afresource
from afresource import ENCODING


class afExportXML():
    def __init__(self, outfilename, model):
        self.model = model
        self.of = codecs.open(outfilename, encoding=ENCODING, mode="w", errors='strict')
        self.writeXMLHeader()
        self.writeProductInfo()
        self.writeSimpleSections()
        self.writeGlossary()
        self.writeFeatures()
        self.writeRequirements()
        self.writeTestcases()
        self.writeTestsuites()
        self.writeRelations()
        self.writeXMLFooter()
        self.of.close()


    def writeXMLHeader(self):
        self.of.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.of.write('<!-- Created from %s at %s !-->\n' % (self.model.getFilename(), strftime(afresource.TIME_FORMAT, localtime())))
        self.of.write('<product>\n')


    def writeXMLFooter(self):
        self.of.write('</product>\n')


    def writeTag(self, tag, content):
        self.of.write("<%s><![CDATA[%s]]></%s>\n" % (tag, content, tag))


    def writeSimpleTag(self, tag, content):
        self.of.write("<%s>%s</%s>\n" % (tag, content, tag))


    def writeProductInfo(self):
        pi = self.model.getProductInformation()
        self.writeTag('producttitle', pi['title'])
        self.writeTag('productdescription', pi['description'])


    def writeSimpleSections(self):
        idlist = self.model.getSimpleSectionIDs()
        self.of.write('<simplesections>\n')
        for ID in idlist:
            simplesection = self.model.getSimpleSection(ID)
            self.of.write(simplesection.xmlrepr('simplesection'))
        self.of.write('</simplesections>\n')


    def writeGlossary(self):
            idlist = self.model.getGlossaryEntryIDs()
            self.of.write('<glossary>\n')
            for ID in idlist:
                glossaryentry = self.model.getGlossaryEntry(ID)
                self.of.write(glossaryentry.xmlrepr('glossaryentry'))
            self.of.write('</glossary>\n')


    def writeFeatures(self):
        idlist = self.model.getFeatureIDs()
        self.of.write('<features>\n')
        for ID in idlist:
            feature = self.model.getFeature(ID)
            self.of.write(feature.xmlrepr())
        self.of.write('</features>\n')


    def writeRequirements(self):
        idlist = self.model.getRequirementIDs()
        self.of.write('<requirements>\n')
        for ID in idlist:
            requirement = self.model.getRequirement(ID)
            self.of.write(requirement.xmlrepr())
        self.of.write('</requirements>\n')


    def writeUsecase(self, uc_id):
        idlist = self.model.getUsecaseIDs()
        self.of.write('<usecases>\n')
        for ID in idlist:
            usecase = self.model.getUsecase(ID)
            self.of.write(usecase.xmlrepr())
        self.of.write('</usecases>\n')


    def writeTestcases(self):
        idlist = self.model.getTestcaseIDs()
        self.of.write('<testcases>\n')
        for ID in idlist:
            testcase = self.model.getTestcase(ID)
            self.of.write(testcase.xmlrepr())
        self.of.write('</testcases>\n')


    def writeTestsuites(self):
        idlist = self.model.getTestsuiteIDs()
        self.of.write('<testsuites>\n')
        for ID in idlist:
            testsuite = self.model.getTestsuite(ID)
            self.of.write(testsuite.xmlrepr())
        self.of.write('</testsuites>\n')


    def writeRelations(self):
        data = [\
            {   'func'          : self.model.getFeatureRequirementRelations,
                'outertag'      : 'feature_requirement_relations',
                'innerlefttag'  : 'feature_id',
                'innerrighttag' : 'requirement_id'
            },
            {   'func'          : self.model.getTestsuiteTestcaseRelations,
                'outertag'      : 'testsuite_testcase_relations',
                'innerlefttag'  : 'testsuite_id',
                'innerrighttag' : 'testcase_id'
            },
            {   'func'         : self.model.getRequirementUsecaseRelations,
                'outertag'      : 'requirement_usecase_relations',
                'innerlefttag'  : 'requirement_id',
                'innerrighttag' : 'usecase_id'
            },
            {   'func'          : self.model.getRequirementTestcaseRelations,
                'outertag'      : 'requirement_testcase_relations',
                'innerlefttag'  : 'requirement_id',
                'innerrighttag' : 'testcase_id'
            }]

        for d in data:
            self.of.write('<%s>\n' % d["outertag"])
            relations = d["func"]()
            for r in relations:
                self.of.write('<relation>\n')
                self.writeSimpleTag(d['innerlefttag'], r[0])
                self.writeSimpleTag(d['innerrighttag'], r[1])
                self.of.write('</relation>\n')
            self.of.write('</%s>\n' % d["outertag"])



if __name__=="__main__":
    import os, sys, getopt

    def version():
        print("Version unknown")

    def usage():
        print("Usage:\n%s [-h|--help] [-V|--version] [-o <ofile>|--output=<ofile>] <ifile>\n"
        "  -h, --help                      show help and exit\n"
        "  -V, --version                   show version and exit\n"
        "  -o <ofile>, --output=<ofile>    output to file <ofile>\n"
        "  <ifile>                         database file"
        % sys.argv[0])


    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:V", ["help", "output=", "version"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    for o, a in opts:
        if o in ("-V", "--version"):
            version()
            sys.exit()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    if len(args) != 1:
        usage()
        sys.exit(1)

    model = afmodel.afModel(controller = None)
    try:
        cwd = os.getcwd()
        model.requestOpenProduct(args[0])
        os.chdir(cwd)
    except:
        print("Error opening database file %s" % args[0])
        sys.exit(1)

    if output is None:
        output =  os.path.splitext(args[0])[0] + ".html"

    export = afExportXML(output, model)
