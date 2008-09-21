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
Export database to html output

@author: Achim Koehler
@version: $Rev$
"""

import os, sys, getopt, gettext
if __name__=="__main__":
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)
import codecs, logging
from xml.dom.minidom import getDOMImplementation, XMLNS_NAMESPACE, parseString, parse
from time import localtime, gmtime, strftime
import afmodel
import afconfig
import afresource, _afartefact
from afresource import ENCODING
import _afhtmlwindow

class afExportXMLBase():
    def write(self, filename):
        f = codecs.open(filename, encoding='UTF-8', mode="w", errors='strict')
        self.xmldoc.writexml(f, indent='', addindent=' '*2, newl='\n', encoding=ENCODING)
        f.close()


    def _createTextElement(self, tagName, text, attribute={}):
        node = self.xmldoc.createElement(tagName)
        for name, value in attribute.iteritems():
            node.setAttribute(name, value)
        node.appendChild(self.xmldoc.createTextNode(text))
        return node


    def _createElement(self, elementname, attribute={}):
        node = self.xmldoc.createElement(elementname)
        for name, value in attribute.iteritems():
            node.setAttribute(name, value)
        return node


    def _render(self, text, maskspecialchars=True, enclosingtag='div'):
        text = _afhtmlwindow.render(text, maskspecialchars, enclosingtag)
        text = '''<?xml version="1.0" encoding="UTF-8" ?>
                <!DOCTYPE xhtml [
                  <!ENTITY nbsp "&#160;">
                ]>'''  + text
        dom = parseString(text.encode('UTF-8'))
        return dom.documentElement


class afExportHTML(afExportXMLBase):
    def __init__(self, model, cssfile, title='AFMS Report'):
        self.model = model
        self.title = title
        self.encoding = 'UTF-8'
        self.cssfile = cssfile
        self.impl = getDOMImplementation()
        doctype = self.getDocType()
        self.xmldoc = self.impl.createDocument(None, "html", doctype)
        self.root = self.xmldoc.documentElement
        self.root.setAttribute('xmlns', 'http://www.w3.org/1999/xhtml')

        self.root.appendChild(self.getHead())
        self.body = self.xmldoc.createElement('body')
        self.root.appendChild(self.body)


    def getDocType(self):
        return self.impl.createDocumentType('html', '-//W3C//DTD XHTML 1.0 Strict//EN', 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd')


    def getHead(self):
        head = self.xmldoc.createElement('head')
        node = self.xmldoc.createElement('meta')
        node.setAttribute('content', "text/xhtml; charset=%s" % self.encoding)
        node.setAttribute('http-equiv', "content-type")
        head.appendChild(node)
        node = self.xmldoc.createElement('title')
        node.appendChild(self.xmldoc.createTextNode(self.title))
        head.appendChild(node)

        node = self.xmldoc.createElement('style')
        node.setAttribute('type', "text/css")
        node.appendChild(self.xmldoc.createTextNode(self.getCSSFile()))
        head.appendChild(node)
        return head


    def run(self):
        node = self._createElement('div', {'id': 'header'})
        node.appendChild(self._createElement('span'))
        self.body.appendChild(node)
        self.toc = self._createElement('div', {'class': 'tableofcontent'})
        self.toc.appendChild(self._createTextElement('h1', _('Table of Contents')))
        self.body.appendChild(self.toc)

        self.changelog = self._createElement('div', {'class': 'changelog'})

        # --- Product information ---
        self.toc.appendChild(self._createHeadline('h2', _('Product information'), {'href': '#productinformation'}))
        self.body.appendChild(self._createHeadline('h1', _('Product information'), {'name': 'productinformation'}))
        node = self.renderProductInformation()
        self.body.appendChild(node)

        # --- Text sections ---
        self.toc.appendChild(self._createHeadline('h2', _('Text sections'), {'href': '#textsections'}))
        self.body.appendChild(self._createHeadline('h1', _('Text sections'), {'name': 'textsections'}))
        idlist = self.model.getSimpleSectionIDs()
        if len(idlist) > 0:
            listnode = self._createElement('ul')
            self.toc.appendChild(listnode)
            for id in idlist:
                (node, tocnode, changelognode) = self.renderSimpleSection(id)
                self.body.appendChild(node)
                self.appendListItem(listnode, tocnode)
                self.changelog.appendChild(changelognode)

        # --- Glossary ---
        self.toc.appendChild(self._createHeadline('h2', _('Terms and Abbreviations'), {'href': '#glossary'}))
        self.body.appendChild(self._createHeadline('h1', _('Terms and Abbreviations'), {'name': 'glossary'}))
        cursor = self.model.connection.cursor()
        # SQL query for demonstration purposes only
        cursor.execute('select ID from glossary where delcnt==0 order by title;')
        idlist = [item[0] for item in cursor.fetchall()]
        if len(idlist) > 0:
            listnode = self._createElement('dl', {'class': 'glossary'})
            self.body.appendChild(listnode)
            for id in idlist:
                (termnode, descnode) = self.renderGlossaryEntry(id)
                listnode.appendChild(termnode)
                listnode.appendChild(descnode)

        # --- Features ---
        self.toc.appendChild(self._createHeadline('h2', _('Features'), {'href': '#features'}))
        self.body.appendChild(self._createHeadline('h1', _('Features'), {'name': 'features'}))
        idlist = self.model.getFeatureIDs()
        if len(idlist) > 0:
            listnode = self._createElement('ul')
            self.toc.appendChild(listnode)
            for id in idlist:
                (node, tocnode, changelognode) = self.renderFeature(id)
                self.body.appendChild(node)
                self.appendListItem(listnode, tocnode)
                self.changelog.appendChild(changelognode)

        # --- Requirements ---
        self.toc.appendChild(self._createHeadline('h2', _('Requirements'), {'href': '#requirements'}))
        self.body.appendChild(self._createHeadline('h1', _('Requirements'), {'name': 'requirements'}))
        cursor = self.model.connection.cursor()
        # SQL query for demonstration purposes only
        cursor.execute('select ID from requirements where delcnt==0 order by ID;')
        idlist = [item[0] for item in cursor.fetchall()]
        if len(idlist) > 0:
            listnode = self._createElement('ul')
            self.toc.appendChild(listnode)
            for id in idlist:
                (node, tocnode, changelognode) = self.renderRequirement(id)
                self.body.appendChild(node)
                self.appendListItem(listnode, tocnode)
                self.changelog.appendChild(changelognode)

        # --- Usecases ---
        self.toc.appendChild(self._createHeadline('h2', _('Usecases'), {'href': '#usecases'}))
        self.body.appendChild(self._createHeadline('h1', _('Usecases'), {'name': 'usecases'}))
        idlist = self.model.getUsecaseIDs()
        if len(idlist) > 0:
            listnode = self._createElement('ul')
            self.toc.appendChild(listnode)
            for id in idlist:
                (node, tocnode, changelognode) = self.renderUsecase(id)
                self.body.appendChild(node)
                self.appendListItem(listnode, tocnode)
                self.changelog.appendChild(changelognode)

        # --- Testcases ---
        self.toc.appendChild(self._createHeadline('h2', _('Testcases'), {'href': '#testcases'}))
        self.body.appendChild(self._createHeadline('h1', _('Testcases'), {'name': 'testcases'}))
        idlist = self.model.getTestcaseIDs()
        if len(idlist) > 0:
            listnode = self._createElement('ul')
            self.toc.appendChild(listnode)
            for id in idlist:
                (node, tocnode, changelognode) = self.renderTestcase(id)
                self.body.appendChild(node)
                self.appendListItem(listnode, tocnode)
                self.changelog.appendChild(changelognode)

        # --- Testsuites ---
        self.toc.appendChild(self._createHeadline('h2', _('Testsuites'), {'href': '#testsuites'}))
        self.body.appendChild(self._createHeadline('h1', _('Testsuites'), {'name': 'testsuites'}))
        idlist = self.model.getTestsuiteIDs()
        if len(idlist) > 0:
            listnode = self._createElement('ul')
            self.toc.appendChild(listnode)
            for id in idlist:
                (node, tocnode) = self.renderTestsuite(id)
                self.body.appendChild(node)
                self.appendListItem(listnode, tocnode)

        # -- Problem reports ---
        self.toc.appendChild(self._createHeadline('h2', _('Detected problems'), {'href': '#problems'}))
        self.body.appendChild(self._createHeadline('h1', _('Detected problems'), {'name': 'problems'}))
        hrefs  = ("lonelyfeatures","untestedrequirements", "lonelytestcases","unexecutedtestcases","emptytestsuites","lonelyusecases")
        labels = (_('Features without requirements'), _('Requirements without testcases'), _('Testcases not belonging to requirements'), _('Testcases not belonging to testsuites'), _('Empty testsuites'), _('Usecases not belonging to features or requirements'))
        getIDFuncs = (self.model.getIDofFeaturesWithoutRequirements, self.model.getIDofRequirementsWithoutTestcases,
                     self.model.getIDofTestcasesWithoutRequirements, self.model.getIDofTestcasesWithoutTestsuites,
                     self.model.getIDofTestsuitesWithoutTestcases, self.model.getIDofUsecasesWithoutArtefacts)
        getAFFuncs = (self.model.getFeature, self.model.getRequirement, self.model.getTestcase,
                     self.model.getTestcase, self.model.getTestsuite, self.model.getUsecase)
        renderFuncs = (self.renderFeatureAnchor, self.renderRequirementAnchor, self.renderTestcaseAnchor,
                      self.renderTestcaseAnchor, self.renderTestsuiteAnchor, self.renderUsecaseAnchor)

        tocnode = self._createElement('ul')
        for href, label, getIDFunc, getAFFunc, renderFunc in zip(hrefs, labels, getIDFuncs, getAFFuncs, renderFuncs):
            subnode = self._createElement('li')
            subnode.appendChild(self._createTextElement('a', label, {'href': '#' + href}))
            tocnode.appendChild(subnode)

            node = self._createElement('h2')
            node.appendChild(self._createTextElement('a', label, {'name': href}))
            self.body.appendChild(node)
            idlist = getIDFunc()
            if len(idlist) == 0:
                subnode = self._createElement('p')
                spannode = self._createTextElement('span', _('None'), {'class': 'pass'})
                subnode.appendChild(spannode)
            else:
                subnode = self._createElement('ul')
                for id in idlist:
                    self.appendListItem(subnode, renderFunc(getAFFunc(id), True))
            self.body.appendChild(subnode)
        self.toc.appendChild(tocnode)

        # --- Changelog ---
        self.toc.appendChild(self._createHeadline('h2', _('Changelog'), {'href': '#changelog'}))
        self.body.appendChild(self._createHeadline('h1', _('Changelog'), {'name': 'changelog'}))
        self.body.appendChild(self.changelog)

        # --- Footer ---
        self.body.appendChild(self._createElement('hr'))
        footer = _('Created from %s at %s by %s') % (self.model.getFilename(), strftime(afresource.TIME_FORMAT, localtime()), afconfig.CURRENT_USER)
        self.body.appendChild(self._createTextElement('p', footer, {'class': 'footer'}))


    def _createHeadline(self, tagName, text, attribute):
        node = self._createElement(tagName)
        node.appendChild(self._createTextElement('a', text, attribute))
        return node


    def appendListItem(self, listnode, itemnode):
        listitemnode = self._createElement('li')
        listitemnode.appendChild(itemnode)
        listnode.appendChild(listitemnode)


    def renderGlossaryEntry(self, id):
        glossaryentry = self.model.getGlossaryEntry(id)
        termnode = self._createElement('dt')
        termnode.appendChild(self._createTextElement('p', '[GE-%03d]' % glossaryentry['ID'], {'class': 'glossaryid'}))
        subnode = self._createElement('p', {'class': 'glossarytitle'})
        subnode.appendChild(self._createTextElement('span', glossaryentry['title'], {'class': 'glossarytitle'}))
        termnode.appendChild(subnode)
        descnode = self._createElement('dd')
        subnode = self._render(glossaryentry['description'])
        subnode.setAttribute('class', 'glossarydescription')
        descnode.appendChild(subnode)
        return (termnode, descnode)


    def renderProductInformation(self):
        productinfo = self.model.getProductInformation()
        node = self._createElement('div', {'class': 'productinfo'})
        node.appendChild(self._createTextElement('div', productinfo['title'], {'class': 'producttitle'}))
        node.appendChild(self._render(productinfo['description']))
        return node


    def renderSimpleSection(self, ID):
        simplesection = self.model.getSimpleSection(ID)
        node = self._createElement('div', {'class': 'simplesection'})
        subnode = self._createElement('h2')
        subnode.appendChild(self._createTextElement('a', 'SS-%(ID)03d: %(title)s' % simplesection, {'name': 'SS-%(ID)03d' % simplesection}))
        node.appendChild(subnode)
        node.appendChild(self._render(simplesection['content']))
        tocnode = self._createTextElement('a', 'SS-%(ID)03d: %(title)s' % simplesection, {'href': '#SS-%(ID)03d' % simplesection})
        (changelognode, changeloglink) = self.renderChangelist('SS', simplesection)
        node.appendChild(changeloglink)
        return (node, tocnode, changelognode)


    def renderFeature(self, ID):
        feature = self.model.getFeature(ID)
        basedata = feature.getPrintableDataDict()
        node = self._createElement('div', {'class': 'feature'})
        subnode = self._createElement('h2')
        subnode.appendChild(self.renderFeatureAnchor(feature, False))
        node.appendChild(subnode)

        table = self._createElement('table', {'class': 'aftable'})
        node.appendChild(table)

        table.appendChild(self._createTableRow(_('Description'), self._render(basedata['description'])))
        table.appendChild(self._createTableRow(_('Priority'),    basedata['priority']))
        table.appendChild(self._createTableRow(_('Status'),      basedata['status']))
        table.appendChild(self._createTableRow(_('Version'),     basedata['version']))
        table.appendChild(self._createTableRow(_('Risk'),        basedata['risk']))

        relatedrequirements = feature.getRelatedRequirements()
        if len(relatedrequirements) == 0:
            subnode = self._createTextElement('div', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for requirement in relatedrequirements:
                self.appendListItem(subnode, self.renderRequirementAnchor(requirement, True))
        table.appendChild(self._createTableRow(_('Related Requirements'), subnode))

        relatedusecases = feature.getRelatedUsecases()
        if len(relatedusecases) == 0:
            subnode = self._createTextElement('div', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for usecase in relatedusecases:
                self.appendListItem(subnode, self.renderUsecaseAnchor(usecase, True))
        table.appendChild(self._createTableRow(_('Related Usecases'), subnode))

        tocnode = self.renderFeatureAnchor(feature, True)
        (changelognode, changeloglink) = self.renderChangelist('FT', feature)
        node.appendChild(changeloglink)
        return (node, tocnode, changelognode)


    def renderFeatureAnchor(self, feature, href):
        if href:
            attribute = {'href': '#FT-%(ID)03d' % feature}
        else:
            attribute = {'name': 'FT-%(ID)03d' % feature}
        return self._createTextElement('a', 'FT-%(ID)03d: %(title)s' % feature, attribute)


    def renderRequirement(self, ID):
        requirement = self.model.getRequirement(ID)
        basedata = requirement.getPrintableDataDict()
        node = self._createElement('div', {'class': 'requirement'})
        subnode = self._createElement('h2')
        subnode.appendChild(self.renderRequirementAnchor(requirement, False))
        node.appendChild(subnode)

        table = self._createElement('table', {'class': 'aftable'})
        node.appendChild(table)
        table.appendChild(self._createTableRow(_('Description'), self._render(basedata['description'])))
        table.appendChild(self._createTableRow(_('Priority'),    basedata['priority']))
        table.appendChild(self._createTableRow(_('Status'),      basedata['status']))
        table.appendChild(self._createTableRow(_('Version'),     basedata['version']))
        table.appendChild(self._createTableRow(_('Complexity'),  basedata['complexity']))
        table.appendChild(self._createTableRow(_('Assigned'),    basedata['assigned']))
        table.appendChild(self._createTableRow(_('Effort'),      basedata['effort']))
        table.appendChild(self._createTableRow(_('Category'),    basedata['category']))
        table.appendChild(self._createTableRow(_('Origin'),      self._render(basedata['origin'])))
        table.appendChild(self._createTableRow(_('Rationale'),   self._render(basedata['rationale'])))

        relatedfeatures = requirement.getRelatedFeatures()
        if len(relatedfeatures) == 0:
            subnode = self._createTextElement('span', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for feature in relatedfeatures:
                self.appendListItem(subnode, self.renderFeatureAnchor(feature, True))
        table.appendChild(self._createTableRow(_('Related Features'), subnode))

        relatedrequirements = requirement.getRelatedRequirements()
        if len(relatedrequirements) == 0:
            subnode = self._createTextElement('span', _('None'))
        else:
            subnode = self._createElement('ul')
            for rq in relatedrequirements:
                self.appendListItem(subnode, self.renderRequirementAnchor(rq, True))
        table.appendChild(self._createTableRow(_('Related Requirements'), subnode))

        relatedusecases = requirement.getRelatedUsecases()
        if len(relatedusecases) == 0:
            subnode = self._createTextElement('span', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for usecase in relatedusecases:
                self.appendListItem(subnode, self.renderUsecaseAnchor(usecase, True))
        table.appendChild(self._createTableRow(_('Attached Usecases'), subnode))

        relatedtestcases = requirement.getRelatedTestcases()
        if len(relatedtestcases) == 0:
            subnode = self._createTextElement('span', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for testcase in relatedtestcases:
                self.appendListItem(subnode, self.renderTestcaseAnchor(testcase, True))
        table.appendChild(self._createTableRow(_('Attached Testcases'), subnode))

        tocnode = self.renderRequirementAnchor(requirement, True)
        (changelognode, changeloglink) = self.renderChangelist('REQ', requirement)
        node.appendChild(changeloglink)
        return (node, tocnode, changelognode)


    def renderRequirementAnchor(self, requirement, href):
        if href:
            attribute = {'href': '#REQ-%(ID)03d' % requirement}
        else:
            attribute = {'name': 'REQ-%(ID)03d' % requirement}
        return self._createTextElement('a', 'REQ-%(ID)03d: %(title)s' % requirement, attribute)


    def renderUsecase(self, ID):
        usecase = self.model.getUsecase(ID)
        basedata = usecase.getPrintableDataDict()
        node = self._createElement('div', {'class': 'usecase'})
        subnode = self._createElement('h2')
        subnode.appendChild(self.renderUsecaseAnchor(usecase, False))
        node.appendChild(subnode)

        table = self._createElement('table', {'class': 'aftable'})
        node.appendChild(table)
        table.appendChild(self._createTableRow(_('Priority'),      basedata['priority']))
        table.appendChild(self._createTableRow(_('Use frequency'), basedata['usefrequency']))
        table.appendChild(self._createTableRow(_('Actors'),        basedata['actors']))
        table.appendChild(self._createTableRow(_('Stakeholders'),  basedata['stakeholders']))
        table.appendChild(self._createTableRow(_('Prerequisites'), self._render(basedata['prerequisites'])))
        table.appendChild(self._createTableRow(_('Main scenario'), self._render(basedata['mainscenario'])))
        table.appendChild(self._createTableRow(_('Alt scenario'),  self._render(basedata['altscenario'])))
        table.appendChild(self._createTableRow(_('Notes'),         self._render(basedata['notes'])))

        relatedrequirements = usecase.getRelatedRequirements()
        relatedfeatures = usecase.getRelatedFeatures()

        if len(relatedrequirements) == 0:
            if len(relatedfeatures) == 0:
                attrib = {'class': 'alert'}
            else:
                attrib = {}
            subnode = self._createTextElement('span', _('None'), attrib)
        else:
            subnode = self._createElement('ul')
            for requirement in relatedrequirements:
                self.appendListItem(subnode, self.renderRequirementAnchor(requirement, True))
        table.appendChild(self._createTableRow(_('Related Requirements'), subnode))

        relatedfeatures = usecase.getRelatedFeatures()
        if len(relatedfeatures) == 0:
            if len(relatedrequirements) == 0:
                attrib = {'class': 'alert'}
            else:
                attrib = {}
            subnode = self._createTextElement('span', _('None'), attrib)
        else:
            subnode = self._createElement('ul')
            for feature in relatedfeatures:
                self.appendListItem(subnode, self.renderFeatureAnchor(feature, True))
        table.appendChild(self._createTableRow(_('Related Features'), subnode))

        tocnode = self.renderUsecaseAnchor(usecase, True)
        (changelognode, changeloglink) = self.renderChangelist('UC', usecase)
        node.appendChild(changeloglink)
        return (node, tocnode, changelognode)


    def renderUsecaseAnchor(self, usecase, href):
        if href:
            attribute = {'href': '#UC-%(ID)03d' % usecase}
        else:
            attribute = {'name': 'UC-%(ID)03d' % usecase}
        return self._createTextElement('a', 'UC-%(ID)03d: %(title)s' % usecase, attribute)


    def renderTestcase(self, ID):
        testcase = self.model.getTestcase(ID)
        basedata = testcase.getPrintableDataDict()
        node = self._createElement('div', {'class': 'testcase'})
        subnode = self._createElement('h2')
        subnode.appendChild(self.renderTestcaseAnchor(testcase, False))
        node.appendChild(subnode)

        table = self._createElement('table', {'class': 'aftable'})
        node.appendChild(table)
        self._renderTestcaseBasedata(table, basedata)

        relatedrequirements = testcase.getRelatedRequirements()
        if len(relatedrequirements) == 0:
            subnode = self._createTextElement('span', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for requirement in relatedrequirements:
                self.appendListItem(subnode, self.renderRequirementAnchor(requirement, True))
        table.appendChild(self._createTableRow(_('Related Requirements'), subnode))

        relatedtestsuites = testcase.getRelatedTestsuites()
        if len(relatedtestsuites) == 0:
            subnode = self._createTextElement('span', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for testsuite in relatedtestsuites:
                self.appendListItem(subnode, self.renderTestsuiteAnchor(testsuite, True))
        table.appendChild(self._createTableRow(_('Related Testsuites'), subnode))

        tocnode = self.renderTestcaseAnchor(testcase, True)
        (changelognode, changeloglink) = self.renderChangelist('TC', testcase)
        node.appendChild(changeloglink)
        return (node, tocnode, changelognode)


    def renderTestcaseAnchor(self, testcase, href):
        if href:
            attribute = {'href': '#TC-%(ID)03d' % testcase}
        else:
            attribute = {'name': 'TC-%(ID)03d' % testcase}
        return self._createTextElement('a', 'TC-%(ID)03d: %(title)s' % testcase, attribute)
    
    
    def _renderTestcaseBasedata(self, table, basedata):
        table.appendChild(self._createTableRow(_('Version'),      basedata['version']))
        table.appendChild(self._createTableRow(_('Purpose'),      self._render(basedata['purpose'])))
        table.appendChild(self._createTableRow(_('Prerequisite'), self._render(basedata['prerequisite'])))
        table.appendChild(self._createTableRow(_('Testdata'),     self._render(basedata['testdata'])))
        table.appendChild(self._createTableRow(_('Steps'),        self._render(basedata['steps'])))
        table.appendChild(self._createTableRow(_('Script URL'),   basedata['scripturl']))
        table.appendChild(self._createTableRow(_('Notes'),        self._render(basedata['notes'])))
        

    def renderTestsuite(self, ID):
        testsuite = self.model.getTestsuite(ID)
        basedata = testsuite.getPrintableDataDict()
        node = self._createElement('div', {'class': 'testsuite'})
        subnode = self._createElement('h2')
        subnode.appendChild(self.renderTestsuiteAnchor(testsuite, False))
        node.appendChild(subnode)

        table = self._createElement('table', {'class': 'aftable'})
        node.appendChild(table)
        table.appendChild(self._createTableRow(_('Description'),     self._render(basedata['description'])))
        if len(basedata['execorder'].strip()) == 0:
            table.appendChild(self._createTableRow(_("Execution order ID's"), self._createTextElement('span', _('None'))))
        else:
            table.appendChild(self._createTableRow(_("Execution order ID's"), basedata['execorder']))

        relatedtestcases = testsuite.getRelatedTestcases()
        if len(relatedtestcases) == 0:
            subnode = self._createTextElement('span', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for testcase in relatedtestcases:
                self.appendListItem(subnode, self.renderTestcaseAnchor(testcase, True))
        table.appendChild(self._createTableRow(_('Attached Testcases'), subnode))

        tocnode = self.renderTestsuiteAnchor(testsuite, True)
        return (node, tocnode)


    def renderTestsuiteAnchor(self, testsuite, href):
        if href:
            attribute = {'href': '#TS-%(ID)03d' % testsuite}
        else:
            attribute = {'name': 'TS-%(ID)03d' % testsuite}
        return self._createTextElement('a', 'TS-%(ID)03d: %(title)s' % testsuite, attribute)


    def renderChangelist(self, anchorstr, artefact):
        artefact['keystr'] = anchorstr
        node = self._createElement('div')
        headline = self._createElement('h3')
        nameanchor = self._createElement('a', {'name': 'H%s-%03d' % (anchorstr, artefact['ID'])})
        hrefanchor = self._createTextElement('a', '%(keystr)s-%(ID)03d: %(title)s' % artefact, {'href': '#%(keystr)s-%(ID)03d' % artefact})
        nameanchor.appendChild(hrefanchor)
        headline.appendChild(nameanchor)
        node.appendChild(headline)
        changelist = artefact.getChangelist()
        if len(changelist) == 0:
            node.appendChild(self._createTextElement('p', _('None')))
        else:
            attribute = {'class': 'history'}
            table = self._createElement('table', attribute)
            node.appendChild(table)
            tr = self._createElement('tr')
            table.appendChild(tr)
            for label in changelist[0].labels():
                tr.appendChild(self._createTextElement('th', label, attribute))
            for changelogentry in changelist:
                tr = self._createElement('tr')
                table.appendChild(tr)
                basedata = changelogentry.getPrintableDataDict()
                tr.appendChild(self._createTextElement('td', basedata['date'], attribute))
                tr.appendChild(self._createTextElement('td', basedata['user'], attribute))
                td = self._createElement('td', attribute)
                subnode = self._render(basedata['description'])
                subnode.setAttribute('class', 'history')
                td.appendChild(subnode)
                tr.appendChild(td)

        link = self._createElement('p', {'class': 'changeloglink'})
        hrefanchor = self._createTextElement('a', _('Changelog'), {'href': '#H%(keystr)s-%(ID)03d' % artefact})
        link.appendChild(hrefanchor)
        return (node, link)


    def _createTableRow(self, left, right):
        attribute = {'class': 'aftable'}
        tr = self._createElement('tr', attribute)
        if type(left) in [type(''), type(u'')]:
            th = self._createTextElement('th', left, attribute)
        else:
            th = self._createElement('th', attribute)
            th.appendChild(left)
        if type(right) in [type(''), type(u'')]:
            td = self._createTextElement('td', right, attribute)
        else:
            td = self._createElement('td', attribute)
            td.appendChild(right)
        tr.appendChild(th)
        tr.appendChild(td)
        return tr


    def getCSSFile(self):
        if os.path.exists(self.cssfile):
            fp = codecs.open(self.cssfile, encoding='utf-8', errors = 'ignore')
            css = ''
            for line in fp:
                css += line
            fp.close()
        else:
            css = ''
        return css


def doExportHTML(path, model, cssfile):
    export = afExportHTML(model, cssfile)
    export.run()
    export.write(path)


class CommandLineProcessor():
    def __init__(self, stylesheet):
        self.stylesheet = stylesheet
        self.output = None
        self.language = 'en'


    def version(self):
        print("Version unknown")


    def usage(self):
        print("Usage:\n%s [-h|--help] [-V|--version] [-s <cssfile>|--stylesheet=<cssfile>] [-o <ofile>|--output=<ofile>] <ifile>\n"
        "  -h, --help                            show help and exit\n"
        "  -V, --version                         show version and exit\n"
        "  -o <ofile>, --output=<ofile>          output to file <ofile>\n"
        "  -s <cssfile>, --stylesheet=<cssfile>  include cascading stylesheet\n"
        "  -l <lang>, --language=<lang>          select output language (de|en)\n"
        "  <ifile>                               database file"
        % os.path.basename(sys.argv[0]))


    def parseOpts(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hs:o:l:V", ["help", "stylesheet=", "output=", "language=", "version"])
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
            elif o in ("-l", "--language"):
                self.language = a
            elif o in ("-s", "--stylesheet"):
                self.stylesheet = a
            else:
                assert False, "unhandled option"

        if len(args) != 1:
            self.usage()
            sys.exit(1)

        try:
            t = gettext.translation(DOMAIN, LOCALEDIR, languages=[self.language])
            t.install(unicode=True)
        except IOError:
            print('Unsupported language: %s' % self.language)
            sys.exit(1)

        if self.output is None:
            self.output =  os.path.splitext(args[0])[0] + ".html"

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
            print(sys.exc_info())
            sys.exit(1)

        doExportHTML(self.output, model, self.stylesheet)


if __name__=="__main__":
    clp = CommandLineProcessor(afresource.getDefaultCSSFile())
    clp.parseOpts()
    clp.run()
