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
        connection = sqlite3.connect(self.database_filename)
        self.cursor = connection.cursor()
        tablenodes = self.dom.getElementsByTagName('table')
        for tablenode in tablenodes:
            self._createTable(tablenode)
            
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
    #worker.write()
    
afarchivetodb('sample\sample_11.xml', 'sample\sample_11_from_xml.af')

