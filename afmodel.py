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

#TODO: update documentation !!!

"""
Artefact database access

All access to the artefact database is done here.
This module implements the model part in the design.

@author: Achim Koehler
@version: $Rev: 95 $
"""

import os
import sqlite3
import random, time
import logging
import afconfig
import afresource
from _afartefact import cFeature, cRequirement, cUsecase, cTestcase, cTestsuite, cChangelogEntry, cProduct

# Database version, reserved for future use
_DBVERSION = "1.0"

_TYPEID_FEATURE     = 0
_TYPEID_REQUIREMENT = 1
_TYPEID_USECASE     = 2
_TYPEID_TESTCASE    = 3
_TYPEID_TESTSUITE   = 4

_CHANGEID_NEW      = 0
_CHANGEID_EDIT     = 1
_CHANGEID_DELETE   = 2
_CHANGEID_UNDELETE = 3


class afModel():
    """
    Class containing all model functions of the MVC pattern
    """
    
    def __init__(self, controller, workdir = None):
        """
        Initialize local variables and constants
        """
        self.controller = controller
        self.currentdir = workdir
        if self.currentdir is None:
            self.currentdir = os.getcwd()
        self.productfilename = None
        self.connection = None
        self.tablenames = "features requirements usecases testcases testsuites".split()


    def getFilename(self):
        return self.productfilename
    
    
    def requestNewProduct(self, path):
        """
        Request to create a new product
        @param path: File name for the new product database
        @type  path: string
        """
        self.currentdir = os.path.dirname(path)
        self.productfilename = path
        os.chdir(self.currentdir)
        logging.debug("afmodel.(%s)" % path)
        if os.path.exists(self.productfilename):
            os.remove(self.productfilename)
        self.connection = sqlite3.connect(self.productfilename)
        c = self.connection.cursor()
        c.execute('''create table product (property text, value text);''')
        c.execute("insert into product values ('title', '');")
        c.execute("insert into product values ('description', '');")
        c.execute("insert into product values ('dbversion', ?);", (_DBVERSION,))
        c.execute("create table features " \
            "(ID integer primary key autoincrement, title text, priority integer, status integer, version text, risk integer, description text, delcnt integer default 0);")
        c.execute("create table requirements " \
            "(ID integer primary key, title text, priority integer, status integer, version text, complexity integer," \
            "assigned text, effort integer, category integer, origin text, rationale text, description text, delcnt integer default 0);")
        c.execute("create table testcases " \
            "(ID integer primary key, title text, purpose text, prerequisite text, testdata text, steps text, notes text, version text, delcnt integer default 0);")
        c.execute("create table usecases " \
            "(ID integer primary key, title text, priority integer, "\
            "usefrequency integer, actors text, stakeholders text, "\
            "prerequisites text, mainscenario text, altscenario text, notes text, delcnt integer default 0);")
        c.execute("create table testsuites " \
            "(ID integer primary key autoincrement, title text, description text, execorder text, delcnt integer default 0);")
        c.execute("create table changelog" \
            "(afid integer, aftype integer, changetype integer, date text, user text, description text);")
            
        c.execute("create table testsuite_testcase_relation (ts_id integer, tc_id integer, delcnt integer default 0);")
        c.execute("create table requirement_testcase_relation (rq_id integer, tc_id integer, delcnt integer default 0);")
        c.execute("create table requirement_usecase_relation (rq_id integer, uc_id integer, delcnt integer default 0);")
        c.execute("create table feature_requirement_relation (ft_id integer, rq_id integer, delcnt integer default 0);")

        #self.InsertTestData()
        self.connection.commit()


    def requestOpenProduct(self, path):
        """
        Request to open an existing product database
        @param path: File name of the product database
        @type  path: string
        """
        #print path
        if not os.path.exists(path): raise IOError
        if len(os.path.dirname(path)) > 0:
            self.currentdir = os.path.dirname(path)
        else:
            self.currentdir = os.getcwd()
            #print self.currentdir
            path = os.path.join(self.currentdir, path)
            #print path
            
        self.productfilename = path
        os.chdir(self.currentdir)
        logging.debug("afmodel.requestOpenProduct(%s)" % path)
        self.connection = sqlite3.connect(self.productfilename)

    #---------------------------------------------------------------------
    
    def getProductInformation(self):
        """
        Get title and description of product from the database
        @rtype:  dictionary
        @return: Dictionary with keys C{title} and C{description} along with their values
        @note: We rely on the product table to follow the key/value scheme and to have title
               and description as keys
        """
        c = self.connection.cursor()
        c.execute('select * from product;')
        product = cProduct()
        for row in c:
            product[row[0]] = row[1]
        return product
    
    
    def getFeature(self, ID):
        """
        Get a feature from database or new feature with default values
        @param ID: Feature ID
        @type  ID: integer
        @rtype:  feature data tuple
        @return: Tuple with feature data (basedata, related requirements, unrelated requirements)
        @note: If ID < 0 a tuple with predefined data for a new feature is returned
        """
        c = self.connection.cursor()
        
        if ID < 0:
            feature = cFeature()
        else:
            query_string = 'select ID, title, priority, status, version, risk, description from features where ID = %d;' % ID
            c.execute(query_string)
            basedata = c.fetchone()
            feature = cFeature(ID=basedata[0], title=basedata[1], priority=basedata[2],
                               status=basedata[3], version=basedata[4], risk=basedata[5],
                               description=basedata[6])
        
        select_string = 'select rq_id from feature_requirement_relation where ft_id=%d and delcnt==0' % ID
        query_string = 'select ID, title, priority, status, complexity,' \
            'assigned, effort, category, version, description from requirements where id in (%s);' % select_string
        related_requirements_list = self.getData(query_string)
        feature.setRelatedRequirements(self._RequirementListFromPlainList(related_requirements_list))
        
        query_string = 'select ID, title, priority, status, complexity,' \
            'assigned, effort, category, version, description from requirements where id not in (%s) and delcnt==0;' % select_string
        unrelated_requirements_list = self.getData(query_string)
        feature.setUnrelatedRequirements(self._RequirementListFromPlainList(unrelated_requirements_list))
        
        feature.setChangelist(self.getChangelist(_TYPEID_FEATURE, ID))
        return feature
    
    
    def getRequirement(self, ID):
        """
        Get a requirement from database or new requirement with default values
        @param ID: Requirement ID
        @type  ID: integer
        @rtype:  requirement data tuple
        @return: Tuple with requirement data (basedata, related testcases, unrelated testcases, related usecases, unrelated usecase, related festures)
        @note: If ID < 0 a tuple with predefined data for a new requirement is returned
        """
        c = self.connection.cursor()
        
        if ID < 0:
            requirement = cRequirement()
        else:
            query_string = 'select ID, title, priority, status, version, complexity,' \
                'assigned, effort, category, origin, rationale, description from requirements where ID = %d;' % ID
            c.execute(query_string)
            basedata = c.fetchone()
            requirement = cRequirement(ID=basedata[0], title=basedata[1],
                                       priority=basedata[2], status=basedata[3], version=basedata[4],
                                       complexity=basedata[5], assigned=basedata[6], effort=basedata[7],
                                       category=basedata[8], origin=basedata[9], rationale=basedata[10],
                                       description=basedata[11])
        
        select_string = 'select tc_id from requirement_testcase_relation where rq_id=%d and delcnt==0' % ID
        query_string = 'select all id, title, version, purpose from testcases where id in (%s);' % select_string
        c.execute(query_string)
        relatedtestcaselist = self.getData(query_string)
        requirement.setRelatedTestcases(self._TestcaseListFromPlainList(relatedtestcaselist))
        
        query_string = 'select all id, title, version, purpose from testcases where id not in (%s) and delcnt==0;' % select_string
        c.execute(query_string)
        unrelatedtestcaselist = self.getData(query_string)
        requirement.setUnrelatedTestcases(self._TestcaseListFromPlainList(unrelatedtestcaselist))

        select_string = 'select uc_id from requirement_usecase_relation where rq_id=%d and delcnt==0' % ID
        query_string = 'select all id, title, priority, usefrequency, actors, stakeholders from usecases where id in (%s);' % select_string
        c.execute(query_string)
        relatedusecaselist = self.getData(query_string)
        requirement.setRelatedUsecases(self._UsecaseListFromPlainList(relatedusecaselist))
        
        query_string = 'select all id, title, priority, usefrequency, actors, stakeholders from usecases where id not in (%s) and delcnt==0;' % select_string
        c.execute(query_string)
        unrelatedusecaselist = self.getData(query_string)
        requirement.setUnrelatedUsecases(self._UsecaseListFromPlainList(unrelatedusecaselist))
        
        select_string = 'select ft_id from feature_requirement_relation where rq_id=%d and delcnt==0' % ID
        query_string = 'select all ID, title, priority, status, version, risk, description from features where ID in (%s);' % select_string
        c.execute(query_string)
        features = self.getData(query_string)
        requirement.setRelatedFeatures(self._FeatureListFromPlainList(features))

        requirement.setChangelist(self.getChangelist(_TYPEID_REQUIREMENT, ID))
        return requirement

    
    def _FeatureListFromPlainList(self, ftplainlist):
        ftlist = []
        for ft in ftplainlist:
            ftobj = cFeature()
            ftobj['ID'] = ft[0]
            ftobj['title'] = ft[1]
            ftobj['priority'] = ft[2]
            ftobj['status'] = ft[3]
            ftobj['version'] = ft[4]
            ftobj['risk'] = ft[5]
            ftobj['description'] = ft[6]
            ftlist.append(ftobj)
        return ftlist
    
    
    def getTestcase(self, ID):
        """
        Get a testcase from database or new testcase with default values
        @param ID: Testcase ID
        @type  ID: integer
        @rtype:  testcase data tuple
        @return: Tuple with testcase data (basedata, related requirements, related testsuites)
        @note: If ID < 0 a tuple with predefined data for a new testcase is returned
        """
        c = self.connection.cursor()
        if ID < 0:
            testcase = cTestcase()
        else:
            query_string = 'select ID, title, purpose, prerequisite, testdata , steps , notes, version from testcases where ID = %d;' % ID
            c.execute(query_string)
            basedata = c.fetchone()
            testcase = cTestcase(ID=basedata[0], title=basedata[1], purpose=basedata[2],
                                 prerequisite=basedata[3], testdata=basedata[4],
                                 steps=basedata[5], notes=basedata[6], version=basedata[7] )

        select_string = 'select rq_id from requirement_testcase_relation where tc_id=%d and delcnt==0' % ID
        query_string = 'select ID, title, priority, status, complexity,' \
            'assigned, effort, category, version, description from requirements where id in (%s);' % select_string
        c.execute(query_string)
        related_requirements = self.getData(query_string)
        testcase.setRelatedRequirements(self._RequirementListFromPlainList(related_requirements))

        select_string = 'select ts_id from testsuite_testcase_relation where tc_id=%d and delcnt==0' % ID
        query_string = 'select ID, title, description from testsuites where id in (%s);' % select_string
        c.execute(query_string)
        related_testsuites = self.getData(query_string)
        tslist = []
        for ts in related_testsuites:
            tsobj = cTestsuite(ID=ts[0], title=ts[1], description=ts[2])
            tslist.append(tsobj)
        testcase.setRelatedTestsuites(tslist)

        testcase.setChangelist(self.getChangelist(_TYPEID_TESTCASE, ID))
        
        return testcase


    def getUsecase(self, ID):
        """
        Get a usecase from database or new usecase with default values
        @param ID: Usecase ID
        @type  ID: integer
        @rtype:  usecase data tuple
        @return: Tuple with testcase data (basedata, related requirements)
        @note: If ID < 0 a tuple with predefined data for a new usecase is returned
        """
        c = self.connection.cursor()
        if ID < 0:
            usecase = cUsecase()
        else:
            query_string = 'select ID, title, priority, usefrequency, actors, stakeholders, prerequisites, mainscenario, altscenario, notes from usecases where ID = %d;' % ID
            c.execute(query_string)
            basedata = c.fetchone()
            usecase = cUsecase(ID=basedata[0], title=basedata[1], priority=basedata[2],
                               usefrequency=basedata[3], actors=basedata[4],
                               stakeholders=basedata[5], prerequisites=basedata[6],
                               mainscenario=basedata[7], altscenario=basedata[8],
                               notes=basedata[9])

        select_string = 'select rq_id from requirement_usecase_relation where uc_id=%d and delcnt==0' % ID
        query_string = 'select ID, title, priority, status, complexity,' \
            'assigned, effort, category, version, description from requirements where id in (%s);' % select_string
        c.execute(query_string)
        related_requirements = self.getData(query_string)
        
        usecase.setRelatedRequirements(self._RequirementListFromPlainList(related_requirements))
        usecase.setChangelist(self.getChangelist(_TYPEID_USECASE, ID))
        return usecase
    
    
    def _RequirementListFromPlainList(self, rqplainlist):
        rqlist = []
        for rq in rqplainlist:
            rqobj = cRequirement(ID=rq[0], title=rq[1], priority=rq[2], status=rq[3],
                                 complexity=rq[4], assigned=rq[5], effort=rq[6],
                                 category=rq[7], version=rq[8], description=rq[9])
            rqlist.append(rqobj)
        return rqlist
    
    
    def getTestsuite(self, ID):
        """
        Get a testsuite from database or new testsuite with default values
        @param ID: Testsuite ID
        @type  ID: integer
        @rtype:  Testsuite data tuple
        @return: Tuple with testsuite data (basedata, related testcases, unrelated testcases)
        @note: If ID < 0 a tuple with predefined data for a new testsuite is returned
        """
        c = self.connection.cursor()
        
        if ID < 0:
            testsuite = cTestsuite()
        else:
            query_string = 'select ID, title, description, execorder from testsuites where ID = %d;' % ID
            c.execute(query_string)
            basedata = c.fetchone()
            testsuite = cTestsuite(ID=basedata[0], title=basedata[1],
                                   description=basedata[2], execorder=basedata[3])
            
        select_string = 'select tc_id from testsuite_testcase_relation where ts_id=%d and delcnt==0' % ID
        query_string = 'select all id, title, version, purpose from testcases where id in (%s);' % select_string
        includedtestcaselist = self.getData(query_string)
        testsuite.setRelatedTestcases(self._TestcaseListFromPlainList(includedtestcaselist))
        
        query_string = 'select all id, title, version, purpose from testcases where id not in (%s) and delcnt==0;' % select_string
        excludedtestcaselist = self.getData(query_string)
        testsuite.setUnrelatedTestcases(self._TestcaseListFromPlainList(excludedtestcaselist))
        return testsuite
        
        
    def getTestcasesInTestsuite(self, ts_id):
        """
        Get ID's of all testcases in a testsuite 
        @param ID: Testsuite ID
        @type  ID: integer
        @rtype:  list
        @return: Testcase ID's
        """
        query_string = 'select tc_id from testsuite_testcase_relation where ts_id=%d and delcnt==0' % ts_id
        tc_id = self.getData(query_string)
        return [i[0] for i in tc_id]
    
    
    def getChangelist(self, aftype, afid):
        query_string = 'select user, date, description, changetype from changelog where aftype==%d and afid==%d' % (aftype, afid)
        changelist = self.getData(query_string)
        cllist = []
        for cl in changelist:
            clobj = cChangelogEntry(user=cl[0], date=cl[1], description=cl[2], changetype=cl[3])
            cllist.append(clobj)
        return cllist

    
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


    def getIDs(self, tablename):
        """
        Get list with ID's of all elements from given table in database
        @param tablename: table name in database
        @type  tablename: string
        @rtype:  list
        @return: list with all feature ID
        """
        where_string = 'delcnt==0'
        query_string = 'select ID from %s where %s;' % (tablename, where_string)
        return [data[0] for data in self.getData(query_string)];


    def getFeatureIDs(self):
        """
        Get list with all ID's of all features from database
        @rtype:  list
        @return: list with all feature ID
        """
        return self.getIDs('features')


    def getRequirementIDs(self):
        """
        Get list with all ID's of all requirements from database
        @rtype:  list
        @return: list with all requirement ID
        """
        return self.getIDs('requirements')


    def getUsecaseIDs(self):
        """
        Get list with ID's of all usecase from database
        @rtype:  list
        @return: list with all usecase ID
        """
        return self.getIDs('usecases')


    def getTestcaseIDs(self):
        """
        Get list with ID's of all testcases from database
        @rtype:  list
        @return: list with all testcase ID
        """
        return self.getIDs('testcases')
    
    
    def getTestsuiteIDs(self):
        """
        Get list with ID's of all testsuites from database
        @rtype:  list
        @return: list with all testsuite ID
        """
        return self.getIDs('testsuites')

    def getFeatureList(self, deleted=False):
        """
        Get list with all features from database
        @type  deleted: boolean
        @param deleted: If C{True}, a list with all features marked as deleted is returned;
                        Otherways all ordinary features are returned
        @rtype:  tuple list
        @return: list with tuples of basedata from all features  
        """
        if deleted:
            where_string = 'delcnt!=0'
        else:
            where_string = 'delcnt==0'
        query_string = 'select ID, title, priority, status, version, risk, description from features where %s;' % where_string
        plainfeatures = self.getData(query_string)
        return self._FeatureListFromPlainList(plainfeatures)
        
    
    def getRequirementList(self, deleted=False):
        """
        Get list with all requirements from database
        @type  deleted: boolean
        @param deleted: If C{True}, a list with all requirements marked as deleted is returned;
                        Otherways all ordinary requirements are returned
        @rtype:  tuple list
        @return: list with tuples of basedata from all requirements  
        """
        if deleted:
            where_string = 'delcnt!=0'
        else:
            where_string = 'delcnt==0'
        query_string = 'select ID, title, priority, status, complexity, assigned, effort, category, version, description from requirements where %s;' % where_string
        plainrequirements = self.getData(query_string)
        return self._RequirementListFromPlainList(plainrequirements)

    
    def getTestcaseList(self, deleted=False):
        """
        Get list with all testcases from database
        @type  deleted: boolean
        @param deleted: If C{True}, a list with all testcases marked as deleted is returned;
                        Otherways all ordinary testcases are returned
        @rtype:  tuple list
        @return: list with tuples of basedata from all testcases
        """
        if deleted:
            where_string = 'delcnt!=0'
        else:
            where_string = 'delcnt==0'
        query_string = 'select id, title, version, purpose from testcases where %s;' % where_string
        tclist = self.getData(query_string)
        return self._TestcaseListFromPlainList(tclist)
    

    def _TestcaseListFromPlainList(self, tcplainlist):
        tclist = []
        for tc in tcplainlist:
            tcobj = cTestcase()
            tcobj['ID'] = tc[0]
            tcobj['title'] = tc[1]
            tcobj['version'] = tc[2]
            tcobj['purpose'] = tc[3]
            tclist.append(tcobj)
        return tclist


    def getUsecaseList(self, deleted=False, idlist=None):
        """
        Get list with all or some usecases from database
        @type  deleted: boolean
        @param deleted: If C{True}, a list with all usecases marked as deleted is returned;
                        Otherways all ordinary usecases are returned
        @rtype:  tuple list
        @return: list with tuples of basedata from all usecases
        """
        if deleted:
            where_string = 'delcnt!=0'
        else:
            where_string = 'delcnt==0'
        query_string = 'select ID, title, priority, usefrequency, actors, stakeholders from usecases where %s;'  % where_string
        uclist = self.getData(query_string)
        return self._UsecaseListFromPlainList(uclist)
    
    
    def _UsecaseListFromPlainList(self, ucplainlist):
        uclist = []
        for uc in ucplainlist:
            ucobj = cUsecase()
            ucobj['ID'] = uc[0]
            ucobj['title'] = uc[1]
            ucobj['priority'] = uc[2]
            ucobj['usefrequency'] = uc[3]
            ucobj['actors'] = uc[4]
            ucobj['stakeholders'] = uc[5]
            uclist.append(ucobj)
        return uclist

    
    def getTestsuiteList(self, deleted=False):
        """
        Get list with all testsuites from database
        @type  deleted: boolean
        @param deleted: If C{True}, a list with all testsuites marked as deleted is returned;
                        Otherways all ordinary testsuites are returned
        @rtype:  tuple list
        @return: list with tuples of basedata from all testsuites
        """
        if deleted:
            where_string = 'delcnt!=0'
        else:
            where_string = 'delcnt==0'
        query_string = 'select ID, title, description, execorder from testsuites where %s;' % where_string
        tsplainlist = self.getData(query_string)
        tslist = []
        for tsplain in tsplainlist:
            ts = cTestsuite(ID=tsplain[0], title=tsplain[1], description=tsplain[2], execorder=tsplain[3])
            tslist.append(ts)
        
        c = self.connection.cursor()
        # only undeleted testcases are taken into account
        query_string = 'select tc_id from testsuite_testcase_relation where ts_id=? and delcnt==0;'
        for i in range(len(tslist)):
            c.execute(query_string, (tslist[i]['ID'],))
            tslist[i]['nbroftestcase'] = len(c.fetchall())

        return tslist
    
    
    def getArtefactNames(self):
        """
        Return name/title and ID of all (undeleted) artefacts in database
        
        @rtype:  dictionary
        @return: Dictionary with the artefact types as keys. The
                 value of each key is a list with tuples, each tuple containing two
                 values:
                    - ID of artefact
                    - name/title of the artefact
        """
        r = {}
        c = self.connection.cursor()
        for item, tablename in zip(afresource.ARTEFACTS, self.tablenames):
            key = item["id"]
            r[key] = []
            c.execute('select ID, title from %s where delcnt==0;' % tablename)
            for row in c:
                r[key].append((row[0], row[1]))

        return r
    
    
    def getNumberOfDeletedArtefacts(self):
        """
        Get the number of deleted artefacts for each artefact type
        @rtype:  dictionary
        @return: Dictionary with artefact types as keys and number of deleted
                 artefacts as value.
        """
        number_of_deleted_items = {}
        c = self.connection.cursor()
        for item, tablename in zip(afresource.ARTEFACTS, self.tablenames):
            key = item["id"]
            c.execute('select delcnt from %s where delcnt!=0' % tablename)
            number_of_deleted_items[key]= len(c.fetchall())
        return number_of_deleted_items

    #---------------------------------------------------------------------

    ## @brief Save product information to database
    ## @param product_info Dictionary with keys title and description 
    def saveProductInfo(self, product_info):
        """
        Save product info to database
        @param product_info: Dictionary with keys 'title' and 'description'
        @type  product_info: dictionary 
        """
        logging.debug("afmodel.saveProductInfo()")
        c = self.connection.cursor()
        c.execute("update product set 'value'='%s' where property='title'" % product_info['title'])
        c.execute("update product set 'value'='%s' where property='description'" % product_info['description'])
        self.connection.commit()
    

    def saveFeature(self, feature):
        """
        Save feature to database
        @param feature: Tuple with feature basedata and related/unrelated requirements
        @type  feature: tuple
        @return: tuple with updated feature data and boolean flag indication if the 
                 saved artefact is a new artefact
        @rtype:  tuple
        """
        logging.debug("afmodel.saveFeature()")
        plainfeature = [feature['ID'], feature['title'], feature['priority'], feature['status'],
                        feature['version'], feature['risk'], feature['description']]
        plainfeature.append(0) # append delcnt
        sqlstr = []
        sqlstr.append("insert into features values (NULL, ?, ?, ?, ?, ?, ?, ?)")
        sqlstr.append("select max(ID) from features")
        sqlstr.append("update features set "\
            "'title'=?, 'priority'=?, 'status'=?, 'version'=?, 'risk'=?, 'description'=?, " \
            "'delcnt'=? where ID=?;")
        (basedata, new_artefact) = self.saveArtefact(plainfeature, sqlstr)
        ft_id = basedata[0]
        
        c = self.connection.cursor()
        c.execute("delete from feature_requirement_relation where ft_id=?", (ft_id,))
        for rq in feature.getRelatedRequirements():
            c.execute("insert into feature_requirement_relation values (?,?,?)", (ft_id, rq['ID'], 0))

        changelog = feature.getChangelog()
        changelog['changetype'] = [_CHANGEID_EDIT, _CHANGEID_NEW][bool(new_artefact)]
        self.saveChangelog(_TYPEID_FEATURE, ft_id, changelog, False)

        self.connection.commit()

        return (self.getFeature(ft_id), new_artefact)


    def saveRequirement(self, requirement):
        """
        Save requirement to database
        @param requirement: Tuple with requirement basedata, related/unrelated testcases and related/unrelated usecases 
        @type  requirement: tuple
        @return: tuple with updated requirement data and boolean flag indication if the 
                 saved artefact is a new artefact
        @rtype:  tuple
        """
        plainrequirement = [requirement['ID'], requirement['title'], requirement['priority'],
                            requirement['status'], requirement['version'],
                            requirement['complexity'], requirement['assigned'],
                            requirement['effort'], requirement['category'],
                            requirement['origin'], requirement['rationale'],
                            requirement['description']]
        plainrequirement.append(0) # append delcnt
        logging.debug("afmodel.saveRequirement()")
        sqlstr = []
        sqlstr.append("insert into requirements values (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        sqlstr.append("select max(ID) from requirements")
        sqlstr.append("update requirements set "\
            "'title'=?, 'priority'=?, 'status'=?, 'version'=?,"\
            "'complexity'=?, 'assigned'=?, 'effort'=?, 'category'=?,"\
            "'origin'=?, 'rationale'=?, 'description'=?, 'delcnt'=? where ID=?")

        (basedata, new_artefact) = self.saveArtefact(plainrequirement, sqlstr, commit = False)
        rq_id = basedata[0]
        
        related_testcases= requirement.getRelatedTestcases()
        c = self.connection.cursor()
        c.execute("delete from requirement_testcase_relation where rq_id=?", (rq_id,))
        for tc in related_testcases:
            c.execute("insert into requirement_testcase_relation values (?,?,?)", (rq_id, tc['ID'], 0))
        
        related_usecases = requirement.getRelatedUsecases()
        c = self.connection.cursor()
        c.execute("delete from requirement_usecase_relation where rq_id=?", (rq_id,))
        for uc in related_usecases:
            c.execute("insert into requirement_usecase_relation values (?,?,?)", (rq_id, uc['ID'], 0))

        changelog = requirement.getChangelog()
        changelog['changetype'] = [_CHANGEID_EDIT, _CHANGEID_NEW][bool(new_artefact)]
        self.saveChangelog(_TYPEID_REQUIREMENT, rq_id, changelog, False)

        self.connection.commit()

        return (self.getRequirement(rq_id), new_artefact)


    def saveTestcase(self, testcase):
        """
        Save testcase to database
        @param testcase: Tuple with testcase basedata
        @type  testcase: tuple
        @return: tuple with updated testcase data and boolean flag indication if the 
                 saved artefact is a new artefact
        @rtype:  tuple
        """
        logging.debug("afmodel.saveTestcase()")
        plaintestcase = [testcase['ID'], testcase['title'], testcase['purpose'],
                         testcase['prerequisite'], testcase['testdata'],
                         testcase['steps'], testcase['notes'], testcase['version']]
        plaintestcase.append(0) # append delcnt

        sqlstr = []
        sqlstr.append("insert into testcases values (NULL, ?, ?, ?, ?, ?, ?, ?, ?)")
        sqlstr.append("select max(ID) from testcases")
        sqlstr.append("update testcases set "\
            "'title'=?, 'purpose'=?, 'prerequisite'=?, 'testdata'=?,"\
            "'steps'=?, 'notes'=?, 'version'=?, 'delcnt'=? where ID=?")
        (basedata, new_artefact) = self.saveArtefact(plaintestcase, sqlstr)
        tc_id = basedata[0]

        changelog = testcase.getChangelog()
        changelog['changetype'] = [_CHANGEID_EDIT, _CHANGEID_NEW][bool(new_artefact)]
        self.saveChangelog(_TYPEID_TESTCASE, tc_id, changelog, commit = True)

        return (self.getTestcase(tc_id), new_artefact)


    def saveUsecase(self, usecase):
        """
        Save usecase to database
        @param usecase: Tuple with usecase basedata
        @type  usecase: tuple
        @return: tuple with updated usecase data and boolean flag indication if the 
                 saved artefact is a new artefact
        @rtype:  tuple
        """
        logging.debug("afmodel.saveUsecase()")
        plainusecase = [usecase['ID'], usecase['title'], usecase['priority'],
                        usecase['usefrequency'], usecase['actors'],
                        usecase['stakeholders'], usecase['prerequisites'],
                        usecase['mainscenario'], usecase['altscenario'],
                        usecase['notes']]
        changelog = usecase.getChangelog()
        plainusecase.append(0) # append delcnt
        sqlstr = []
        sqlstr.append("insert into usecases values (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        sqlstr.append("select max(ID) from usecases")
        sqlstr.append("update usecases set "\
            "'title'=?, 'priority'=?, 'usefrequency'=?, 'actors'=?, 'stakeholders'=?," \
            "'prerequisites'=?, 'mainscenario'=?,"\
            "'altscenario'=?, 'notes'=?, 'delcnt'=? where ID=?")
        (basedata, new_artefact) = self.saveArtefact(plainusecase, sqlstr, commit = False)
        uc_id = basedata[0]
        
        changelog['changetype'] = [_CHANGEID_EDIT, _CHANGEID_NEW][bool(new_artefact)]
        self.saveChangelog(_TYPEID_USECASE, uc_id, changelog, commit = True)

        return (self.getUsecase(uc_id), new_artefact)

    
    def saveTestsuite(self, testsuite):
        """
        Save testsuite to database
        @param testsuite: Tuple with testsuite basedata and included/excluded testcases 
        @type  testsuite: tuple
        @return: tuple with updated testsuite data and boolean flag indication if the 
                 saved artefact is a new artefact
        @rtype:  tuple
        """
        logging.debug("afmodel.saveTestsuite()")
        plaintestsuite = [testsuite['ID'], testsuite['title'], testsuite['description'], testsuite['execorder']]
        plaintestsuite.append(0) # append delcnt
        sqlstr = []
        sqlstr.append("insert into testsuites values (NULL, ?, ?, ?, ?)")
        sqlstr.append("select max(ID) from testsuites")
        sqlstr.append("update testsuites set "\
            "'title'=?, 'description'=?, execorder=?, 'delcnt'=? where ID=?")
        (basedata, new_artefact) = self.saveArtefact(plaintestsuite, sqlstr, commit=False)
        ts_id = basedata[0]
        
        c = self.connection.cursor()
        c.execute("delete from testsuite_testcase_relation where ts_id=?", (ts_id,))
        for tc in testsuite.getRelatedTestcases():
            c.execute("insert into testsuite_testcase_relation values (?,?,?)", (ts_id, tc['ID'], 0))
        self.connection.commit()

        return (self.getTestsuite(ts_id), new_artefact)
        
        
    def saveArtefact(self, data, sqlstr, commit=True):
        """
        Save basedata of an artefact to database
        @param   data: tuple with artefact basedata
        @type    data: tuple
        @param sqlstr: List with 3 sql command strings
                         - First string is used if a new artefact has to be stored in the database
                         - Second is used to get the ID of a new artefact,
                         - Third string is used if existing artefact data has to be updated
        @type  sqlstr: list
        @param commit: Flag indicating if  commit command should be issued
        @type  commit: boolean
        @return:       Tuple with artefact data and flog indication a new artefact
        @rtype:        boolean
        """
        c = self.connection.cursor()
        ID = data[0]
        if ID < 0:
            # save new artefact
            c.execute(sqlstr[0], data[1:])
            # get ID of new artefact
            c.execute(sqlstr[1])
            data = c.fetchone() + tuple(data[1:])
            new_artefact = True
        else:
            new_artefact = False
            args = tuple(data[1:]) + (data[0],)
            c.execute(sqlstr[2], args)
        if commit:
            self.connection.commit()
        return (data, new_artefact)

            
    def saveChangelog(self, aftype, afid, changelog, commit = False):
        c = self.connection.cursor()
        savedata = (afid, aftype, changelog['changetype'], changelog['date'],
                    changelog['user'], changelog['description'])
        c.execute('insert into changelog values (?, ?, ?, ?, ?, ?)', savedata)
        if commit:
            self.connection.commit()

    #---------------------------------------------------------------------
    
    
    def requestAssignedList(self):
        """
        Get list with all assigned entries from requirements
        @return: Unique list with all entries of the assigned field of requirements
        @rtype:  list
        """
        query_string = 'select distinct assigned from requirements order by assigned asc;'
        c = self.connection.cursor()
        c.execute(query_string)
        return [item[0] for item in c.fetchall()]
    
    
    def requestActorList(self):
        """
        Get list with all actor entries from usecases
        @return: Unique list with all entries of the actor field of usecases
        @rtype:  list
        """
        query_string = 'select distinct actors from usecases order by actors asc;'
        c = self.connection.cursor()
        c.execute(query_string)
        return [item[0] for item in c.fetchall()]


    def requestStakeholderList(self):
        """
        Get list with all stakeholders entries from usecases
        @return: Unique list with all entries of the stakeholders  field of usecases
        @rtype:  list
        """
        query_string = 'select distinct stakeholders from usecases order by stakeholders asc;'
        c = self.connection.cursor()
        c.execute(query_string)
        return [item[0] for item in c.fetchall()]
    
    #---------------------------------------------------------------------
    
    def deleteFeature(self, item_id, delcnt=1):
        """
        Delete a feature and it's relations
        
        Actually the feature is not deleted from the database. Instead, the delcnt
        column of the feature is set to 1 to indicated that the feature is deleted.
        Reseting the delcnt column to 0 means undeleting the feature.
        A similar approach is used for feature/requirements relation. When deleting
        a feature (or a requirement) the delcnt value of all corresponding rows in the table
        feature_requirement_relation is incremented. On undeleting the feature
        (or the requirement) the delcnt value is decremented and the relation
        only becomes 'undeleted' when both the feature and the requirement are not deleted.
        
        @type  item_id: integer
        @param item_id: Feature ID
        @type   delcnt: integer
        @param  delcnt: a value of 0 means restore the feature,
                        a value > 0 means delete the feature
        @rtype:  tuple
        @return: Basedata of the feature
        """
        logging.debug("afmodel.deleteFeature(%i, delcnt=%d)" % (item_id, delcnt))
        c = self.connection.cursor()
        c.execute("update features set delcnt=? where id=?", (delcnt, item_id))
        if delcnt > 0:
            incr = 1
            changetype = _CHANGEID_DELETE
        else:
            incr = -1
            changetype = _CHANGEID_UNDELETE
            
        c.execute("select all ft_id, rq_id, delcnt from feature_requirement_relation where ft_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update feature_requirement_relation set delcnt=? where ft_id=? and rq_id=?", (new_delcnt, row[0], row[1]))

        cle = cChangelogEntry(user=self.controller.getUsername(),
                              description='',
                              date=self.controller.getCurrentTimeStr(),
                              changetype=changetype)
        self.saveChangelog(_TYPEID_FEATURE, item_id, cle, False)
        
        self.connection.commit()
        return self.getFeature(item_id)

    
    ## @brief Delete a requirement from database
    ## @param item_id ID of the requirement
    ##
    def deleteRequirement(self, item_id, delcnt=1):
        """
        Delete a feature and it's relations

        See L{deleteFeature} for details.
        @type  item_id: integer
        @param item_id: Requirement ID
        @type   delcnt: integer
        @param  delcnt: a value of 0 means restore the requirement,
                        a value > 0 means delete the requirement
        @rtype:  tuple
        @return: Basedata of the requirement
        """
        logging.debug("afmodel.deleteRequirement(%i, delcnt=%d)" % (item_id, delcnt))
        c = self.connection.cursor()
        c.execute("update requirements set delcnt=? where id=?", (delcnt, item_id))
        if delcnt > 0:
            incr = 1
            changetype = _CHANGEID_DELETE
        else:
            incr = -1
            changetype = _CHANGEID_UNDELETE

        c.execute("select all ft_id, rq_id, delcnt from feature_requirement_relation where rq_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update feature_requirement_relation set delcnt=? where ft_id=? and rq_id=?", (new_delcnt, row[0], row[1]))

        c.execute("select all rq_id, tc_id, delcnt from requirement_testcase_relation where rq_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update requirement_testcase_relation set delcnt=? where rq_id=? and tc_id=?", (new_delcnt, row[0], row[1]))

        c.execute("select all rq_id, uc_id, delcnt from requirement_usecase_relation where rq_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update requirement_usecase_relation set delcnt=? where rq_id=? and uc_id=?", (new_delcnt, row[0], row[1]))

        cle = cChangelogEntry(user=self.controller.getUsername(),
                              description='',
                              date=self.controller.getCurrentTimeStr(),
                              changetype=changetype)
        self.saveChangelog(_TYPEID_REQUIREMENT, item_id, cle, False)

        self.connection.commit()
        return self.getRequirement(item_id)


    def deleteTestcase(self, item_id, delcnt=1):
        """
        Delete a testcase and it's relations

        See L{deleteFeature} for details.
        @type  item_id: integer
        @param item_id: Testcase ID
        @type   delcnt: integer
        @param  delcnt: a value of 0 means restore the testcase,
                        a value > 0 means delete the testcase
        @rtype:  tuple
        @return: Basedata of the testcase
        """
        logging.debug("afmodel.deleteTestcase(%i)" % item_id)
        c = self.connection.cursor()
        c.execute("update testcases set delcnt=? where id=?", (delcnt, item_id))
        if delcnt > 0:
            incr = 1
            changetype = _CHANGEID_DELETE
        else:
            incr = -1
            changetype = _CHANGEID_UNDELETE

        c.execute("select all ts_id, tc_id, delcnt from testsuite_testcase_relation where tc_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update testsuite_testcase_relation set delcnt=? where ts_id=? and tc_id=?", (new_delcnt, row[0], row[1]))

        c.execute("select all rq_id, tc_id, delcnt from requirement_testcase_relation where tc_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update requirement_testcase_relation set delcnt=? where rq_id=? and tc_id=?", (new_delcnt, row[0], row[1]))

        cle = cChangelogEntry(user=self.controller.getUsername(),
                              description='',
                              date=self.controller.getCurrentTimeStr(),
                              changetype=changetype)
        self.saveChangelog(_TYPEID_TESTCASE, item_id, cle, False)

        self.connection.commit()
        return self.getTestcase(item_id)
        
        
    def deleteUsecase(self, item_id, delcnt=1):
        """
        Delete a usecase and it's relations

        See L{deleteFeature} for details.
        @type  item_id: integer
        @param item_id: Usecase ID
        @type   delcnt: integer
        @param  delcnt: a value of 0 means restore the usecase,
                        a value > 0 means delete the usecase
        @rtype:  tuple
        @return: Basedata of the usecase
        """
        logging.debug("afmodel.deleteUsecase(%i)" % item_id)
        c = self.connection.cursor()
        c.execute("update usecases set delcnt=? where id=?", (delcnt, item_id))
        if delcnt > 0:
            incr = 1
            changetype = _CHANGEID_DELETE
        else:
            incr = -1
            changetype = _CHANGEID_UNDELETE

        c.execute("select all rq_id, uc_id, delcnt from requirement_usecase_relation where uc_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update requirement_usecase_relation set delcnt=? where rq_id=? and uc_id=?", (new_delcnt, row[0], row[1]))

        cle = cChangelogEntry(user=self.controller.getUsername(),
                              description='',
                              date=self.controller.getCurrentTimeStr(),
                              changetype=changetype)
        self.saveChangelog(_TYPEID_USECASE, item_id, cle, False)

        self.connection.commit()
        return self.getUsecase(item_id)


    def deleteTestsuite(self, item_id, delcnt=1):
        """
        Delete a testsuite and it's relations

        See L{deleteFeature} for details.
        @type  item_id: integer
        @param item_id: Testsuite ID
        @type   delcnt: integer
        @param  delcnt: a value of 0 means restore the testsuite,
                        a value > 0 means delete the testsuite
        @rtype:  tuple
        @return: Basedata of the testsuite
        """
        logging.debug("afmodel.deleteTestsuite(%i)" % item_id)
        c = self.connection.cursor()
        c.execute("update testsuites set delcnt=? where id=?", (delcnt, item_id))
        if delcnt > 0:
            incr = 1
        else:
            incr = -1

        c.execute("select all ts_id, tc_id, delcnt from testsuite_testcase_relation where ts_id=?", (item_id,))
        rows = c.fetchall()
        for row in rows:
            new_delcnt = max(0, row[2] + incr) # prevent delcnt < 0
            c.execute("update testsuite_testcase_relation set delcnt=? where ts_id=? and tc_id=?", (new_delcnt, row[0], row[1]))

        self.connection.commit()
        return self.getTestsuite(item_id)

    #---------------------------------------------------------------------

    def addFeatureRequirementRelation(self, ft_id, rq_id):
        """
        Add a new relation to the feature_requirement_relation table
        @param ft_id: Feature ID
        @type  ft_id: integer
        @param rt_id: Requirement ID
        @type  rt_id: integer
        """
        self._AddRelation(("feature_requirement_relation", "ft_id", "rq_id"), ft_id, rq_id)
        
    
    def addTestsuiteTestcaseRelation(self, ts_id, tc_id):
        """
        Add a new relation to the testsuite_testcase_relation table
        @param ts_id: Testsuite ID
        @type  ts_id: integer
        @param tc_id: Testcase ID
        @type  tc_id: integer
        """
        self._AddRelation(("testsuite_testcase_relation", "ts_id", "tc_id"), ts_id, tc_id)
    
    
    def addRequirementUsecaseRelation(self, rq_id, uc_id):
        """
        Add a new relation to the requirement_usecase_relation table
        @param rq_id: Requirement ID
        @type  rq_id: integer
        @param uc_id: Usecase ID
        @type  uc_id: integer
        """
        self._AddRelation(("requirement_usecase_relation", "rq_id", "uc_id"), rq_id, uc_id)
        
    
    def addRequirementTestcaseRelation(self, rq_id, tc_id):
        """
        Add a new relation to the requirement_testcase_relation table
        @param rq_id: Requirement ID
        @type  rq_id: integer
        @param tc_id: Testcase ID
        @type  tc_id: integer
        """
        self._AddRelation(("requirement_testcase_relation", "rq_id", "tc_id"), rq_id, tc_id)
        
    
    def _AddRelation(self, table, left_id, right_id):
        """
        Base function to add a new relation to a table in the database
        @param    table: name of the ralation table
        @type     table: string
        @param  left_id: artefact ID, left table column
        @type   left_id: integer
        @param right_id: artefact ID, right table column
        @type  right_id: integer
        """
        c = self.connection.cursor()
        c.execute("select * from %s where %s=? and %s=?" % table, (left_id, right_id))
        if c.fetchone() is not None: return
        c.execute("insert into %s values (?,?,?)" % table[0], (left_id, right_id, 0))
        self.connection.commit()

    #---------------------------------------------------------------------

    def getFeatureRequirementRelations(self):
        """Get feature_requirement_relation table"""
        return self._getRelations("feature_requirement_relation", "ft_id", "rq_id")


    def getTestsuiteTestcaseRelations(self):
        """Get testsuite_testcase_relation table"""
        return self._getRelations("testsuite_testcase_relation", "ts_id", "tc_id")


    def getRequirementUsecaseRelations(self):
        """Get requirement_usecase_relation table"""
        return self._getRelations("requirement_usecase_relation", "rq_id", "uc_id")


    def getRequirementTestcaseRelations(self):
        """Get requirement_testcase_relation table"""
        return self._getRelations("requirement_testcase_relation", "rq_id", "tc_id")


    def _getRelations(self, tablename, leftcolname, rightcolname):
        c = self.connection.cursor()
        c.execute("select %s, %s from %s" % (leftcolname, rightcolname, tablename))
        return c.fetchall()
        
    #---------------------------------------------------------------------

    def getRequirementIDsReleatedToFeature(self, ft_id):
        query_string = 'select rq_id from feature_requirement_relation where ft_id=%d and delcnt==0' % ft_id
        return [data[0] for data in self.getData(query_string)];
    
    
    def getTestcaseIDsRelatedToRequirement(self, rq_id):
        query_string = 'select tc_id from requirement_testcase_relation where rq_id=%d and delcnt==0' % rq_id
        return [data[0] for data in self.getData(query_string)];


    def getUsecaseIDsRelatedToRequirement(self, rq_id):
        query_string = 'select uc_id from requirement_usecase_relation where rq_id=%d and delcnt==0' % rq_id
        return [data[0] for data in self.getData(query_string)];
    
    
    def getTestcaseIDsRelatedToTestsuite(self, ts_id):
        query_string = 'select tc_id from testsuite_testcase_relation where ts_id=%d and delcnt==0' % ts_id
        return [data[0] for data in self.getData(query_string)];

    #---------------------------------------------------------------------

    def InsertTestData(self):
        """
        Insert testdata into database.
        """
        c = self.connection.cursor()
        c.execute("""insert into product values ('title', 'Sample product');""")
        s = \
        """
        This is a very <b>long</b> sample page description.
        This is a very <b>long</b> sample page description.
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <a href="http://www.google.de">long</a> sample page description. <br>
        <a href="file://test.htm">Link zu Datei</a>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        This is a very <b>long</b> sample page description. <br>
        """
        c.execute("insert into product values ('description', '%s');" % s)
        
        for i in range(20):
            title = "Feature %d" % i
            priority = random.randint(0,2)
            version = random.randint(1,10)
            status = random.randint(0,2)
            risk = random.randint(0,4)
            description = "Description of feature %d" % i
            c.execute("insert into features values (NULL, ?, ?, ?, ?, ?, ?, ?)", (title, priority, status, version, risk, description, 0) )

        for i in range(4):
            title = "Title %d" % i
            description = "Desc %d" % i
            c.execute("insert into testsuites values (NULL, ?, ?, ?, ?)", (title, description, "", 0) )

        for i in range(5,11):
            title = "Testcase %d" % i
            purpose = "Purpose %d" % i
            prerequisite = "Prereq %d" % i
            testdata = "Testdata %d" % i
            steps = "Steps %d" % i
            notes = "Notes %d" % i
            version = random.randint(1,10)
            c.execute("insert into testcases values (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (title, purpose, prerequisite, testdata, steps, notes, version, 0) )

        c.execute("insert into feature_requirement_relation values (2, 3, 0);")
        c.execute("insert into feature_requirement_relation values (2, 4, 0);")
        c.execute("insert into feature_requirement_relation values (2, 5, 0);")
        c.execute("insert into feature_requirement_relation values (3, 5, 0);")
        


        c.execute("insert into testsuite_testcase_relation values (1, 1, 0);")
        c.execute("insert into testsuite_testcase_relation values (1, 2, 0);")
        c.execute("insert into testsuite_testcase_relation values (3, 2, 0);")
        c.execute("insert into testsuite_testcase_relation values (3, 3, 0);")
        c.execute("insert into testsuite_testcase_relation values (3, 6, 0);")

        c.execute("insert into requirement_testcase_relation values (3, 3, 0);")
        c.execute("insert into requirement_testcase_relation values (3, 6, 0);")

        c.execute("insert into requirement_usecase_relation values (3, 3, 0);")
        c.execute("insert into requirement_usecase_relation values (3, 4, 0);")

        for i in range(4):
            title = "Summary %d" % i
            priority = random.randint(1,3)
            usefrequency = random.randint(1,3)
            actors = "Actors %d" %i
            stakeholders = "stakeholders %d" %i
            prerequisites = "prerequisites %d" %i
            mainscenario = "mainscenario %d" %i
            altscenario = "altscenario %d" %i
            notes = "notes %d" %i
            c.execute("insert into usecases values (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (title, priority, usefrequency, actors, stakeholders, prerequisites, mainscenario, altscenario, notes, 0) )

        for i in range (45,54):
            title = "Req %d" % i
            description = "Desc"
            status = random.randint(0,2)
       	    complexity = random.randint(0,2)
            assigned = "Someone"
            effort = random.randint(0,2)
            priority = random.randint(0,2)
            category = random.randint(0,14)
            origin = "Origin"
            rationale = "Rationale"
            version = random.randint(1,10)
            created = "2007/12/07 20:%02d:00" % random.randint(0,59)
            c.execute("insert into requirements values (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (title, priority, status, version, complexity, assigned, effort, category, origin, rationale, description, 0) )


        for i in range(6):
            description = "Description %d" % i
            afid = 1
            aftype = 0
            changetype = 1
            user = "Change author"
            date = time.strftime(afresource.TIME_FORMAT)
            c.execute("insert into changelog values (?, ?, ?, ?, ?, ?)",
                (afid, aftype, changetype, date, user, description))

            
