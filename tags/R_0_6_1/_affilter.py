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
Several filter classes for each kind of artefacts.
"""

import datetime
import wx
from afmodel import _TYPEID_FEATURE, _TYPEID_REQUIREMENT, _TYPEID_USECASE, _TYPEID_TESTCASE, _TYPEID_TESTSUITE
import afresource


class afNoFilter():
    def isApplied(self):
        return False

    def GetSQLWhereClause(self, prefix=''):
        return ''


class afFilter(object):
    def __init__(self):
        self.applied = False
        self.textfields = []
        self.textcondition = None
        self.textpattern = ''

    def isApplied(self):
        return self.applied

    def _FormatIntList(self, intlist):
        return '(' + ','.join([str(item) for item in intlist]) + ')'

    def _FormatStringList(self, strlist):
        return '(' + ','.join(["'"+unicode(item)+"'" for item in strlist]) + ')'

    def GetSQLWhereClauseForChanges(self):
        if len(self.changedby) > 0:
            s = 'and user=:user'
        else:
            s = ''
        return 'ID in (select afid from lastchanges where aftype=:aftype %s and gettime(date) between gettime(:fromdate) and gettime(:todate))' % s

    def GetSQLWhereClauseForTextfields(self):
        if len(self.textfields) <= 0: return ''
        if len(self.textpattern) <= 0: return ''
        if self.textcondition < 0: return ''
        if self.textcondition in (0, 1):
            # contains the string
            self.textpattern = '%' + self.textpattern + '%'
            op = 'like'
        elif self.textcondition in (2, 3):
            # contains the string (exact case)
            self.textpattern = '*' + self.textpattern + '*'
            op = 'glob'
        elif self.textcondition in (4, 5):
            # contains the word
            self.textpattern = r'\b' + self.textpattern + r'\b'
            op = 'regexp'
        else:
            op = 'regexp'
        if self.textcondition in (1, 3, 5, 7):
            op = 'not ' + op
            joinop = ' and '
        else:
            joinop = ' or '
        clause = []
        for field in self.textfields:
            clause.append('%s %s :pattern' % (field, op))
        return '(' + joinop.join(clause) + ')'


    def GetSQLWhereClauseForTags(self):
        if len(self.tags) <= 0:  return ''
        return 'or '.join(["tags like '%%%c%%'" % tagchar for tagchar in self.tags])


    def appendExpression(self, exprlist, expr):
        if len(expr) > 0:
            exprlist.append(expr)


class afFeatureFilter(afFilter):
    def __init__(self):
        super(afFeatureFilter, self).__init__()

        self.priority = []
        self.status   = []
        self.risk     = []
        self.version  = []
        self.tags     = []
        self.changedfrom = wx.DateTimeFromDMY(1, 1, 2000)
        self.changedto   = wx.Now()
        self.changedby   = None
        self.changedbylist = []

    def SetChangedByList(self, cbl):
        self.changedbylist = cbl

    def SetVersionList(self, vlist):
        self.version = vlist

    def GetSQLWhereClause(self, prefix=''):
        expr = []
        if len(self.priority) > 0:
            expr.append('priority in ' + self._FormatIntList(self.priority))
        if len(self.status) > 0:
            expr.append('status in ' + self._FormatIntList(self.status))
        if len(self.risk) > 0:
            expr.append('risk in ' + self._FormatIntList(self.risk))
        if len(self.version) > 0:
            expr.append('version in ' + self._FormatStringList(self.version))
        expr.append(self.GetSQLWhereClauseForChanges())

        self.appendExpression(expr, self.GetSQLWhereClauseForTextfields())
        self.appendExpression(expr, self.GetSQLWhereClauseForTags())

        clause = ' and '.join(expr)
        clause = prefix + ' ' + clause

        params = {'user': self.changedby,
            'fromdate': self.changedfrom,
            'todate' : self.changedto,
            'pattern': self.textpattern}

        return (clause, params)

#-------------------------------------------------------------------------------

class afRequirementFilter(afFilter):
    def __init__(self):
        super(afRequirementFilter, self).__init__()
        self.priority = []
        self.status   = []
        self.complexity  = []
        self.effort = []
        self.category = []
        self.version  = []
        self.assigned = []
        self.tags = []
        self.changedfrom = wx.DateTimeFromDMY(1, 1, 2000)
        self.changedto   = wx.Now()
        self.changedby   = None
        self.changedbylist = []

    def SetChangedByList(self, cbl):
        self.changedbylist = cbl

    def SetVersionList(self, vlist):
        self.version = vlist

    def SetAssignedList(self, alist):
        self.assigned = alist

    def GetSQLWhereClause(self, prefix=''):
        expr = []
        if len(self.priority) > 0:
            expr.append('priority in ' + self._FormatIntList(self.priority))
        if len(self.status) > 0:
            expr.append('status in ' + self._FormatIntList(self.status))
        if len(self.complexity) > 0:
            expr.append('complexity in ' + self._FormatIntList(self.complexity))
        if len(self.category) > 0:
            expr.append('category in ' + self._FormatIntList(self.category))
        if len(self.effort) > 0:
            expr.append('effort in ' + self._FormatIntList(self.effort))
        if len(self.version) > 0:
            expr.append('version in ' + self._FormatStringList(self.version))
        if len(self.assigned) > 0:
            expr.append('assigned in ' + self._FormatStringList(self.assigned))
        expr.append(self.GetSQLWhereClauseForChanges())

        self.appendExpression(expr, self.GetSQLWhereClauseForTextfields())
        self.appendExpression(expr, self.GetSQLWhereClauseForTags())

        clause = ' and '.join(expr)
        if len(clause) > 0:
            clause = prefix + ' ' + clause

        params = {'user': self.changedby,
            'fromdate': self.changedfrom,
            'todate' : self.changedto,
            'pattern': self.textpattern}

        return (clause, params)

#-------------------------------------------------------------------------------

class afUsecaseFilter(afFilter):
    def __init__(self):
        super(afUsecaseFilter, self).__init__()
        self.priority = []
        self.usefrequency   = []
        self.stakeholders = []
        self.actors = []
        self.changedfrom = wx.DateTimeFromDMY(1, 1, 2000)
        self.changedto   = wx.Now()
        self.changedby   = None
        self.changedbylist = []

    def SetChangedByList(self, cbl):
        self.changedbylist = cbl

    def SetActorsList(self, al):
        self.actors = al

    def SetStakeholdersList(self, sl):
        self.stakeholders = sl

    def GetSQLWhereClause(self, prefix=''):
        expr = []
        if len(self.priority) > 0:
            expr.append('priority in ' + self._FormatIntList(self.priority))
        if len(self.usefrequency) > 0:
            expr.append('usefrequency in ' + self._FormatIntList(self.usefrequency))
        if len(self.stakeholders) > 0:
            expr.append('stakeholders in ' + self._FormatStringList(self.stakeholders))
        if len(self.actors) > 0:
            expr.append('actors in ' + self._FormatStringList(self.actors))
        expr.append(self.GetSQLWhereClauseForChanges())

        self.appendExpression(expr, self.GetSQLWhereClauseForTextfields())
        self.appendExpression(expr, self.GetSQLWhereClauseForTags())

        clause = ' and '.join(expr)
        if len(clause) > 0:
            clause = prefix + ' ' + clause

        params = {'user': self.changedby,
            'fromdate': self.changedfrom,
            'todate' : self.changedto,
            'pattern': self.textpattern}

        return (clause, params)

#-------------------------------------------------------------------------------

class afTestcaseFilter(afFilter):
    def __init__(self):
        super(afTestcaseFilter, self).__init__()
        self.version = []
        self.changedfrom = wx.DateTimeFromDMY(1, 1, 2000)
        self.changedto   = wx.Now()
        self.changedby   = None
        self.changedbylist = []

    def SetChangedByList(self, cbl):
        self.changedbylist = cbl

    def SetVersionList(self, vlist):
        self.version = vlist

    def GetSQLWhereClause(self, prefix=''):
        expr = []
        if len(self.version) > 0:
            expr.append('version in ' + self._FormatStringList(self.version))
        expr.append(self.GetSQLWhereClauseForChanges())

        self.appendExpression(expr, self.GetSQLWhereClauseForTextfields())
        self.appendExpression(expr, self.GetSQLWhereClauseForTags())

        clause = ' and '.join(expr)
        if len(clause) > 0:
            clause = prefix + ' ' + clause

        params = {'user': self.changedby,
            'fromdate': self.changedfrom,
            'todate' : self.changedto,
            'pattern': self.textpattern}

        return (clause, params)

#-------------------------------------------------------------------------------

class afTestsuiteFilter(afFilter):
    def __init__(self):
        super(afTestsuiteFilter, self).__init__()

    def GetSQLWhereClause(self, prefix=''):
        expr = []
        self.appendExpression(expr, self.GetSQLWhereClauseForTextfields())
        self.appendExpression(expr, self.GetSQLWhereClauseForTags())
        clause = ' and '.join(expr)
        if len(clause) > 0:
            clause = prefix + ' ' + clause

        params = {'pattern': self.textpattern}

        return (clause, params)

#-------------------------------------------------------------------------------

class afSimpleSectionFilter(afFilter):
    def __init__(self):
        super(afSimpleSectionFilter, self).__init__()
        self.changedfrom = wx.DateTimeFromDMY(1, 1, 2000)
        self.changedto   = wx.Now()
        self.changedby   = None
        self.changedbylist = []

    def SetChangedByList(self, cbl):
        self.changedbylist = cbl

    def GetSQLWhereClause(self, prefix=''):
        expr = []
        expr.append(self.GetSQLWhereClauseForChanges())
        self.appendExpression(expr, self.GetSQLWhereClauseForTextfields())
        self.appendExpression(expr, self.GetSQLWhereClauseForTags())

        clause = ' and '.join(expr)
        if len(clause) > 0:
            clause = prefix + ' ' + clause

        params = {'user': self.changedby,
            'fromdate': self.changedfrom,
            'todate' : self.changedto,
            'pattern': self.textpattern}
        print clause
        return (clause, params)

