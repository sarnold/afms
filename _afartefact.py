# -*- coding: latin-1  -*-

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

import wx
import afresource


class cArtefact():
    """Base class for all artefacts"""

    def __init__(self):
        self._changelist = []
        self._changelog = None
        self._supportschangelog = False
        self._tags = ''


    def __getitem__(self, key):
        if key=='tags':
            return self._tags
        return self._basedata[key]


    def __setitem__(self, key, value):
        self._basedata[key] = value


    def keys(self):
        return self._keys


    def labels(self):
        return self._labels


    def setChangelist(self, changelist):
        self._changelist = changelist


    def clearRelations(self):
        pass


    def getChangelist(self):
        return self._changelist


    def setChangelog(self, changelog):
        self._changelog = changelog


    def getChangelog(self):
        return self._changelog


    def identity(self, s):
        return s


    def getPrintableDataDict(self, formatter=None):
        """Return base data in printable format, i.e. localized and enuumerations
        replaced with human readable text"""
        return self._basedata


    def _writeHistory(self, s):
        s += '<history>\n'
        for cle in self.getChangelist():
            s += cle.xmlrepr('item')
        s += '</history>\n'
        return s


    def xmlrepr(self, tagname):
        """Return base data as XML string"""
        s = '<%s>\n' % tagname
        for key in self._keys:
            s += '<%s><![CDATA[%s]]></%s>\n' % (key, self._basedata[key], key)
        s = self._writeHistory(s)
        s += '</%s>\n' % tagname
        return s


    def supportsChangelog(self):
        """Return True when a changelog is part of an artefact"""
        return self._supportschangelog


    def getTags(self):
        return self._tags


    def setTags(self, tags):
        self._tags = tags

#----------------------------------------------------------------------

class cChangelogEntry():
    def __init__(self, user, description, changetype=None, date=None):
        self._basedata = {
        'user'        : user,
        'ID'          : date,
        'description' : description,
        'changetype'  : changetype,
        'date'        : date }

    def __getitem__(self, key):
        if key=='tags':
            return ''
        return self._basedata[key]


    def __setitem__(self, key, value):
        self._basedata[key] = value


    def identity(self, s):
        return s


    def labels(self):
        return [_('Date'), _('User'), _('Description')]


    def keys(self):
        return ['date', 'user', 'description']


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        if len(basedata['description']) <= 0:
            basedata['description'] = _(afresource.CHANGETYPE_NAME[basedata['changetype']])
        else:
            basedata['description'] = formatter(basedata['description'])
        basedata['user'] = formatter(basedata['user'])
        return basedata


    def xmlrepr(self, tagname):
        """Return base data as XML string"""
        data = self.getPrintableDataDict(lambda s: s)
        s = '<%s>\n' % tagname
        for key in self.keys():
            s += '<%s><![CDATA[%s]]></%s>\n' % (key, data[key], key)
        s += '</%s>\n' % tagname
        return s

#----------------------------------------------------------------------

class cFeature(cArtefact):
    def __init__(self, ID=-1, title='', priority=0, status=0, version='',
                 risk=0, description=''):
        cArtefact.__init__(self)
        self._labels = [_('ID'), _('Title'), _('Priority'), _('Status'), _('Version'), _('Risk'), _('Description')]
        self._keys = ['ID', 'title','priority', 'status', 'version', 'risk', 'description']
        self._supportschangelog = True
        self._basedata = {
            'ID'            : ID,
            'title'         : title,
            'priority'      : priority,
            'status'        : status,
            'version'       : version,
            'risk'          : risk,
            'description'   : description }
        self._relatedRequirements = []
        self._unrelatedRequirements = []
        self._relatedUsecases = []
        self._unrelatedUsecases = []


    def clearRelations(self):
        self._relatedRequirements = []
        self._unrelatedRequirements = []
        self._relatedUsecases = []
        self._unrelatedUsecases = []


    def setRelatedRequirements(self, requirements):
        self._relatedRequirements = requirements


    def getRelatedRequirements(self):
        return self._relatedRequirements


    def setUnrelatedRequirements(self, requirements):
        self._unrelatedRequirements = requirements


    def getUnrelatedRequirements(self):
        return self._unrelatedRequirements


    def setRelatedUsecases(self, usecases):
        self._relatedUsecases = usecases


    def getRelatedUsecases(self):
        return self._relatedUsecases


    def setUnrelatedUsecases(self, usecases):
        self._unrelatedUsecases = usecases


    def getUnrelatedUsecases(self):
        return self._unrelatedUsecases


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['description'] = formatter(basedata['description'])
        basedata['priority'] = _(afresource.PRIORITY_NAME[basedata['priority']])
        basedata['status'] = _(afresource.STATUS_NAME[basedata['status']])
        basedata['risk'] = _(afresource.RISK_NAME[basedata['risk']])
        return basedata


    def getClipboardText(self):
        s = u""
        basedata = self.getPrintableDataDict()
        for label, key in zip(self._labels, self._keys):
            s += u"%s: %s\n" % (label, basedata[key])
        return s.encode('iso-8859-1')


    def xmlrepr(self):
        return cArtefact.xmlrepr(self, 'feature')

#----------------------------------------------------------------------

class cRequirement(cArtefact):
    def __init__(self, ID=-1, title='', priority=0, status=0, version='',
                 complexity=0, assigned='', effort=0, category=0, origin='',
                 rationale='', description=''):
        cArtefact.__init__(self)
        self._supportschangelog = True
        self._labels = [_('ID'), _('Title'), _('Priority'), _('Status'), _('Version'),
                        _('Complexity'), _('Assigned'), _('Effort'), _('Category'),
                        _('Origin'), _('Rationale'), _('Description')]
        self._keys = ['ID', 'title', 'priority', 'status', 'version',
                      'complexity', 'assigned', 'effort', 'category',
                      'origin', 'rationale', 'description']
        self._basedata = {
            'ID'          : ID,
            'title'       : title,
            'priority'    : priority,
            'status'      : status,
            'version'     : version,
            'complexity'  : complexity,
            'assigned'    : assigned,
            'effort'      : effort,
            'category'    : category,
            'origin'      : origin,
            'rationale'   : rationale,
            'description' : description }
        self._relatedTestcases = []
        self._unrelatedTestcases = []
        self._relatedUsecases = []
        self._unrelatedUsecases = []
        self._relatedFeatures = []
        self._relatedRequirements = []
        self._unrelatedRequirements = []


    def clearRelations(self):
        self._relatedTestcases = []
        self._unrelatedTestcases = []
        self._relatedUsecases = []
        self._unrelatedUsecases = []
        self._relatedFeatures = []
        self._unrelatedRequirements = []
        self._relatedRequirements = []


    def setRelatedTestcases(self, testcases):
        self._relatedTestcases = testcases


    def getRelatedTestcases(self):
        return self._relatedTestcases


    def setUnrelatedTestcases(self, testcases):
        self._unrelatedTestcases = testcases


    def getUnrelatedTestcases(self):
        return self._unrelatedTestcases


    def setRelatedUsecases(self, usecases):
        self._relatedUsecases = usecases


    def getRelatedUsecases(self):
        return self._relatedUsecases


    def setUnrelatedUsecases(self, usecases):
        self._unrelatedUsecases = usecases


    def getUnrelatedUsecases(self):
        return self._unrelatedUsecases


    def setRelatedFeatures(self, features):
        self._relatedFeatures = features


    def getRelatedFeatures(self):
        return self._relatedFeatures


    def getUnrelatedRequirements(self):
        return self._unrelatedRequirements


    def getRelatedRequirements(self):
        return self._relatedRequirements


    def setUnrelatedRequirements(self, requirements):
        self._unrelatedRequirements = requirements


    def setRelatedRequirements(self, requirements):
        self._relatedRequirements = requirements


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['origin'] = formatter(basedata['origin'])
        basedata['rationale'] = formatter(basedata['rationale'])
        basedata['description'] = formatter(basedata['description'])
        basedata['priority'] = _(afresource.PRIORITY_NAME[basedata['priority']])
        basedata['status'] = _(afresource.STATUS_NAME[basedata['status']])
        basedata['complexity'] = _(afresource.COMPLEXITY_NAME[basedata['complexity']])
        basedata['effort'] = _(afresource.EFFORT_NAME[basedata['effort']])
        basedata['category'] = _(afresource.CATEGORY_NAME[basedata['category']])
        return basedata


    def getClipboardText(self):
        s = u""
        basedata = self.getPrintableDataDict()
        for label, key in zip(self._labels, self._keys):
            s += u"%s: %s\n" % (label, basedata[key])
        return s.encode('iso-8859-1')


    def xmlrepr(self):
        return cArtefact.xmlrepr(self, 'requirement')


    def supportsChangelogEntry(self):
        """Return True when a changelog entry is part of an artefact"""
        return True

#----------------------------------------------------------------------

class cUsecase(cArtefact):
    def __init__(self, ID=-1, title='', priority=0, usefrequency=0, actors='',
                 stakeholders='', prerequisites='', mainscenario='',
                 altscenario='', notes=''):
        cArtefact.__init__(self)
        self._supportschangelog = True
        self._labels = [_('ID'), _('Summary'), _('Priority'), _('Use frequency'),
                        _('Actors'), _('Stakeholders'), _('Prerequisites'),
                        _('Main scenario'), _('Alt scenario'), _('Notes')]
        self._keys = ['ID', 'title', 'priority', 'usefrequency', 'actors',
                       'stakeholders', 'prerequisites', 'mainscenario', 'altscenario',
                       'notes']
        self._basedata = {
            'ID'            : ID,
            'title'         : title,
            'priority'      : priority,
            'usefrequency'  : usefrequency,
            'actors'        : actors,
            'stakeholders'  : stakeholders,
            'prerequisites' : prerequisites,
            'mainscenario'  : mainscenario,
            'altscenario'   : altscenario,
            'notes'         : notes }
        self.relatedRequirements = []
        self.relatedFeatures = []


    def clearRelations(self):
        self.relatedRequirements = []
        self.relatedFeatures = []


    def setRelatedRequirements(self, requirements):
        self.relatedRequirements = requirements


    def getRelatedRequirements(self):
        return self.relatedRequirements


    def setRelatedFeatures(self, features):
        self.relatedFeatures = features


    def getRelatedFeatures(self):
        return self.relatedFeatures


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['prerequisites'] = formatter(basedata['prerequisites'])
        basedata['mainscenario'] = formatter(basedata['mainscenario'])
        basedata['altscenario'] = formatter(basedata['altscenario'])
        basedata['notes'] = formatter(basedata['notes'])
        basedata['priority'] = _(afresource.PRIORITY_NAME[basedata['priority']])
        basedata['usefrequency'] = _(afresource.USEFREQUENCY_NAME[basedata['usefrequency']])
        return basedata


    def getClipboardText(self):
        s = u""
        basedata = self.getPrintableDataDict()
        for label, key in zip(self._labels, self._keys):
            s += u"%s: %s\n" % (label, basedata[key])
        return s.encode('iso-8859-1')


    def xmlrepr(self):
        return cArtefact.xmlrepr(self, 'usecase')


    def supportsChangelogEntry(self):
        """Return True when a changelog entry is part of an artefact"""
        return True

#----------------------------------------------------------------------

class cTestcase(cArtefact):
    def __init__(self, ID=-1, title='', purpose='', prerequisite='', testdata='', steps='', notes='', version='', scripturl=''):
        cArtefact.__init__(self)
        self._supportschangelog = True
        self._labels = [_('ID'), _('Title'), _('Purpose'),
                  _('Prerequisite'), _('Testdata'), _('Steps'),
                  _('Notes && Questions'), _('Version'), 'Script URL']
        self._keys = ['ID', 'title', 'purpose', 'prerequisite', 'testdata', 'steps',
                'notes', 'version', 'scripturl']
        self._basedata = {
            'ID'           :  ID,
            'title'        :  title,
            'purpose'      :  purpose,
            'prerequisite' :  prerequisite,
            'testdata'     :  testdata,
            'steps'        :  steps,
            'notes'        :  notes,
            'version'      :  version,
            'scripturl'    :  scripturl }
        self.relatedRequirements = []
        self.relatedTestsuites = []


    def clearRelations(self):
        self.relatedRequirements = []
        self.relatedTestsuites = []


    def setRelatedRequirements(self, requirements):
        self.relatedRequirements = requirements


    def getRelatedRequirements(self):
        return self.relatedRequirements


    def setRelatedTestsuites(self, testsuites):
        self.relatedTestsuites = testsuites


    def getRelatedTestsuites(self):
        return self.relatedTestsuites


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['purpose'] = formatter(basedata['purpose'])
        basedata['prerequisite'] = formatter(basedata['prerequisite'])
        basedata['testdata'] = formatter(basedata['testdata'])
        basedata['steps'] = formatter(basedata['steps'])
        basedata['notes'] = formatter(basedata['notes'])
        return basedata


    def getClipboardText(self):
        s = u""
        basedata = self.getPrintableDataDict()
        for label, key in zip(self._labels, self._keys):
            s += u"%s: %s\n" % (label, basedata[key])
        return s.encode('iso-8859-1')


    def xmlrepr(self):
        return cArtefact.xmlrepr(self, 'testcase')


    def supportsChangelogEntry(self):
        """Return True when a changelog entry is part of an artefact"""
        return True

#----------------------------------------------------------------------

class cTestsuite(cArtefact):
    def __init__(self, ID=-1, title='', description='', execorder='', nbroftestcases='N/A'):
        cArtefact.__init__(self)
        self._supportschangelog = False
        self._labels = [_("ID"), _("Title"), _("Description"), _("Execution order ID's"), '# '+_('Testcases')]
        self._keys = ['ID', 'title', 'description', 'execorder', 'nbroftestcase']
        self._basedata = {
            'ID'           : ID,
            'title'        : title,
            'description'  : description,
            'execorder'    : execorder,
            'nbroftestcase': nbroftestcases }
        self._relatedTestcases = []
        self._unrelatedTestcases = []


    def clearRelations(self):
        self._relatedTestcases = []
        self._unrelatedTestcases = []


    def setRelatedTestcases(self, testcases):
        self._relatedTestcases = testcases


    def getRelatedTestcases(self):
        return self._relatedTestcases


    def setUnrelatedTestcases(self, testcases):
        self._unrelatedTestcases = testcases


    def getUnrelatedTestcases(self):
        return self._unrelatedTestcases


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['description'] = formatter(basedata['description'])
        return basedata


    def getClipboardText(self):
        s = u""
        basedata = self._basedata.copy()

        for label, key in zip(self._labels, self._keys):
            s += u"%s: %s\n" % (label, basedata[key])
        return s.encode('iso-8859-1')


    def xmlrepr(self):
        s = '<testsuite>\n'
        for key in self._keys:
            s += '<%s><![CDATA[%s]]></%s>\n' % (key, self._basedata[key], key)
        s += '<testcases>\n'
        for tc in self._relatedTestcases:
            s += '<id>%d</id>\n' % tc['ID']
        s += '</testcases>\n'
        s += '</testsuite>\n'
        return s

#----------------------------------------------------------------------

class cProduct(cArtefact):
    def __init__(self, title='', description='', dbversion=None):
        cArtefact.__init__(self)
        self._basedata = {
            'title'       : title,
            'description' : description,
            'dbversion'   : dbversion }


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['description'] = formatter(basedata['description'])
        return basedata

#----------------------------------------------------------------------

class cSimpleSection(cArtefact):
    def __init__(self, ID=-1, title='', content='', level=-1):
        cArtefact.__init__(self)
        self._supportschangelog = True
        self._labels = [_("ID"), _("Title"), _("Content"), _("Level")]
        self._keys = ['ID', 'title', 'content', 'level']
        self._basedata = {
            'ID'       : ID,
            'title'    : title,
            'content'  : content,
            'level'    : level    }


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['content'] = formatter(basedata['content'])
        return basedata


    def getClipboardText(self):
        s = u""
        for label, key in zip(self._labels, self._keys):
            s += u"%s: %s\n" % (label, self._basedata[key])
        return s.encode('iso-8859-1')

#----------------------------------------------------------------------

class cGlossaryEntry(cArtefact):
    def __init__(self, ID=-1, title='', description=''):
        cArtefact.__init__(self)
        self._supportschangelog = False
        self._labels = [_("ID"), _("Term"), _("Description")]
        self._keys = ['ID', 'title', 'description']
        self._basedata = {
            'ID'           : ID,
            'title'        : title,
            'description'  : description,}


    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['description'] = formatter(basedata['description'])
        return basedata


    def getClipboardText(self):
        s = u""
        for label, key in zip(self._labels, self._keys):
            s += u"%s: %s\n" % (label, self._basedata[key])
        return s.encode('iso-8859-1')

#----------------------------------------------------------------------

class cTag(object):
    color = {'Red' : wx.RED, 'Green' : wx.GREEN, 'Blue' : wx.BLUE, 'Black': wx.BLACK,
             'Yellow' : wx.Colour(255, 255,   0), 'Light Blue': wx.Colour(173, 216, 230),
             'Magenta' : wx.Colour(255,   0, 255), 'Pink' : wx.Colour(255, 181, 197),
             'Orange' : wx.Colour(255, 165,   0),  'Purple' : wx.Colour(160,  32, 240)}
    colornames = ['Black', 'Blue', 'Red', 'Green', 'Yellow', 'Light Blue', 'Magenta',
                  'Pink', 'Orange', 'Purple']

    @staticmethod
    def index2tagchar(index):
        return chr(index+ord('A'))

    @staticmethod
    def tagchar2index(tagchar):
        return ord(tagchar)-ord('A')

    def __init__(self, ID, shortdesc, longdesc, color='Black'):
        self._basedata = {'ID' : ID, 'shortdesc' : shortdesc, 'longdesc' : longdesc, 'color': color}

    def __getitem__(self, key):
        return self._basedata[key]


    def __setitem__(self, key, value):
        self._basedata[key] = value