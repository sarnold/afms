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
Main test script for afeditor testing

Collect test suites from several test scripts and run contained testcases.
"""

import unittest
import test_afeditor_createartefacts, test_afeditor_verifyartefactlists
import test_afeditor_statistics, test_afeditor_verifyartefactcontents
import test_afeditor_deleteartefacts, test_afeditor_editartefacts
import test_afexportxml

suitelist = []
suitelist.append(test_afeditor_createartefacts.getSuite())
suitelist.append(test_afeditor_verifyartefactlists.getSuite())
suitelist.append(test_afeditor_verifyartefactcontents.getSuite())
suitelist.append(test_afeditor_statistics.getSuite())
suitelist.append(test_afeditor_deleteartefacts.getSuite())
suitelist.append(test_afeditor_editartefacts.getSuite())
suitelist.append(test_afexportxml.getSuite())
suite  = unittest.TestSuite(suitelist)

unittest.TextTestRunner(verbosity=2).run(suite)

