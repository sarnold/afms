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
Write AFMS database to xml archive file

@author: Achim Koehler
@version: $Rev$
"""

import sqlite3, os
import codecs
from xml.dom.minidom import getDOMImplementation


class AFDB2XML(object):
    def __init__(self, database_filename, xml_filename = None):
        self.xml_filename = xml_filename
        self.database_filename = database_filename
        if not os.path.exists(database_filename):
            raise IOError("file not found: %s" % database_filename)
        impl = getDOMImplementation()
        self.xmldoc = impl.createDocument(None, "afms_database", None)
        self.root = self.xmldoc.documentElement
        
    def run(self):
        connection = sqlite3.connect(self.database_filename)
        self.cursor = connection.cursor()
        # See http://www.sqlite.org/faq.html#q7 for details
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name not like 'sqlite%' ORDER BY name;")
        table_names = [table_name[0] for table_name in self.cursor.fetchall()]
        for table_name in table_names:
            self.cursor.execute("pragma table_info(%s)" % table_name)
            table_infos = self.cursor.fetchall()
            table = self._createTable(table_name, table_infos)
            self.root.appendChild(table)
            
    def write(self, xml_filename = None):
        if xml_filename is None:
            xml_filename = self.xml_filename
        f = codecs.open(xml_filename, encoding='UTF-8', mode="w", errors='strict')
        self.xmldoc.writexml(f, indent='', addindent=' '*2, newl='\n', encoding='UTF-8')
        f.close()
        
    def _createTable(self, table_name, table_infos):
        table = self.xmldoc.createElement('table')
        table.appendChild(self._createNode('name', table_name))
        columns = self.xmldoc.createElement('columns')
        for table_info in table_infos:
            columns.appendChild(self._createColumn(table_info))
        table.appendChild(columns)
        
        columnnames = [table_info[1] for table_info in table_infos]
        query = 'select ' + ','.join(columnnames) + ' from ' + table_name
        self.cursor.execute(query)
        rows = self.xmldoc.createElement('rows')
        for data in self.cursor:
            row = self.xmldoc.createElement('row')
            for columnname, value in zip(columnnames, data):
                if value is None: value = ''
                row.appendChild(self._createNode(columnname, unicode(value)))
            rows.appendChild(row)
        table.appendChild(rows)
        return table
        
    def _createColumn(self, table_info):
        column = self.xmldoc.createElement('column')
        table_info = list(table_info)
        if table_info[4] is None: table_info[4] = '' 
        for key, value in zip(['cid', 'name', 'type', 'notnull', 'default', 'primarykey'], table_info):
            column.appendChild(self._createNode(key, unicode(value)))
        return column
        
    def _createNode(self, nodename, nodetext):
        node = self.xmldoc.createElement(nodename)
        if len(nodetext) > 0:
            text = self.xmldoc.createTextNode(nodetext)
            node.appendChild(text)
        return node
        
        
def afdbtoarchive(database_filename, archive_filename):
    worker = AFDB2XML(database_filename, archive_filename)
    worker.run()
    worker.write()


if __name__=="__main__":
    import sys, getopt

    def version():
        print("Version unknown")

    def usage():
        print("Write AFMS database to XML archive file\n"
        "Usage:\n%s [-h|--help] [-V|--version] <ifile> [<ofile>]\n"
        "  -h, --help                      show help and exit\n"
        "  -V, --version                   show version and exit\n"
        "  <ifile>                         AFMS database file\n"
        "  <ofile>                         archive file (default <ifile>.xml)"
        % os.path.basename(sys.argv[0]))

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hV", ["help", "version"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-V", "--version"):
            version()
            sys.exit()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    if len(args) == 1:
        ifile = args[0]
        ofile =  os.path.splitext(ifile)[0] + ".xml"
    elif len(args) == 2:
        (ifile, ofile) = args[0:2]
    else:
        usage()
        sys.exit(1)
        
    afdbtoarchive(ifile, ofile)        
