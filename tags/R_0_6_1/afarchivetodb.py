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
Convert xml archive file to AFMS database

@author: Achim Koehler
@version: $Rev$
"""

import os.path
import sqlite3
from xml.dom.minidom import parse


class AFXML2DB(object):
    def __init__(self, xml_filename, database_filename = None):
        self.xml_filename = xml_filename
        self.database_filename = database_filename

    def run(self):
        self.dom = parse(self.xml_filename)
        if os.path.exists(self.database_filename):
            os.remove(self.database_filename)
        connection = sqlite3.connect(self.database_filename.encode('utf-8'))
        self.cursor = connection.cursor()
        tablenodes = self.dom.getElementsByTagName('table')
        for tablenode in tablenodes:
            self._createTable(tablenode)
        connection.commit()


    def _createTable(self, tablenode):
        tablename = tablenode.getElementsByTagName('name')[0].childNodes[0].data.strip()
        columnnodes = tablenode.getElementsByTagName('column')
        columnstrlist = []
        columnnames = []
        columntypes = []
        for columnnode in columnnodes:
            (columnstr, columnname, columntype) = self._getColumnStr(columnnode)
            columnstrlist.append(columnstr)
            columnnames.append(columnname)
            columntypes.append(columntype)
        sqlcmd = "create table %s (%s);" % (tablename, ','.join(columnstrlist))
        self.cursor.execute(sqlcmd)

        rows = tablenode.getElementsByTagName('row')
        for row in rows:
            items = []
            mask = []
            for columnname, columntype in zip(columnnames, columntypes):
                item = self._getSubnodeData(row, columnname)
                if item is None:
                    item = ''
                elif columntype == 'integer':
                    item = int(item)
                items.append(item)
                mask.append('?')
            sqlstr = "insert into %s values (%s)" % (tablename, ','.join(mask))
            self.cursor.execute(sqlstr, items)


    def _getColumnStr(self, columnnode):
        column = []
        columnname = self._getSubnodeData(columnnode, 'name')
        column.append(columnname)
        columntype = self._getSubnodeData(columnnode, 'type')
        column.append(columntype)
        if int(self._getSubnodeData(columnnode, 'notnull')) != 0:
            column.append('not null')
        default = self._getSubnodeData(columnnode, 'default')
        if (default) is not None:
            column.append('default %s' % unicode(default))
        if int(self._getSubnodeData(columnnode, 'primarykey')) != 0:
            column.append('primary key')
        return (' '.join(column), columnname, columntype)

    def _getSubnodeData(self, node, nodename):
        try:
            return node.getElementsByTagName(nodename)[0].childNodes[0].data.strip()
        except IndexError:
            return None


def afarchivetodb(archive_filename, database_filename):
    worker = AFXML2DB(archive_filename, database_filename)
    worker.run()


if __name__=="__main__":
    import sys, getopt

    def version():
        print("Version unknown")

    def usage():
        print("Convert XML archive file to AFMS database\n"
        "Usage:\n%s [-h|--help] [-V|--version] <ifile> [<ofile>]\n"
        "  -h, --help                      show help and exit\n"
        "  -V, --version                   show version and exit\n"
        "  <ifile>                         archive file\n"
        "  <ofile>                         AFMS database file (default <ifile>.af)"
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
        ofile =  os.path.splitext(ifile)[0] + ".af"
    elif len(args) == 2:
        (ifile, ofile) = args[0:2]
    else:
        usage()
        sys.exit(1)

    afarchivetodb(ifile, ofile)

