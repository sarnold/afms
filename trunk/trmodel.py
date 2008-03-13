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

# Database version, reserved for future use
_DBVERSION = "1.0"

class trModel():
    """
    Class containing all model functions of the MVC pattern
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
        testsuite = model.getTestsuite(testsuite_id)[0]
        testcases_id = model.getTestcasesInTestsuite(testsuite_id)
        
        self.currentdir = os.path.dirname(path)
        self.testrunfilename = path
        if self.currentdir != '':
            os.chdir(self.currentdir)
        logging.debug("trmodel.requestNewTestrun(%s, ...)" % path)
        if os.path.exists(self.testrunfilename):
            os.remove(self.testrunfilename)
        self.connection = sqlite3.connect(self.testrunfilename)
        c = self.connection.cursor()
        c.execute('''create table testrun (property text, value text);''')
        c.execute("insert into testrun values ('product_title', ?);", (product_info["title"],))
        c.execute("insert into testrun values ('creation_date', ?);", (time.strftime("%Y-%m-%d, %H:%M:%S"),))
        c.execute("insert into testrun values ('description', ?);", (description[0],))
        c.execute("insert into testrun values ('tester', ?);", (description[1],))
        c.execute("insert into testrun values ('afdatabase', ?);", (afdatabase,))
        c.execute("insert into testrun values ('testsuite_id', ?);", (testsuite[0],))
        c.execute("insert into testrun values ('testsuite_title', ?);", (testsuite[1],))
        c.execute("insert into testrun values ('testsuite_description', ?);", (testsuite[2],))
        c.execute("insert into testrun values ('testsuite_execorder', ?);", (testsuite[3],))
        c.execute("insert into testrun values ('dbversion', ?);", (_DBVERSION,))
        
        c.execute("create table testcases " \
            "(ID integer primary key, title text, purpose text, prerequisite text,"
            " testdata text, steps text, notes text, version text, "
            " testresult integer, testremark text, action text, timestamp text);")
        sqlstr = "insert into testcases values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        for tc_id in testcases_id:
            testcase = list(model.getTestcase(tc_id)[0])
            testcase.extend([afresource.PENDING, "", "", ""])
            c.execute(sqlstr, testcase)
            
        self.connection.commit()
        
        
    def OpenTestrun(self, path):
        """
        Request to open an existing test run database
        @param path: File name of the test run database
        @type  path: string
        """
        if not os.path.exists(path): raise IOError

        if len(os.path.dirname(path)) > 0:
            self.currentdir = os.path.dirname(path)
        else:
            self.currentdir = os.getcwd()
            path = os.path.join(self.currentdir, path)

        self.testrunfilename = path
        os.chdir(self.currentdir)
        logging.debug("trmodel.requestOpenProduct(%s)" % path)
        self.connection = sqlite3.connect(self.testrunfilename)


    def getTestcaseList(self):
        """
        Get list with all testcases from database
        @rtype:  tuple list
        @return: list with tuples of some basedata from all testcases
        """
        query_string = 'select id, testresult, title from testcases'
        return self.getData(query_string)
    
    
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
        query_string = "select id, title, purpose, prerequisite, testdata, steps, notes, version from testcases where id==%s" % tc_id
        return self.getData(query_string)[0]


    def getTestresult(self, tc_id):
        query_string = "select testresult, testremark, action, timestamp from testcases where id==%s" % tc_id
        return self.getData(query_string)[0]


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


    def saveTestresult(self, tc_id, testresult):
        query_string = "update testcases set 'testresult'=?, 'testremark'=?, 'action'=?, 'timestamp'=? where ID=%d" % tc_id
        c = self.connection.cursor()
        c.execute(query_string, testresult)
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

