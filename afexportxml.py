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

from time import localtime, gmtime, strftime
import afmodel
import afconfig, afresource


class afExportXML():
    def __init__(self, outfilename, model):
        self.model = model
        self.of = open(outfilename, "w")
        self.writeXMLHeader()
        self.writeProductInfo()
        self.writeFeatures()
        self.writeRequirements()
        self.writeTestcases()
        self.writeTestsuites()
        self.writeRelations()
        self.writeXMLFooter()
        self.of.close()
        

    def writeXMLHeader(self):
        self.of.write('<?xml version="1.0" encoding="UTF-8"?>')
        self.of.write('<!-- Created from %s at %s !-->' % (self.model.getFilename(), strftime(afresource.TIME_FORMAT, localtime())))
        self.of.write('<product>')
        

    def writeXMLFooter(self):
        self.of.write('</product>')
        
        
    def writeTag(self, tag, content):
        self.of.write("<%s><![CDATA[%s]]></%s>" % (tag, content, tag))


    def writeSimpleTag(self, tag, content):
        self.of.write("<%s>%s</%s>" % (tag, content, tag))


    def writeProductInfo(self):
        pi = self.model.getProductInformation()
        self.writeTag('producttitle', pi['title'])
        self.writeTag('productdescription', pi['description'])
        
        
    def writeFeatures(self):
        columnnames = 'id title priority status version risk description'.split()
        idlist = self.model.getFeatureIDs()
        self.of.write('<features>\n')
        for ID in idlist:
            basedata = self.model.getFeature(ID)[0]
            self.of.write('<feature>\n')
            for left, right in zip(columnnames, basedata):
                self.writeTag(left, right)
            self.of.write('</feature>\n')
        self.of.write('</features>\n')


    def writeRequirements(self):
        columnnames = 'id title priority status version complexity assigned effort category origin rationale description'.split()
        idlist = self.model.getRequirementIDs()
        self.of.write('<requirements>\n')
        for ID in idlist:
            basedata = self.model.getRequirement(ID)[0]
            self.of.write('<requirement>\n')
            for left, right in zip(columnnames, basedata):
                self.writeTag(left, right)
            self.of.write('</requirement>\n')
        self.of.write('</requirements>\n')
        
                
    def writeUsecase(self, uc_id):
        columnnames = ['id', 'title', 'priority', 'usefrequency', 'actors', 'stakeholders', 'prerequisites', 'mainscenario', 'altscenario', 'notes']
        idlist = self.model.getUsecaseIDs()
        self.of.write('<usecases>\n')
        for ID in idlist:
            basedata = self.model.getUsecase(uc_id)[0]
            self.of.write('<usecase>\n')
            for left, right in zip(columnnames, basedata):
                self.of.write(left, right)
            self.of.write('</usecase>\n')
        self.of.write('</usecases>\n')
        
        
    def writeTestcases(self):
        columnnames = "id title version purpose prerequisite testdata steps notes".split()
        idlist = self.model.getTestcaseIDs()
        self.of.write('<testcases>\n')
        for ID in idlist:
            basedata = self.model.getTestcase(ID)[0]
            self.of.write('<testcase>\n')
            for left, right in zip(columnnames, basedata):
                self.writeTag(left, right)
            self.of.write('</testcase>\n')
        self.of.write('</testcases>\n')
        

    def writeTestsuites(self):
        columnnames = "id title description".split()
        idlist = self.model.getTestsuiteIDs()
        self.of.write('<testsuites>\n')
        for ID in idlist:
            (basedata, includedtestcaselist, excludedtestcaselist) = self.model.getTestsuite(ID)
            self.of.write('<testsuite>\n')
            for left, right in zip(columnnames, basedata):
                self.writeTag(left, right)
            self.of.write('<testcases>\n')
            for tc in includedtestcaselist:
                self.writeTag('id', tc[0])
            self.of.write('</testcases>\n')
            self.of.write('</testsuite>\n')
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
    
    model = afmodel.afModel()
    try:
        model.requestOpenProduct(args[0])
    except:
        print("Error opening database file %s" % args[0])
        sys.exit(1)
    
    if output is None:
        output =  os.path.splitext(args[0])[0] + ".html"
        
    export = afExportXML(output, model)
