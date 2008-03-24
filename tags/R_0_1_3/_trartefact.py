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

import _afartefact 
import afresource
from afresource import _

class cTestcase(_afartefact.cTestcase):
    def __init__(self, ID=-1, title='', purpose='', prerequisite='', testdata='',
                 steps='', notes='', version='1.0',
                 testresult=afresource.PENDING, testremark='', action='', timestamp=''):
        _afartefact.cArtefact.__init__(self)
        self._labels = [_('ID'), _('Title'), _('Purpose'),
                  _('Prerequisite'), _('Testdata'), _('Steps'),
                  _('Notes && Questions'), _('Version'), _('Result'), _('Remark'),
                  _('Action'), _('Time stamp')]
        self._keys = ['ID', 'title', 'purpose', 'prerequisite', 'testdata', 'steps',
                'notes', 'version', 'testresult', 'testremark', 'action', 'timestamp']
        self._basedata = {
            'ID'           : ID,
            'title'        : title,
            'purpose'      : purpose,
            'prerequisite' : prerequisite,
            'testdata'     : testdata,
            'steps'        : steps,
            'notes'        : notes,
            'version'      : version,
            'testresult'   : testresult,
            'testremark'   : testremark,
            'action'       : action,
            'timestamp'    : timestamp        }
            
    def importBaseTestcase(self, basetestcase):
        self._basedata['ID'] = basetestcase['ID']
        self._basedata['title'] = basetestcase['title']
        self._basedata['purpose'] = basetestcase['purpose']
        self._basedata['prerequisite'] = basetestcase['prerequisite']
        self._basedata['testdata'] = basetestcase['testdata']
        self._basedata['steps'] = basetestcase['steps']
        self._basedata['notes'] = basetestcase['notes']
        self._basedata['version'] = basetestcase['version']

    def getPrintableDataDict(self, formatter=None):
        if formatter == None: formatter = self.identity
        basedata = self._basedata.copy()
        basedata['purpose'] = formatter(basedata['purpose'])
        basedata['prerequisite'] = formatter(basedata['prerequisite'])
        basedata['testdata'] = formatter(basedata['testdata'])
        basedata['steps'] = formatter(basedata['steps'])
        basedata['notes'] = formatter(basedata['notes'])
        basedata['testresult'] = formatter(_(afresource.TEST_STATUS_NAME[basedata['testresult']]))
        basedata['testremark'] = formatter(basedata['testremark'])
        basedata['action'] = formatter(basedata['action'])
        basedata['timestamp']  = formatter(basedata['timestamp'])
        return basedata
