# -*- coding: utf-8  -*-


# TODO: problem analysis summary: requirements without testcases, features without requirements, ...

import os
if __name__=="__main__":
    import sys, gettext
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)
import codecs
from xml.dom.minidom import getDOMImplementation, XMLNS_NAMESPACE, parseString, parse
from time import localtime, gmtime, strftime
import afmodel
import afconfig
import afresource, _afartefact
from afresource import ENCODING
import _afhtmlwindow 


class afExportHTML():
    def __init__(self, model):
        self.model = model
        self.title='AFMS Report'
        self.encoding = 'UTF-8'
        self.cssfile = 'afmsreport.css'
        
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
        self.toc = self._createElement('div', {'class': 'tableofcontent'})
        self.toc.appendChild(self._createTextElement('h1', _('Table of Contents')))
        self.body.appendChild(self.toc)
        
        # --- Product information ---
        (node, tocnode) = self.renderProductInformation()
        self.body.appendChild(node)
        subnode = self._createElement('h2')
        subnode.appendChild(tocnode)
        self.toc.appendChild(subnode)
        
        # --- Text sections ---
        self.toc.appendChild(self._createTextElement('h2', _('Text sections')))
        self.body.appendChild(self._createTextElement('h1', _('Text sections')))
        listnode = self._createElement('ul')
        self.toc.appendChild(listnode)
        idlist = self.model.getSimpleSectionIDs()
        for id in idlist:
            (node, tocnode) = self.renderSimpleSection(id)
            self.body.appendChild(node)
            self.appendListItem(listnode, tocnode)
            
        # --- Features ---
        self.toc.appendChild(self._createTextElement('h2', _('Features')))
        self.body.appendChild(self._createTextElement('h1', _('Features')))
        listnode = self._createElement('ul')
        self.toc.appendChild(listnode)
        idlist = self.model.getFeatureIDs()
        for id in idlist:
            (node, tocnode) = self.renderFeature(id)
            self.body.appendChild(node)
            self.appendListItem(listnode, tocnode)
        
        # --- Requirements ---
        self.toc.appendChild(self._createTextElement('h2', _('Requirements')))
        self.body.appendChild(self._createTextElement('h1', _('Requirements')))
        listnode = self._createElement('ul')
        self.toc.appendChild(listnode)
        cursor = self.model.connection.cursor()
        # SQL query for demonstration purposes only
        cursor.execute('select ID from requirements where delcnt==0 order by ID;')
        for id in [item[0] for item in cursor.fetchall()]:
            (node, tocnode) = self.renderRequirement(id)
            self.body.appendChild(node)
            self.appendListItem(listnode, tocnode)
            
        # --- Usecases ---
        self.toc.appendChild(self._createTextElement('h2', _('Usecases')))
        self.body.appendChild(self._createTextElement('h1', _('Usecases')))
        listnode = self._createElement('ul')
        self.toc.appendChild(listnode)
        idlist = self.model.getUsecaseIDs()
        for id in idlist:
            (node, tocnode) = self.renderUsecase(id)
            self.body.appendChild(node)
            self.appendListItem(listnode, tocnode)

        # --- Testcases ---
        self.toc.appendChild(self._createTextElement('h2', _('Testcases')))
        self.body.appendChild(self._createTextElement('h1', _('Testcases')))
        listnode = self._createElement('ul')
        self.toc.appendChild(listnode)
        idlist = self.model.getTestcaseIDs()
        for id in idlist:
            (node, tocnode) = self.renderTestcase(id)
            self.body.appendChild(node)
            self.appendListItem(listnode, tocnode)
            
        # --- Testsuites ---
        self.toc.appendChild(self._createTextElement('h2', _('Testsuites')))
        self.body.appendChild(self._createTextElement('h1', _('Testsuites')))
        listnode = self._createElement('ul')
        self.toc.appendChild(listnode)
        idlist = self.model.getTestsuiteIDs()
        for id in idlist:
            (node, tocnode) = self.renderTestsuite(id)
            self.body.appendChild(node)
            self.appendListItem(listnode, tocnode)            
        

    def appendListItem(self, listnode, itemnode):
        listitemnode = self._createElement('li')
        listitemnode.appendChild(itemnode)
        listnode.appendChild(listitemnode)
        
        
    def renderProductInformation(self):
        productinfo = self.model.getProductInformation()
        node = self._createElement('div', {'class': 'productinfo'})
        subnode = self._createElement('h1', {'id': 'productinfo'})
        subnode.appendChild(self._createTextElement('a', _('Product information'), {'name': 'PRODUCTINFO'}))
        node.appendChild(subnode)
        node.appendChild(self._createTextElement('div', productinfo['title'], {'class': 'producttitle'}))
        node.appendChild(self._render(productinfo['description']))
        tocnode = self._createTextElement('a', _('Product information'), {'href': '#PRODUCTINFO'})
        return (node, tocnode)
        
        
    def renderSimpleSection(self, ID):
        simplesection = self.model.getSimpleSection(ID)
        node = self._createElement('div', {'class': 'simplesection'})
        subnode = self._createElement('h2')
        subnode.appendChild(self._createTextElement('a', 'SS-%(ID)03d: %(title)s' % simplesection, {'name': 'SS-%(ID)03d' % simplesection}))
        node.appendChild(subnode)
        node.appendChild(self._render(simplesection['content']))
        tocnode = self._createTextElement('a', 'SS-%(ID)03d: %(title)s' % simplesection, {'href': '#SS-%(ID)03d' % simplesection})
        return (node, tocnode)
        
        
    def renderFeature(self, ID):
        feature = self.model.getFeature(ID)
        basedata = feature.getPrintableDataDict()
        node = self._createElement('div', {'class': 'feature'})
        subnode = self._createElement('h2')
        subnode.appendChild(self.renderFeatureAnchor(feature, False))
        node.appendChild(subnode)
        
        table = self._createElement('table')
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
            
        tocnode = self.renderFeatureAnchor(feature, True)
        return (node, tocnode)
        

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
        
        table = self._createElement('table')
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
        return (node, tocnode)
        
        
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
        
        table = self._createElement('table')
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
        if len(relatedrequirements) == 0:
            subnode = self._createTextElement('span', _('None'), {'class': 'alert'})
        else:
            subnode = self._createElement('ul')
            for requirement in relatedrequirements:
                self.appendListItem(subnode, self.renderRequirementAnchor(requirement, True))
        table.appendChild(self._createTableRow(_('Related Requirements'), subnode))
            
        tocnode = self.renderUsecaseAnchor(usecase, True)
        return (node, tocnode)
        
        
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
        
        table = self._createElement('table')
        node.appendChild(table)
        table.appendChild(self._createTableRow(_('Version'),      basedata['version']))
        table.appendChild(self._createTableRow(_('Purpose'),      self._render(basedata['purpose'])))
        table.appendChild(self._createTableRow(_('Prerequisite'), self._render(basedata['prerequisite'])))
        table.appendChild(self._createTableRow(_('Testdata'),     self._render(basedata['testdata'])))
        table.appendChild(self._createTableRow(_('Steps'),        self._render(basedata['steps'])))
        table.appendChild(self._createTableRow(_('Notes'),        self._render(basedata['notes'])))
        
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
        return (node, tocnode)
        
        
    def renderTestcaseAnchor(self, testcase, href):
        if href:
            attribute = {'href': '#TC-%(ID)03d' % testcase}
        else:
            attribute = {'name': 'TC-%(ID)03d' % testcase}
        return self._createTextElement('a', 'TC-%(ID)03d: %(title)s' % testcase, attribute)


    def renderTestsuite(self, ID):
        testsuite = self.model.getTestsuite(ID)
        basedata = testsuite.getPrintableDataDict()
        node = self._createElement('div', {'class': 'testsuite'})
        subnode = self._createElement('h2')
        subnode.appendChild(self.renderTestsuiteAnchor(testsuite, False))
        node.appendChild(subnode)
        
        table = self._createElement('table')
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
        
        
    def _createTableRow(self, left, right):
        tr = self._createElement('tr')
        if type(left) in [type(''), type(u'')]:
            th = self._createTextElement('th', left) 
        else:
            th = self._createElement('th')
            th.appendChild(left)
        if type(right) in [type(''), type(u'')]:
            td = self._createTextElement('td', right) 
        else:
            td = self._createElement('td')
            td.appendChild(right)
        tr.appendChild(th)
        tr.appendChild(td)
        return tr
        
        
    def getCSSFile(self):
        p = os.path.join(os.path.dirname(__file__), self.cssfile)
        if os.path.exists(p):
            fp = codecs.open(p, encoding='utf-8', errors = 'ignore')
            css = ''
            for line in fp:
                if line.startswith('/* start */'): break
            for line in fp:
                css += line
            fp.close()
        else:
            css = ''
        css += "\n@import '%s';\n" % self.cssfile
        return css
        
    
    def _render(self, text):
        text = _afhtmlwindow.render(text)
        text = '<?xml version="1.0" encoding="UTF-8" ?>' + text
        dom = parseString(text.encode('UTF-8'))
        return dom.documentElement
        


if __name__=="__main__":
    import os, sys, getopt

    def version():
        print("Version unknown")

    def usage():
        print("Usage:\n%s [-h|--help] [-V|--version] [-o <ofile>|--output=<ofile>] <ifile>\n"
        "  -h, --help                      show help and exit\n"
        "  -V, --version                   show version and exit\n"
        "  -o <ofile>, --output=<ofile>    output to file <ofile>\n"
        "  -l <lang>, --language=<lang>    select output language (de|en)"
        "  <ifile>                         database file"
        % sys.argv[0])


    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:l:V", ["help", "output=", "language", "version"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    language = 'en'
    for o, a in opts:
        if o in ("-V", "--version"):
            version()
            sys.exit()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-l", "--language"):
            language = a
        else:
            assert False, "unhandled option"

    if len(args) != 1:
        usage()
        sys.exit(1)

    try:
        t = gettext.translation(DOMAIN, LOCALEDIR, languages=[language])
        t.install(unicode=True)
    except IOError:
        print('Unsupported language: %s' % language)
        sys.exit(1)

    model = afmodel.afModel(controller = None)
    try:
        cwd = os.getcwd()
        model.requestOpenProduct(args[0])
        os.chdir(cwd)
    except:
        print("Error opening database file %s" % args[0])
        print(sys.exc_info())
        sys.exit(1)

    if output is None:
        output =  os.path.splitext(args[0])[0] + ".html"

    export = afExportHTML(model)
    export.run()
    export.write(output)
