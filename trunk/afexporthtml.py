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
import afmodel
import afconfig
import afresource
from afresource import _, ENCODING
import _afdocutils


HTMLHEADER = \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=%s">
<title>AFMS Report</title>
<link href="afmsreport.css" rel="stylesheet" type="text/css">
</head>
<body>
"""

HTMLFOOTER = \
"""
</body>
</html>
"""

htmlentities = \
    {u"ä": u"&auml;", u"ö": u"&ouml;", u"ü": u"&uuml;",
     u"Ä": u"&Auml;", u"Ö": u"&Ouml;", u"Ü": u"&Uuml;",
     u"ß": u"&szlig;", u"\"": u"&quot;"}

htmlentities = (\
    (u"ö",      u"Ö",      u"ä",      u"Ä",      u"ü",      u"Ü",      u"ß",       u"\""),
    (u"&ouml;", u"&Ouml;", u"&auml;", u"&Auml;", u"&uuml;", u"&Uuml;", u"&szlig;", u"&quot;"))

specialchars = (\
    (u"&",     u">",    u"<",    u"ö",      u"Ö",      u"ä",      u"Ä",      u"ü",      u"Ü",      u"ß",       u"\""),
    (u"&amp;", u"&gt;", u"&lt;", u"&ouml;", u"&Ouml;", u"&auml;", u"&Auml;", u"&uuml;", u"&Uuml;", u"&szlig;", u"&quot;"))

def __(s, entities=htmlentities):
    for k,v in zip(entities[0], entities[1]):
        s = s.replace(k, v)
    return s


def formatField(fstr):
    """
    Format a field from database
    Formatting depends on whether the field data starts with <html> or not.
    """
    fstr = fstr.strip(' \t\n')
    if fstr.startswith(("<html>", "<HTML>")):
        fstr = fstr[6:]
        if fstr.endswith(("</html>", "</HTML>")):
            fstr = fstr[0:-7]

    elif fstr.startswith((".. rest", ".. REST")):
        fstr = _afdocutils.html_body(fstr, doctitle=0, initial_header_level=3)
    else:
        fstr = __(fstr, specialchars)
        lines = fstr.split(u"\n")
        fstr = "<br />".join(lines)
    return fstr


class afExportHTML():
    def __init__(self, outfilename, model):
        self.model = model
        self.lonelyfeatures = []
        self.lonelytestcases = []
        self.untestedrequirements = []
        self.emptytestsuites = []
        self.testcasesnotintestsuites = []
        self.attached_usecase_ids = []

        self.of = codecs.open(outfilename, encoding=ENCODING, mode="w", errors='strict')
        self.writeHTMLHeader()
        self.writeTOC()
        self.writeTag('h1', '<a name="productinfo">%s</a>' % __(_('Product information')))
        self.writeProductInfo()
        self.writeTag('h1', '<a name="features">%s</a>' % __(_('Features')))
        self.writeFeatures()

        self.writeTag('h1', '<a name="requirements">%s</a>' % __(_('Requirements')))
        self.writeRequirements()
        
        self.writeTag('h1', '<a name="testcases">%s</a>' % __(_('Testcases')))
        self.writeTestcases()
        
        self.writeTag('h1', '<a name="testsuites">%s</a>' % __(_('Testsuites')))
        self.writeTestsuites()
        
        self.writeTag('h1', '<a name="problems">%s</a>' % __(_('Detected problems')))
        self.writeProblems()
        
        self.writeHTMLFooter()
        self.of.close()
        

    def formatField(self, fstr):
        return formatField(fstr)
        
        
    def writeHTMLHeader(self):
        self.of.write(HTMLHEADER % ENCODING)
        

    def writeHTMLFooter(self):
        self.of.write('<hr />')
        footer = _('Created from %s at %s') % (self.model.getFilename(), strftime(afresource.TIME_FORMAT, localtime()))
        self.of.write('<p class="footer">%s</p>' % footer)
        self.of.write(HTMLFOOTER)
        
        
    def writeTag(self, tag, content):
        self.of.write("<%s>%s</%s>\n" % (tag, content, tag))


    def writeList(self, aflist, label):
        self.of.write("<ul>\n")
        for af in aflist:
            basedata = af.getPrintableDataDict()
            basedata['_LABEL'] = label
            
            self.of.write('<li><a href="#%(_LABEL)s-%(ID)03d">%(_LABEL)s-%(ID)03d: %(title)s</a></li>\n' % basedata)
        self.of.write("</ul>\n")


    def writeTOC(self):
        self.writeTag("h1", __(_('Table of Contents')))
        self.of.write("<ol>")
        self.of.write('<li><a href="#productinfo">%s</a></li>' % _('Product information'))

        self.of.write('<li><a href="#features">%s</a></li>' % _('Features'))
        self.writeList(self.model.getFeatureList(), 'F')

        self.of.write('<li><a href="#requirements">%s</a></li>' % _('Requirements'))
        self.writeList(self.model.getRequirementList(), 'REQ')

        self.of.write('<li><a href="#testcases">%s</a></li>' % _('Testcases'))
        self.writeList(self.model.getTestcaseList(), 'TC')

        self.of.write('<li><a href="#testsuites">%s</a></li>' % _('Testsuites'))
        self.writeList(self.model.getTestsuiteList(), 'TS')
        
        self.of.write('<li><a href="#problems">%s</a></li>' % _('Detected problems'))
        self.of.write('<ul>')
        self.of.write('<li><a href="#lonelyfeatures">%s</a></li>' % _('Features without requirements'))
        self.of.write('<li><a href="#untestedrequirements">%s</a></li>' % _('Requirements without testcases'))
        self.of.write('<li><a href="#lonelytestcases">%s</a></li>' % _('Testcases not belonging to requirements'))
        self.of.write('<li><a href="#unexecutedtestcases">%s</a></li>' % _('Testcases not belonging to testsuites'))
        self.of.write('<li><a href="#emptytestsuites">%s</a></li>' % _('Empty testsuites'))
        self.of.write('<li><a href="#lonelyusecases">%s</a></li>' % _('Usecases not belonging to requirements'))
        self.of.write('</ul>')
        self.of.write("</ol>")
        
    
    def writeProblems(self):
        def writeListOrNone(aflist, label):
            if len(aflist) > 0:
                self.writeList(aflist, label)
            else:
                self.writeTag('p', _('None'))

        self.writeTag('h2', '<a name="lonelyfeatures">%s</a>' % _('Features without requirements'))
        writeListOrNone(self.lonelyfeatures, 'F')

        self.writeTag('h2', '<a name="untestedrequirements">%s</a>' % _('Requirements without testcases'))
        writeListOrNone(self.untestedrequirements, 'REQ')

        self.writeTag('h2', '<a name="lonelytestcases">%s</a>' % _('Testcases not belonging to requirements'))
        writeListOrNone(self.lonelytestcases, 'TC')
        
        self.writeTag('h2', '<a name="unexecutedtestcases">%s</a>' % _('Testcases not belonging to testsuites'))
        writeListOrNone(self.testcasesnotintestsuites, 'TC')

        self.writeTag('h2', '<a name="emptytestsuites">%s</a>' % _('Empty testsuites'))
        writeListOrNone(self.emptytestsuites, 'TS')

        self.writeTag('h2', '<a name="lonelyusecases">%s</a>' % _('Usecases not belonging to requirements'))
        all_uc_ids = set(self.model.getUsecaseIDs())
        lonely_uc_ids = all_uc_ids.difference(set(self.attached_usecase_ids))
        uclist = []
        for uc_id in lonely_uc_ids:
            uclist.append(self.model.getUsecase(uc_id))
        writeListOrNone(uclist, 'UC')
        
        for uc_id in lonely_uc_ids:
            self.writeUsecase(uc_id)

        
    def writeProductInfo(self):
        pi = self.model.getProductInformation()
        self.of.write('<div class="producttitle">\n%s\n</div>' % self.formatField(pi['title']))
        self.of.write('<div class="productdescription">\n%s\n</div>' % self.formatField(pi['description']))
        
        
    def writeFeatures(self):
            idlist = self.model.getFeatureIDs()
            for ID in idlist:
                feature = self.model.getFeature(ID)
                basedata = feature.getPrintableDataDict(self.formatField)
                
                self.writeTag('h2', '<a name="F-%(ID)03d">F-%(ID)03d: %(title)s</a>' % basedata)
                self.of.write('<table>\n')
                for label, key in zip(feature.labels()[2:], feature.keys()[2:]):
                    self.of.write('<tr><th>%s</th><td>%s</td></tr>\n' % (label, basedata[key]))
                    
                self.of.write('<tr><th>%s</th><td>' % _('Related requirements'))
                related_requirements = feature.getRelatedRequirements()
                if len(related_requirements) > 0:
                    self.of.write('<ul>\n')
                    for req in related_requirements:
                        basedata = req.getPrintableDataDict(self.formatField)
                        self.of.write('<li><a href="#REQ-%(ID)03d">REQ-%(ID)03d: %(title)s</a></li>\n' % basedata)
                    self.of.write('</ul>\n')
                else:
                    self.lonelyfeatures.append(feature)
                    self.of.write('<p class="alert">%s</p>' % _('None'))
                self.of.write('</td></tr>\n')
                self.of.write('</table>\n')
                

    def writeRequirements(self):
            idlist = self.model.getRequirementIDs()
            for ID in idlist:
                requirement = self.model.getRequirement(ID)
                basedata = requirement.getPrintableDataDict(self.formatField)
                
                self.writeTag('h2', '<a name="REQ-%(ID)03d">REQ-%(ID)03d: %(title)s</a>' % basedata)
                self.of.write('<div class="requirement">\n')
                
                self.of.write('<table>\n')
                for label, key in zip(requirement.labels()[2:], requirement.keys()[2:]):
                    self.of.write('<tr><th>%s</th><td>%s</td></tr>\n' % (label, basedata[key]))
                    
                self.of.write('<tr><th>%s</th><td>' % _('Attached testcases'))
                related_testcases = requirement.getRelatedTestcases()
                if len(related_testcases) > 0:
                    self.of.write('<ul>')
                    for tc in related_testcases:
                        basedata = tc.getPrintableDataDict(self.formatField)
                        self.of.write('<li><a href="#TC-%(ID)03d">TC-%(ID)03d: %(title)s</a></li>\n' % basedata)
                    self.of.write('</ul>')
                else:
                    self.untestedrequirements.append(requirement)
                    self.of.write('<p class="alert">%s</p>' % _('None'))
                self.of.write('</td></tr>\n')
                self.of.write('</table>\n')
                
                self.of.write('<div class="usecases">\n')
                related_usecases = requirement.getRelatedUsecases()
                if len(related_usecases) > 0:
                    for uc in related_usecases:
                        self.writeUsecase(uc['ID'])
                        self.attached_usecase_ids.append(uc['ID'])
                else:
                    self.of.write('<p>%s</p>' % _('No use cases'))
                self.of.write('</div>\n')
                self.of.write('</div>\n')


    def writeUsecase(self, uc_id):
        usecase = self.model.getUsecase(uc_id)
        basedata = usecase.getPrintableDataDict(self.formatField)

        self.writeTag('h3', '<a name="UC-%(ID)03d">UC-%(ID)03d: %(title)s</a>' % basedata)
        
        self.of.write('<table>\n')
        for label, key in zip(usecase.labels()[2:], usecase.keys()[2:]):
                self.of.write('<tr><th>%s</th><td>%s</td></tr>\n' % (label, basedata[key]))
        self.of.write('</table>\n')

        
    def writeTestcases(self):
        idlist = self.model.getTestcaseIDs()
        for ID in idlist:
            testcase = self.model.getTestcase(ID)
            basedata = testcase.getPrintableDataDict(self.formatField)

            self.writeTag('h2', '<a name="TC-%(ID)03d">TC-%(ID)03d: %(title)s</a>' % basedata)
            self.of.write('<table>\n')
            for label, key in zip(testcase.labels()[2:], testcase.keys()[2:]):
                self.of.write('<tr><th>%s</th><td>%s</td></tr>\n' % (label, basedata[key]))
                
            self.of.write('<tr><th>%s</th><td>' % _('Related requirements'))
            related_requirements = testcase.getRelatedRequirements()
            if len(related_requirements) > 0:
                self.of.write('<ul>')
                for req in related_requirements:
                    basedata = req.getPrintableDataDict(self.formatField)
                    self.of.write('<li><a href="#REQ-%(ID)03d">REQ-%(ID)03d: %(title)s</a></li>\n' % basedata)
                self.of.write('</ul>')
            else:
                self.lonelytestcases.append(testcase)
                self.of.write('<p class="alert">%s</p>' % _('None'))
            self.of.write('</td></tr>\n')

            self.of.write('<tr><th>%s</th><td>' % _('Related testsuites'))
            related_testsuites = testcase.getRelatedTestsuites()
            if len(related_testsuites) > 0:
                self.of.write('<ul>')
                for ts in related_testsuites:
                    basedata = ts.getPrintableDataDict(self.formatField)
                    self.of.write('<li><a href="#TS-%(ID)03d">TS-%(ID)03d: %(title)s</a></li>\n' % basedata)
                self.of.write('</ul>')
            else:
                self.testcasesnotintestsuites.append(testcase)
                self.of.write('<p class="alert">%s</p>' % _('None'))
                
            self.of.write('</table>\n')


    def writeTestsuites(self):
        idlist = self.model.getTestsuiteIDs()
        for ID in idlist:
            testsuite = self.model.getTestsuite(ID)
            basedata = testsuite.getPrintableDataDict(self.formatField)
            self.writeTag('h2', '<a name="TS-%(ID)03d">TS-%(ID)03d: %(title)s</a>' % basedata)
            self.of.write('<table>\n')
            for label, key in zip(testsuite.labels()[2:], testsuite.keys()[2:]):
                self.of.write('<tr><th>%s</th><td>%s</td></tr>\n' % (label, basedata[key]))

            self.of.write('<tr><th>%s</th><td>' % _('Included testcases'))
            includedtestcaselist = testsuite.getRelatedTestcases()
            if len(includedtestcaselist) > 0:
                self.of.write('<ul>')
                for tc in includedtestcaselist:
                    basedata = tc.getPrintableDataDict(self.formatField)
                    self.of.write('<li><a href="#TC-%(ID)03d">TC-%(ID)03d: %(title)s</a></li>\n' % basedata)
                self.of.write('</ul>')
            else:
                self.emptytestsuites.append(testsuite)
                self.of.write('<p class="alert">%s</p>' % _('None'))

            self.of.write('</table>\n')


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
        model.requestOpenProduct(args[0])
    except:
        print("Error opening database file %s" % args[0])
        print(sys.exc_info())
        sys.exit(1)
    
    if output is None:
        output =  os.path.splitext(args[0])[0] + ".html"
        
    export = afExportHTML(output, model)
