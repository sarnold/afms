# -*- coding: latin-1  -*-

# -------------------------------------------------------------------
# Copyright 2008 Achim K�hler
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

import logging

ENCODING = 'utf-8'

ARTEFACTS = [{"name": "Features",      "id": "FEATURES"},
             {"name": "Requirements",  "id": "REQUIREMENTS"},
             {"name": "Usecases",      "id": "USECASES"},
             {"name": "Testcases",     "id": "TESTCASES"},
             {"name": "Testsuites",    "id": "TESTSUITES"}]

TRASH =  {"name": "Trash", "id": "TRASH"}

PRIORITY_NAME = ["Essential", "Expected", "Desired", "Optional"]
STATUS_SUBMITTED, STATUS_APPROVED, STATUS_COMPLETED = (0, 1, 2)
STATUS_NAME = ["Submitted", "Approved", "Completed"]
EFFORT_NAME = ["Months", "Weeks", "Days", "Hours"]
COMPLEXITY_NAME = ["Low", "Medium", "High"]
CATEGORY_NAME = ["Functional", "Reliability", "Up-time", "Safety",
                 "Security", "Performance", "Scalability", "Maintainability",
                 "Upgradability", "Supportability", "Operability",
                 "Business life-cycle", "System hardware", "System software",
                 "API", "Data import/export", "Other"]
USEFREQUENCY_NAME = ["Always", "Often", "Sometimes", "Rarely", "Once"]
RISK_NAME = ["Dangerous", "3-Risk", "2-Risk", "1-Risk", "Safe"]
CHANGETYPE_NAME = ['created', "edited", "deleted", "restored"]

FAILED, PASSED, SKIPPED, PENDING = 0, 1, 2, 3
TEST_STATUS_NAME = ["FAIL", "PASS", "SKIP", "PENDING"]

TIME_FORMAT = "%Y-%m-%d, %H:%M:%S"

AF_WILDCARD_EN = "AF Database (*.af)|*.af|"     \
                 "All files (*.*)|*.*"

HTML_WILDCARD_EN =  "HTML file (*.html)|*.html|"  \
                    "HTM file (*.htm)|*.htm|"     \
                    "All files (*.*)|*.*"

XML_WILDCARD_EN = "XML file (*.xml)|*.xml|"  \
                  "All files (*.*)|*.*"

AF_WILDCARD_DE =    "AF Datenbank (*.af)|*.af|"     \
                    "Alle Dateien (*.*)|*.*"

HTML_WILDCARD_DE =  "HTML Datei (*.html)|*.html|"  \
                    "HTM Datei (*.htm)|*.htm|"     \
                    "Alle Dateien (*.*)|*.*"

XML_WILDCARD_DE = "XML Datei (*.xml)|*.xml|"  \
                  "Alle Dateien (*.*)|*.*"
                  
TR_WILDCARD_EN = "TR Database (*.tr)|*.tr|"     \
                 "All files (*.*)|*.*"


AF_WILDCARD = AF_WILDCARD_EN
HTML_WILDCARD = HTML_WILDCARD_EN
XML_WILDCARD = XML_WILDCARD_EN
TR_WILDCARD = TR_WILDCARD_EN

# set dynamically
ASSIGNED_NAME = []
ACTOR_NAME = []
STAKEHOLDER_NAME = []


RESOURCE_DE = {\
'Title'                 : u'Titel',
'ID'                    : u'ID',
'Version'               : u'Version',
'Priority'              : u'Priorit�t',
'Status'                : u'Status',
'Risk'                  : u'Risiko',
'Description'           : u'Beschreibung',
'Feature'               : u'Feature',
'Attached Requirements' : u'Zugeh�rige Anforderungen',
'Empty field not allowed' : u'Leerer Eintrag nicht erlaubt',
'Date'                  : u'Datum',
'User'                  : u'Benutzer',
'Changelog'             : u'�nderungen',
'Purpose'               : u'Zweck',
'Prerequisite'          : u'Voraussetzungen',
'Testdata'              : u'Testdaten',
'Steps'                 : u'Schritte',
'Notes && Questions'    : u'Hinweise && Fragen',
"Notes &&\nQuestions"   : u"Hinweise &&\nFragen",
'Testcase'              : u'Testfall',
'Related Requirements'  : u'Zugeh�rige Anforderungen',
'Related Testsuites'    : u'Zugeh�rige Testsuiten',
"Execution order ID's"  : u'Ausf�hrungsreihenfolge ID',
'Testcases'             : u'Testf�lle',
"Syntax error in execution order"
                        : u"Syntaxfehler in Ausf�hrungsreihenfolge",
"Some testcase ID's in this testsuite are not listed in execution order"
                        : u"Einige Testfall-ID sind nicht in der Ausf�hrungsreihenfolge",
"Some testcase ID's in execution order are not in this testsuite"
                        : u"Einige Testfall-ID in der Ausf�hrungsreihenfolge sind nicht in der Testsuite",
"Save new product to file"  : u"Neues Produkt speichern unter",
'Error creating product'    : u'Fehler bei der Erstellung des Produktes',
"Open product file"         : u'Produkt �ffnen',
'Error opening product!'    : u'Fehler beim �ffnen des Produktes',
"Really delete artefact?"   : u"Artefact wirklich l�schen?",
"Delete artefact"           : u"Artefakt l�schen",
"Save HTML to file"         : u"HTML speichern unter",
'Error exporting to HTML!'  : u"Fehler beim HTML-Export",
"Save XML to file"          : u"XML speichern unter",
'Error exporting to XML!'   : u"Fehler beim XML-Export",
"Edit Product"              : u"Produkt editieren",
"Edit feature"              : u"Feature editieren",
"Edit requirement"          : u"Anforderung editieren",
"Artefact is already approved!\nChangelog description is required."
                            : u"Artefakt ist bereits freigegeben!\nEine �nderungsbeschreibung ist erforderlich.",
"Artefact is already completed!\nChanges are prohibited!"
                            : u"Artefact is abgeschlossen!\n�nderungen sind nicht erlaubt!",
"Edit testcase"             : u"Testfall editieren",
"Edit usecase"              : u"Anwendungsfall editieren",
"Edit testsuite"            : u"Testsuite editieren",
'Error saving artefact'     : u"Fehler beim Speichern des Artefakts",
"Really restore artefact?"  : u"Artefakt wirklich wiederherstellen?",
"Restore artefact"          : u"Artefakt wiederherstellen",
'Complexity'                : u'Komplexit�t',
'Assigned'                  : u'Zugewiesen',
'Effort'                    : u'Aufwand',
'Category'                  : u'Kategorie',
'Summary'                   : u'Zusammenfassung',
'Use freq.'                 : u'H�ufigkeit',
'Actors'                    : u'Akteure',
'Stakeholders'              : u'Interessengruppen',
"Don't ask again in this session"
                            : u'In dieser Sitzung nicht mehr fragen',
"Unable to execute %s\nScript execution is disabled."
                            : u'Skript %s kann nicht ausgef�hrt werden.\nSkriptausf�hrung ist gesperrt.',
'New'                       : u'Neu',
'New Product'               : u'Neues Produkt',
'Create new product'        : u'Neues Produkt erstellen',
'Open'                      : u'�ffnen',
'Open Product'              : u'Produkt �ffnen',
'Open existing product'     : u'Vorhandenes Produkt �ffnen',
'Edit'                      : u'Bearbeiten',
'Edit artefact'             : u'Artefakt editieren',
'Edit selected artefact'    : u'Ausgew�hltes Artefakt editieren',
'Delete'                    : u'L�schen',
'Delete selected artefact'  : u'Ausgew�hltes Artefakt l�schen',
'New feature'               : u'Neues Feature',
'Create new feature'        : u'Neues Feature erstellen',
'New requirement'           : u'Neue Anforderung',
'Create/attach new requirement' : u'Neue Anforderung erstellen',
'New usecase'                   : u'Neuer Anwendungsfall',
'Create/attach new usecase'     : u'Neuen Anwendungsfall erstellen/zuordnen',
'New testcase'                  : u'Neuer Testfall',
'Create/attach new testcase'    : u'Neuen Testfall erstellen/zuordnen',
'New testsuite'                 : u'Neue Testsuite',
'Create new testsuite'          : u'Neue Testsuite erstellen',
'&New product ...\tCtrl-N'      : u'&Neues Produkt ...\tCtrl-N',
'&Open product ...\tCtrl-O'     : u'&�ffne Produkt ...\tCtrl-O',
'Export as HTML ...'            : u'Exportiere als HTML ...',
'Export product to HTML file'   : u'Exportiere Produkt im HTML-Format',
'Export as XML ...'             : u'Exportiere als XML ...',
'Export product to XML files'   : u'Exportiere Produkt im XML-Format',
'E&xit\tAlt-X'                  : u'B&eenden\tAlt-X',
'Exit this application'         : u'Anwendung beenden',
'&File'                         : u'&Datei',
'&Edit artefact ...\tCtrl-E'    : u'Artefakt editieren ...\tCtrl-E',
'&Delete artefact ...\tDel'     : u'Artefakt l�schen ...\tDel',
'&Copy artefact\tCtrl-C'        : u'Artefakt kopieren\tCtrl-C',
'Copy selected artefact to clipboard'
                                : u'Ausgew�hltes Artefakt in die Zwischenablage kopieren',
'&Paste artefact\tCtrl-V'       : u'Artefakt einf�gen\tCtrl-V',
'Paste artefact from clipboard' : u'Artefakt aus Zwischenablage einf�gen',
'Copy'                          : u'Kopieren',
'Copy artefact'                 : u'Kopiere Artefakt',
'Paste'                         : u'Einf�gen',
'Paste artefact'                : u'Artefakt einf�gen',
'&Edit'                         : u'B&earbeiten',
'New &feature ...'              : u'Neues &Feature',
'New &requirement ...'          : u'Neue &Anforderung',
'Create new requirement'        : u'Neue Anforderung erstellen',
'New &usecase ...'              : u'Ne&uer Anwendungsfall',
'Create new usecase'            : u'Neuen Anwendungsfall erstellen',
'New &testcase ...'             : u'Neuer &Testfall',
'Create new testcase'           : u'Neuen Testfall erstellen',
'New test&suite ...'            : u'Neue Test&suite',
'&New'                          : u'&Neu',
'About ...'                     : u'�ber ...',
'Info about this program'       : u'Information �ber dieses Programm',
'&Help'                         : u'&Hilfe',
'Product'                       : u'Produkt',
'Use frequency'                 : u'H�ufigkeit',
'Prerequisites'                 : u'Vorbedingungen',
'Main scenario'                 : u'Hauptszenario',
'Alt scenario'                  : u'Alternativszenario',
'Notes'                         : u'Anmerkungen',
'Usecase'                       : u'Anwendungsfall',
'&Settings'                     : u'Einstellungen',
'Language ...'                  : u'Sprache ...',
'Set language'                  : u'Sprache ausw�hlen',
'Select program language\n(This takes effect after restarting the program.)'
                                : u'Programmsprache w�hlen\n(Wirksam erst nach Neustart.)',
'Select language'               : u'Sprache ausw�hlen',
'English'                       : u'Englisch',
'German'                        : u'Deutsch',
"Editor for the Artefact Management System"
                                : u'Editor f�r das Artefakt Management System',
"This list could not be edited here"
                                : u'Diese Liste kann hier nicht bearbeitet werden.',
'Origin'                        : u'Herkunft',
'Rationale'                     : u'Erkl�rung',
'Requirement'                   : u'Anforderung',
'Attached Testcases'            : u'Zugeordnete Testf�lle',
'Attached Usecases'             : u'Zugeordnete Anwendungsf�lle',
'Related Features'              : u'Zugeh�rige Features',
"Unknown"                       : u'Unbekannt',
"Trash overview"                : u'�bersicht Papierkorb',
"Number of %s in Trash:"        : u'Anzahl %s im Papierkorb:',
"Requirements"                  : u'Anforderungen',
"Usecases"                      : u"Anwendungsf�lle",
"Testsuites"                    : u"Testsuiten",
"Trash"                         : u"Papierkorb",
'Import ...'                    : u"Import ...",
'Import artefacts from AF database'
                                : u'Importiere Artefakte aus AF Datenbank',
'Import from product file'      : u'Importiere aus Produkt-Datei',

"Table of Contents"             : u'Inhaltsverzeichnis',
"Product information"           : u'Produktinformation',
"Features"                      : u'Features',
"Detected problems"             : u'Erkannte Probleme',
"Features without requirements" : u'Features ohne Anforderungen',
"Requirements without testcases"
                                : u'Anforderungen ohne Testf�lle',
"Usecases not belonging to requirements"
                                : u'Anwendungsf�lle ohne Anforderungen',
"Testcases not belonging to requirements"
                                : u'Testf�lle ohne Anforderungen',
"Testcases not belonging to testsuites"
                                : u'Testf�lle ohne Testsuite',
"Empty testsuites"              : u'Leere Testsuiten',
"Related requirements"          : u'Zugeordnete Anforderungen',
"Attached testcases"            : u'Zugeh�rige Testf�lle',
"None"                          : u'Keine',
"Related testsuites"            : u'Zugeordnete Testsuiten',
"Included testcases"            : u'Zugeh�rige Testf�lle',
"Created from %s at %s"         : u'Erstellt aus %s am %s',

"Essential" : u"unabdingbar",
"Expected"  : u"erwartet",
"Desired"   : u"gew�nscht",
"Optional"  : u"optional",

"Submitted" : u"eingereicht",
"Approved"  : u"best�tigt",
"Completed" : u"abgeschlossen",

"Months"    : u"Monate",
"Weeks"     : u"Wochen",
"Days"      : u"Tage",
"Hours"     : u"Stunden",

"Low"       : u"niedrig",
"Medium"    : u"mittel",
"High"      : u"hoch",
    
"Functional"    : u"Funktional",
"Reliability"   : u"Zuverl�ssigkeit",
"Up-time"       : u"Verf�gbarkeit",
"Safety"        : u"Sicherheit",
"Security"      : u"Schutz",
"Performance"   : u"Performanz",
"Scalability"   : u"Skalierbarkeit",
"Maintainability": u"Wartbarkeit",

"Upgradability" : u"Upgrade-F�higkeit",
"Supportability": u"Support-F�higkeit",
"Operability"   : u"Bedienbarkeit",

"Business life-cycle"   : u"Gesch�fts-Lebenszyklus",
"System hardware"       : u"System Hardware",
"System software"       : u"System Software",
"API"                   : u"API",
"Data import/export"    : u"Datenimport/Export",
"Other"                 : u"Andere",

"Always"    : u"Immer",
"Often"     : u"Oft",
"Sometimes" : u"Manchmal",
"Rarely"    : u"Selten",
"Once"      : u"Einmal",

"Dangerous" : u"gef�hrlich",
"3-Risk"    : u"Risiko 3",
"2-Risk"    : u"Risiko 2",
"1-Risk"    : u"Risiko 1",
"Safe"      : u"sicher",

'created'   : u"erstellt",
"edited"    : u"bearbeitet",
"deleted"   : u"gel�scht",
"restored"  : u"wiederhergestellt",

"New test run"              : u"Neuer Testlauf",
"Create a new test run"     : u"Erstelle neuen Testlauf",
"Open test run"             : u"�ffne Testlauf",
"Open an existing test run" : u"�ffne einen vorhandenen Testlauf",
"Run"                       : u"Ausf�hren",
"Run test case"             : u"Testfall ausf�hren",
"Run a test case"           : u"Einen Testfall ausf�hren",
"&New test run ...\tCtrl-N"
                            : u"Neuer Testlauf ...\tCtrl-N",
"Create a new test run"     : u"Neuen Testlauf erstellen",
"&Open test run ...\tCtrl-O"
                            : u"Testlauf �ffnen ...\tCtrl-O",
"Open an existing test run" : u"Vorhandenen Testlauf �ffnen",
"Export test run to HTML file"
                            : u"Testlauf als HTML exportieren",
"Export test run to XML files"
                            : u"Testlauf als XML exportieren",
"Run ...\tCtrl-R"       : u"Ausf�hren ...\tCtrl-R",
"About current test run..." : u"�ber aktuellen Testlauf",
"Info about the current test run"
                            : u"Informationen �ber den aktuellen Testlauf",
"Cancel current test run..."
                            : u"Aktuellen Testlauf abbrechen",
"Cancel the current test run"
                            : u"Aktuellen Testlauf abbrechen",
"&Test"                     : u"Test",
"Test run status"           : u"Status Testlauf",
"%3d test cases total"      : u"%3d Testf�lle gesamt",
"%3d pending"               : u"%3d offen",
"%3d failed"                : u"%3d fehlgeschlagen",
"%3d skipped"               : u"%3d �bersprungen",
"Create new test run"               : u"Neuen Testlauf erstellen",
"Step 1/4: Select product database" : u"Schritt 1/4: Produkt-Datenbank w�hlen",
"Database file"                     : u"Datenbank-Datei",
"Open Database"                     : u"�ffne Datenbank",
"Browse"                            : u"Durchsuchen",
"Step 2/4: Select test suite"       : u"Schritt 2/4: Testsuite ausw�hlen",
"Test suite:"                       : u"Testsuite:",
"Step 3/4: Enter test description"  : u"Schritt 3/4: Beschreibung Testlauf",
"Tester name"                       : u"Tester",
"Step 4/4: Select test run output file"
                                    : u"Schritt 4/4: Ausgabedatei f�r Testlauf w�hlen",
"File"                              : u"Datei",
"Save test run"                     : u"Testlauf speichern",
"FAIL"                              : u"FEHLGESCHLAGEN",
"PASS"                              : u"BESTANDEN",
"SKIP"                              : u"�BERSPRUNGEN",
"PENDING"                           : u"OFFEN",
"Result"                            : u"Ergebnis",
"Time"                              : u"Zeit",
"Action"                            : u"Aktion",
"Remark"                            : u"Bemerkung",
"Test failed.\nEnter action!"       : u"Test fehlgeschlagen.\nAktion eingeben!",
"Test skipped.\nEnter remark!"      : u"Test �bersprungen.\nBemerkung eingeben!",
"Error"                             : u"Fehler",
"Creation date"             : u"Erstellungsdatum",
"Test run\ndescription"     : u"Beschreibung Testlauf",
"Tester"                    : u"Tester",
"AF Database"               : u"AF Datenbank",
"Test suite ID"             : u"Testsuite ID",
"Test suite title"          : u"Testsuite Titel",
"Test suite\ndescription"   : u"Testsuite Beschreibung",
"Test case order"           : u"Testfall-Abfolge",
"Test Run Info"             : u"Testlauf Information",
"Cancel Test Run"               : u"Testlauf abbrechen",
"Enter reason for cancelation"  : u"Grund f�r Abbruch angeben",
"Test Run Tool for the Artefact Management System"
                                : u"Werkzeug zur Testausf�hrung f�r das Artefakt Management System",
"AFMS Test Run Report"	 : u"AFMS Testlauf Bericht",
"Test run information"	 : u"Information zum Testlauf",
"Product title"	         : u"Produkttitel",
"Test suite description" : u"Testsuite Beschreibung",
"Number of test cases"	 : u"Anzahl Testf�lle",
"Pending test cases"	 : u"Offene Testf�lle",
"Failed test cases"	     : u"Fehlgeschlagene Testf�lle",
"Skipped test cases"	 : u"�bersprungene Testf�lle",
"Passed test cases"	     : u"Bestandene Testf�lle",
"Overall result"	     : u"Gesamtergebnis",
"Test data"	             : u"Testdaten",
"Test result"	         : u"Testergebnis",
"Time stamp"	         : u"Zeitstempel",
}

_RESOURCE = RESOURCE_DE
_language = 'en'

def SetLanguage(lang):
    global _language, _RESOURCE, ARTEFACTS, TRASH, PRIORITY_NAME , STATUS_NAME
    global EFFORT_NAME , COMPLEXITY_NAME , CATEGORY_NAME , USEFREQUENCY_NAME , RISK_NAME , CHANGETYPE_NAME
    global AF_WILDCARD, AF_WILDCARD_DE, HTML_WILDCARD, HTML_WILDCARD_DE, XML_WILDCARD, XML_WILDCARD_DE
    global TEST_STATUS_NAME

    _language = lang
    if lang == 'de':
        _RESOURCE = RESOURCE_DE
        ARTEFACTS = [{'name': _(item['name']), 'id': item['id']} for item in ARTEFACTS ]
        TRASH['name'] = _(TRASH['name'])
        PRIORITY_NAME = [_(item) for item in PRIORITY_NAME]
        STATUS_NAME = [_(item) for item in STATUS_NAME]
        EFFORT_NAME = [_(item) for item in EFFORT_NAME]
        COMPLEXITY_NAME = [_(item) for item in COMPLEXITY_NAME]
        CATEGORY_NAME = [_(item) for item in CATEGORY_NAME]
        USEFREQUENCY_NAME = [_(item) for item in USEFREQUENCY_NAME]
        RISK_NAME = [_(item) for item in RISK_NAME]
        CHANGETYPE_NAME = [_(item) for item in CHANGETYPE_NAME]
        TEST_STATUS_NAME  = [_(item) for item in TEST_STATUS_NAME]
        AF_WILDCARD = AF_WILDCARD_DE
        HTML_WILDCARD = HTML_WILDCARD_DE
        XML_WILDCARD = XML_WILDCARD_DE
    else:
        _RESOURCE = {}
        
def GetLanguage():
    return _language

def _(msg):
    try:
        return _RESOURCE[msg]
    except:
        logging.debug('afresource._(%s) missing' % msg)
        return msg


