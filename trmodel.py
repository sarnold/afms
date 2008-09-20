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

"""
Test run database access

All access to the test run database is done here.
This module implements the model part in the
U{MVC pattern <http://en.wikipedia.org/wiki/Model-view-controller>}

@author: Achim Koehler
@version: $Rev$
"""

import os
import sqlite3
import time
import logging
import afmodel, afresource
import trconfig
import _afartefact
import _trartefact

# Database version, reserved for future use
_DBVERSION = "1.0"

class trModel():
    """
    Class containing all dataase access functions
    """

    def __init__(self, workdir = None):
        """
        Initialize local variables and constants
        """
        self.currentdir = workdir
        if self.currentdir is None:
            self.currentdir = os.getcwd()
        self.testrunfilename = None
        self.connection = None


    def getFilename(self):
        return self.testrunfilename


    def requestNewTestrun(self, path, afdatabase, testsuite_id, description):
        """
        Request to create a new test run
        @param path:         File name for the new test run database
        @type  path:         string
        @param afdatabase:   File name of artefact database with testsuite and testcases
        @type  afdatabase:   string
        @param testsuite_id: ID of test suite to be run
        @type  testsuite_id: integer
        @param description:  Test run description and tester name
        @type  description:  tuple
        """
        model = afmodel.afModel(None)
        model.requestOpenProduct(afdatabase)
        product_info = model.getProductInformation()
        testsuite = model.getTestsuite(testsuite_id)

        self.currentdir = os.path.dirname(path)
        self.testrunfilename = path
        if self.currentdir != '':
            os.chdir(self.currentdir)
        logging.debug("trmodel.requestNewTestrun(%s, ...)" % path)
        if os.path.exists(self.testrunfilename):
            os.remove(self.testrunfilename)
        self.connection = sqlite3.connect(self.testrunfilename.encode('utf-8'))
        c = self.connection.cursor()
        c.execute('''create table testrun (property text, value text);''')
        c.execute("insert into testrun values ('product_title', ?);", (product_info["title"],))
        c.execute("insert into testrun values ('creation_date', ?);", (time.strftime("%Y-%m-%d, %H:%M:%S"),))
        c.execute("insert into testrun values ('description', ?);", (description[0],))
        c.execute("insert into testrun values ('tester', ?);", (description[1],))
        c.execute("insert into testrun values ('afdatabase', ?);", (afdatabase,))
        c.execute("insert into testrun values ('testsuite_id', ?);", (testsuite['ID'],))
        c.execute("insert into testrun values ('testsuite_title', ?);", (testsuite['title'],))
        c.execute("insert into testrun values ('testsuite_description', ?);", (testsuite['description'],))
        c.execute("insert into testrun values ('testsuite_execorder', ?);", (testsuite['execorder'],))
        c.execute("insert into testrun values ('dbversion', ?);", (_DBVERSION,))

        c.execute("create table testcases " \
            "(ID integer primary key, title text, purpose text, prerequisite text,"
            " testdata text, steps text, notes text, version text, "
            " testresult integer, testremark text, action text, timestamp text, scripturl text);")
        sqlstr = "insert into testcases values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        for shorttestcase in testsuite.getRelatedTestcases():
            basetestcase = model.getTestcase(shorttestcase['ID'])
            testcase = _trartefact.cTestcase()
            testcase.importBaseTestcase(basetestcase)
            plaintestcase = [testcase[key] for key in testcase.keys()]
            c.execute(sqlstr, plaintestcase)

        self.connection.commit()


    def OpenTestrun(self, path):
        """
        Request to open an existing test run database
        @param path: File name of the test run database
        @type  path: string
        """
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        if not os.path.exists(path): raise IOError

        self.currentdir = os.path.dirname(path)

        self.testrunfilename = path
        os.chdir(self.currentdir)
        logging.debug("trmodel.requestOpenProduct(%s)" % path)
        self.connection = sqlite3.connect(self.testrunfilename.encode('utf-8'))


    def getTestcaseOverviewList(self):
        """
        Get list with ID, testresult and title from all testcases from database
        @rtype:  object list
        @return: list with testcase object just with some basedata
        """
        query_string = 'select id, testresult, title from testcases'
        testcases = []
        for data in self.getData(query_string):
            testcase = _trartefact.cTestcase(ID=data[0], testresult=data[1], title=data[2])
            testcases.append(testcase)
        return testcases


    def getTestcaseScriptedList(self):
        """
        Get list of all non executed testcases having a script
        @rtype:  object list
        @return: list with testcase object just with some basedata
        """
        query_string = "select id, title, version, purpose, scripturl from testcases where testresult==3 and length(scripturl)>0;"
        testcases = []
        for data in self.getData(query_string):
            testcase = _trartefact.cTestcase(ID=data[0], title=data[1], version=data[2],
                purpose=data[3], scripturl=data[4])
            testcases.append(testcase)
        return testcases


    def getStatusSummary(self):
        """Number of (total, pending, failed, skipped) test cases """
        query_string = 'select testresult from testcases'
        total = len(self.getData(query_string))
        query_string = 'select testresult from testcases where testresult = %s' % afresource.PENDING
        pending = len(self.getData(query_string))
        query_string = 'select testresult from testcases where testresult = %s' % afresource.FAILED
        failed = len(self.getData(query_string))
        query_string = 'select testresult from testcases where testresult = %s' % afresource.SKIPPED
        skipped = len(self.getData(query_string))
        return (total, pending, failed, skipped)


    def getTestcase(self, tc_id):
        query_string = "select id, title, purpose, prerequisite, testdata, steps, " \
                       "scripturl, notes, version, testresult, testremark, action, timestamp  " \
                       "from testcases where id==%s" % tc_id
        d = self.getData(query_string)[0]
        return _trartefact.cTestcase(ID=d[0], title=d[1], purpose=d[2], prerequisite=d[3],
            testdata=d[4], steps=d[5], scripturl=d[6], notes=d[7], version=d[8],
            testresult=d[9], testremark=d[10], action=d[11], timestamp = d[12])


    def getData(self, query_string):
        """
        Simple helper to read data from database
        @type  query_string: string
        @param query_string: SQL select command
        @rtype:  tuple list
        @return: List with query result
        """
        c = self.connection.cursor()
        c.execute(query_string)
        return c.fetchall()


    def saveTestresult(self, testresult):
        query_string = "update testcases set 'testresult'=?, 'testremark'=?, 'action'=?, 'timestamp'=? where ID=%d" % testresult['ID']
        plaintestresult = [testresult['testresult'], testresult['testremark'],
                           testresult['action'], testresult['timestamp']]
        c = self.connection.cursor()
        c.execute(query_string, plaintestresult)
        self.connection.commit()


    def getInfo(self):
        keys = ('product_title', 'creation_date', 'description', 'tester', 'afdatabase',
                'testsuite_id', 'testsuite_title', 'testsuite_description', 'testsuite_execorder')
        retval = []
        c = self.connection.cursor()
        for key in keys:
            query_string = "select value from testrun where property='%s'" % key
            c.execute(query_string)
            retval.append(c.fetchone()[0])
        return retval


    def cancelTestrun(self, reason):
        logging.debug("trmodel.cancelTestrun(%s)" % reason)
        c = self.connection.cursor()
        timestamp = time.strftime(afresource.TIME_FORMAT)
        c.execute("update testcases set 'testresult'=?, 'testremark'=?, 'timestamp'=? where testresult==?", (afresource.SKIPPED, reason, timestamp, afresource.PENDING))
        self.connection.commit()


    def getTestcaseIDs(self, testresult = afresource.FAILED):
        query_string = "select ID from testcases where testresult=%d" % testresult
        return self.getData(query_string)


    def getTestsuiteExecOrder(self):
        c = self.connection.cursor()
        query_string = "select value from testrun where property='testsuite_execorder'"
        c.execute(query_string)
        return c.fetchone()[0]
