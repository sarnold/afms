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

import logging

ENCODING = 'utf-8'

ARTEFACTS = [{"name": _("Features"),      "id": "FEATURES"},
             {"name": _("Requirements"),  "id": "REQUIREMENTS"},
             {"name": _("Usecases"),      "id": "USECASES"},
             {"name": _("Testcases"),     "id": "TESTCASES"},
             {"name": _("Testsuites"),    "id": "TESTSUITES"}]

ARTEFACTLIST = ["FEATURES", "REQUIREMENTS", "USECASES", "TESTCASES", "TESTSUITES"]
ARTEFACTSHORT = {'USECASES': _('UC'), 'TESTCASES': _('TC'),
                 'REQUIREMENTS': _('RQ'), 'FEATURES': _('FT'), 'TESTSUITES': _('TS')}



TRASH =  {"name": _("Trash"), "id": "TRASH"}

TEXTFILTER = [
_('contains the string'),
_("doesn't contain the string"),
_('contains the string (exact case)'),
_("doesn't contain the string (exact case)"),
_('contains the word'),
_("doesn't contain the word"),
_('matches the regexp'),
_("doesn't match the regexp")
]

PRIORITY_NAME = [_("Essential"), _("Expected"), _("Desired"), _("Optional")]
STATUS_SUBMITTED, STATUS_APPROVED, STATUS_COMPLETED = (0, 1, 2)
STATUS_NAME = [_("Submitted"), _("Approved"), _("Completed")]
EFFORT_NAME = [_("Months"), _("Weeks"), _("Days"), _("Hours")]
COMPLEXITY_NAME = [_("Low"), _("Medium"), _("High")]
CATEGORY_NAME = [_("Functional"), _("Reliability"), _("Up-time"), _("Safety"),
                 _("Security"), _("Performance"), _("Scalability"), _("Maintainability"),
                 _("Upgradability"), _("Supportability"), _("Operability"),
                 _("Business life-cycle"), _("System hardware"), _("System software"),
                 _("API"), _("Data import/export"), _("Other")]
USEFREQUENCY_NAME = [_("Always"), _("Often"), _("Sometimes"), _("Rarely"), _("Once")]
RISK_NAME = [_("Dangerous"), _("3-Risk"), _("2-Risk"), _("1-Risk"), _("Safe")]
CHANGETYPE_NAME = [_('created'), _("edited"), _("deleted"), _("restored")]

FAILED, PASSED, SKIPPED, PENDING = 0, 1, 2, 3
TEST_STATUS_NAME = [_("FAIL"), _("PASS"), _("SKIP"), _("PENDING")]

TIME_FORMAT = "%Y-%m-%d, %H:%M:%S"

AF_WILDCARD = _("AF Database (*.af)|*.af|"     \
                "All files (*.*)|*.*")

HTML_WILDCARD =  _("HTML file (*.html)|*.html|"  \
                   "HTM file (*.htm)|*.htm|"     \
                   "All files (*.*)|*.*")

XML_WILDCARD = _("XML file (*.xml)|*.xml|"  \
                 "All files (*.*)|*.*")

TR_WILDCARD = _("TR Database (*.tr)|*.tr|"     \
                "All files (*.*)|*.*")

_language = 'en'

def SetLanguage(lang):
    global _language
    _language = lang

def GetLanguage():
    return _language
