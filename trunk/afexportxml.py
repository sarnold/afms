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

import os, sys, getopt
if __name__=="__main__":
    import sys, gettext
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)
import codecs, logging
from xml.dom.minidom import getDOMImplementation, XMLNS_NAMESPACE, parseString, parse
from time import localtime, gmtime, strftime
import afmodel, afconfig, afresource, _afartefact, _afhtmlwindow
from afresource import ENCODING
from afexporthtml import afExportXMLBase



class afExportXML(afExportXMLBase):
    def __init__(self, model, stylesheet, title='AFMS Report'):
        self.model = model
        self.title = title
        self.encoding = 'UTF-8'

        self.impl = getDOMImplementation()
        self.xmldoc = self.impl.createDocument(None, "artefacts", None)
        self.root = self.xmldoc.documentElement
        self.root.setAttribute('source', self.model.getFilename())
        self.root.setAttribute('creationdate', strftime(afresource.TIME_FORMAT, localtime()))
        if len(stylesheet) > 0:
            stylesheet = self.xmldoc.createProcessingInstruction('xml-stylesheet', 'type="text/xsl" href="%s"' % stylesheet)
            self.xmldoc.insertBefore(stylesheet, self.root)


    def run(self):
        # --- Product information ---
        node = self.renderProductInformation()
        self.root.appendChild(node)

        # --- Text sections ---
        idlist = self.model.getSimpleSectionIDs()
        for id in idlist:
            node = self.renderSimpleSection(id)
            self.root.appendChild(node)

        # --- Glossary ---
        cursor = self.model.connection.cursor()
        # SQL query for demonstration purposes only
        cursor.execute('select ID from glossary where delcnt==0 order by title;')
        for id in [item[0] for item in cursor.fetchall()]:
            node = self.renderGlossaryEntry(id)
            self.root.appendChild(node)

        # --- Features ---
        idlist = self.model.getFeatureIDs()
        for id in idlist:
           node = self.renderFeature(id)
           self.root.appendChild(node)

        # --- Requirements ---
        idlist = self.model.getRequirementIDs()
        for id in idlist:
           node = self.renderRequirement(id)
           self.root.appendChild(node)

        # --- Testcases ---
        idlist = self.model.getTestcaseIDs()
        for id in idlist:
           node = self.renderTestcase(id)
           self.root.appendChild(node)

        # --- Usecases ---
        idlist = self.model.getUsecaseIDs()
        for id in idlist:
           node = self.renderUsecase(id)
           self.root.appendChild(node)

        # --- Usecases ---
        idlist = self.model.getTestsuiteIDs()
        for id in idlist:
           node = self.renderTestsuite(id)
           self.root.appendChild(node)


    def renderProductInformation(self):
        productinfo = self.model.getProductInformation()
        node = self._createElement('productinformation')
        node.appendChild(self._createTextElement('title', productinfo['title']))
        node.appendChild(self._render(productinfo['description'], enclosingtag='description'))
        return node


    def renderSimpleSection(self, ID):
        simplesection = self.model.getSimpleSection(ID)
        node = self._createElement('simplesection', {'ID' : str(ID)})
        node.appendChild(self._createTextElement('title', simplesection['title']))
        node.appendChild(self._render(simplesection['content'], enclosingtag='content'))
        changelognode = self.renderChangelist(simplesection)
        node.appendChild(changelognode)
        return node


    def renderGlossaryEntry(self, ID):
        glossaryentry = self.model.getGlossaryEntry(ID)
        node = self._createElement('glossaryentry', {'ID' : str(ID)})
        node.appendChild(self._createTextElement('title', glossaryentry['title']))
        node.appendChild(self._render(glossaryentry['description'], enclosingtag='description'))
        return node


    def renderFeature(self, ID):
        feature = self.model.getFeature(ID)
        basedata = feature.getPrintableDataDict()
        node = self._createElement('feature', {'ID' : str(ID)})
        for key in ('priority', 'status', 'version', 'risk'):
            node.appendChild(self._createTextElement(key, basedata[key]))
        node.appendChild(self._render(basedata['description'], enclosingtag='description'))
        node.appendChild(self.renderRelatedArtefacts('relatedrequirements', feature.getRelatedRequirements()))
        node.appendChild(self.renderChangelist(feature))
        return node


    def renderRequirement(self, ID):
        requirement = self.model.getRequirement(ID)
        basedata = requirement.getPrintableDataDict()
        node = self._createElement('requirement', {'ID': str(ID)})
        for key in ('priority', 'status', 'version', 'complexity', 'assigned', 'effort', 'category'):
            node.appendChild(self._createTextElement(key,    basedata[key]))
        for key in ('description', 'origin', 'rationale'):
            node.appendChild(self._render(basedata[key], enclosingtag=key))
        node.appendChild(self.renderRelatedArtefacts('relatedfeatures', requirement.getRelatedFeatures()))
        node.appendChild(self.renderRelatedArtefacts('relatedrequirements', requirement.getRelatedRequirements()))
        node.appendChild(self.renderRelatedArtefacts('relatedusecases', requirement.getRelatedUsecases()))
        node.appendChild(self.renderRelatedArtefacts('relatedtestcases', requirement.getRelatedTestcases()))
        node.appendChild(self.renderChangelist(requirement))
        return node


    def renderTestcase(self, ID):
        testcase = self.model.getTestcase(ID)
        basedata = testcase.getPrintableDataDict()
        node = self._createElement('testcase', {'ID': str(ID)})
        node.appendChild(self._createTextElement('title',    basedata['title']))
        node.appendChild(self._createTextElement('version',    basedata['version']))
        for key in ('purpose', 'prerequisite', 'testdata', 'steps', 'scripturl', 'notes'):
            node.appendChild(self._render(basedata[key], enclosingtag=key))
        node.appendChild(self.renderRelatedArtefacts('relatedrequirements', testcase.getRelatedRequirements()))
        node.appendChild(self.renderRelatedArtefacts('relatedtestsuites', testcase.getRelatedTestsuites()))
        node.appendChild(self.renderChangelist(testcase))
        return node


    def renderUsecase(self, ID):
        usecase = self.model.getUsecase(ID)
        basedata = usecase.getPrintableDataDict()
        node = self._createElement('usecase', {'ID': str(ID)})
        for key in ('title', 'priority', 'usefrequency', 'actors', 'stakeholders'):
            node.appendChild(self._createTextElement(key, basedata[key]))
        for key in ('prerequisites', 'mainscenario', 'altscenario', 'notes'):
            node.appendChild(self._render(basedata[key], enclosingtag=key))
        node.appendChild(self.renderRelatedArtefacts('relatedrequirements', usecase.getRelatedRequirements()))
        node.appendChild(self.renderChangelist(usecase))
        return node


    def renderTestsuite(self, ID):
        testsuite = self.model.getTestsuite(ID)
        basedata = testsuite.getPrintableDataDict()
        node = self._createElement('testsuite', {'ID': str(ID)})
        for key in ('title', 'execorder', 'nbroftestcase'):
            node.appendChild(self._createTextElement(key, basedata[key]))
        node.appendChild(self._render(basedata['description'], enclosingtag='description'))
        node.appendChild(self.renderRelatedArtefacts('relatedtestcases', testsuite.getRelatedTestcases()))
        return node


    def renderRelatedArtefacts(self, nodename, artefactlist):
        node = self._createElement(nodename)
        for artefact in artefactlist:
            node.appendChild(self._createTextElement('ID', str(artefact['ID'])))
        return node


    def renderChangelist(self, artefact):
        node = self._createElement('changelist')
        changelist = artefact.getChangelist()
        for changelogentry in changelist:
            basedata = changelogentry.getPrintableDataDict()
            subnode = self._createElement('changelogentry', {'ID': str(basedata['ID'])})
            subnode.appendChild(self._createTextElement('user', str(basedata['user'])))
            subnode.appendChild(self._render(basedata['description'], enclosingtag='description'))
            subnode.appendChild(self._createTextElement('changetype', str(basedata['changetype'])))
            subnode.appendChild(self._createTextElement('date', basedata['date']))
            node.appendChild(subnode)
        return node


def doExportXML(path, model, stylesheet):
    export = afExportXML(model, stylesheet)
    export.run()
    export.write(path)


class CommandLineProcessor():
    def __init__(self, stylesheet):
        self.stylesheet = stylesheet
        self.output = None


    def version(self):
        print("Version unknown")
        

    def usage(selg):
        print("Usage:\n%s [-h|--help] [-V|--version] [-s <xslfile>|--stylesheet=<xslfile>] [-o <ofile>|--output=<ofile>] <ifile>\n"
        "  -h, --help                             show help and exit\n"
        "  -V, --version                          show version and exit\n"
        "  -s <xslfile>, --stylesheet=<xslfile>   include xsl stylesheet\n"
        "  -o <ofile>, --output=<ofile>           output to file <ofile>\n"
        "  <ifile>                                database file"
        % os.path.basename(sys.argv[0]))


    def parseOpts(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ho:s:V", ["help", "output=", "stylesheet=", "version"])
        except getopt.GetoptError, err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"
            self.usage()
            sys.exit(2)
        for o, a in opts:
            if o in ("-V", "--version"):
                self.version()
                sys.exit()
            elif o in ("-h", "--help"):
                self.usage()
                sys.exit()
            elif o in ("-o", "--output"):
                self.output = a
            elif o in ("-s", "--stylesheet"):
                self.stylesheet = a
            else:
                assert False, "unhandled option"

        if len(args) != 1:
            self.usage()
            sys.exit(1)
            
        if self.output is None:
            self.output =  os.path.splitext(args[0])[0] + ".xml"
            
        self.databasename = args[0]
        
        
    def run(self):
        logging.basicConfig(level=afconfig.loglevel, format=afconfig.logformat)
        logging.disable(afconfig.loglevel)

        model = afmodel.afModel(controller = None)
        try:
            cwd = os.getcwd()
            model.requestOpenProduct(self.databasename)
            os.chdir(cwd)
        except:
            print("Error opening database file %s" % self.databasename)
            sys.exit(1)


        doExportXML(self.output, model, self.stylesheet)


if __name__=="__main__":
    clp = CommandLineProcessor(afresource.getDefaultXSLFile())
    clp.parseOpts()
    clp.run()

