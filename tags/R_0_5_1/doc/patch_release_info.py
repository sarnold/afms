#!/usr/bin/env python
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
Patch release information into a file
Search for lines starting with ':Release:' followed by an arbitrary sequence of characters
and add version number.
"""

import sys, re
sys.path.insert(0, "..")
import version
import fileinput

replacestr = ':Release: %s' % version.VERSION
regexp = re.compile('^:RELEASE:.*', re.I)

for line in fileinput.input():
    sys.stdout.write(regexp.sub(replacestr, line))

