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

import os, os.path
if __name__=="__main__":
    import sys, gettext
    basepath = os.path.abspath(os.path.dirname(sys.argv[0]))
    LOCALEDIR = os.path.join(basepath, 'locale')
    DOMAIN = "afms"
    gettext.install(DOMAIN, LOCALEDIR, unicode=True)

import wx
import afresource, afconfig       

def getRelFolder(reffolder, folder):
    commonprefix = os.path.commonprefix([reffolder, folder])
    if commonprefix != '':
        folder = folder[len(commonprefix):]
        reffolder = reffolder[len(commonprefix):]
        n = len(reffolder.split(os.sep))
        relfolder = os.sep.join(['..'] * n)
        folder =  os.path.join(relfolder, folder)
        if folder.startswith(os.sep):
            folder = folder.lstrip(os.sep)
    return folder

    
class afTextCtrl(wx.TextCtrl):
    (MODE_PLAIN, MODE_HTML, MODE_REST) = (0, 1, 2)
    REST_TAG = '.. REST\n\n'
    HTML_TAG = '.. HTML\n\n'
    
    def __init__(self, parent, ID=-1):
        style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB|wx.TE_RICH2
        wx.TextCtrl.__init__(self, parent, ID, style=style)
        font = self.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE )
        self.SetFont(font)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self._InitPopupMenu()


    def _InitPopupMenu(self):
        class menuitem: 
            def __init__(self, text, handler, enabler, kind=wx.ITEM_NORMAL, help=''):
                (self.text, self.handler, self.enabler, self.kind, self.help) = \
                    (text, handler, enabler, kind, help)
                self.id = wx.NewId()
                
        self.menuitems = (
            menuitem(text=_('Undo'), handler=self.handleUndo, enabler=self.CanUndo),
            menuitem(text=_('Redo'), handler=self.handleRedo, enabler=self.CanRedo),
            None,
            menuitem(text=_('Cut'), handler=self.handleCut, enabler=self.CanCut),
            menuitem(text=_('Copy'), handler=self.handleCopy, enabler=self.CanCopy),
            menuitem(text=_('Paste'), handler=self.handlePaste, enabler=self.CanPaste),
            menuitem(text=_('Delete'), handler=self.handleDelete, enabler=self.CanCut),
            None,
            menuitem(text=_('Select All'), handler=self.handleSelectAll, enabler=self.true),
            None,
            menuitem(text=_('Bold'), handler=self.handleBold, enabler=self._CanFormat),
            menuitem(text=_('Italic'), handler=self.handleItalic, enabler=self._CanFormat),
            menuitem(text=_('Fixed Width'), handler=self.handleFixedWidth, enabler=self._CanFormat),
            menuitem(text=_('Bullet List'), handler=self.handleBulletList, enabler=self._CanFormat),
            menuitem(text=_('Numbered List'), handler=self.handleNumberedList, enabler=self._CanFormat),
            menuitem(text=_('Table'), handler=self.handleTable, enabler=self._CanFormat),
            menuitem(text=_('Indent'), handler=self.handleIndent, enabler=self.CanCut),
            menuitem(text=_('Unindent'), handler=self.handleUnindent, enabler=self.CanCut),
            menuitem(text=_('Insert Image')+'...', handler = self.handleInsertImage, enabler=self._CanInsertImage),
            None,
            menuitem(text=_('Plain Text'), handler=self.handlePlainText, enabler=self.true, kind=wx.ITEM_RADIO),
            menuitem(text=_('HTML'), handler=self.handleHTML, enabler=self.true, kind=wx.ITEM_RADIO),
            menuitem(text=_('ReStructured Text'), handler=self.handleREST, enabler=self.true, kind=wx.ITEM_RADIO))
        self.mode = afTextCtrl.MODE_PLAIN
        
        self.menu = wx.Menu()
        for menuitem in self.menuitems: 
            if menuitem is None:
                self.menu.AppendSeparator()
            else:
                self._AppendMenuItem(menuitem)
                    
            
    def _AppendMenuItem(self, menuitem):
        self.menu.Append(menuitem.id, _(menuitem.text), _(menuitem.help), menuitem.kind)
        self.Bind(wx.EVT_MENU, menuitem.handler, id=menuitem.id)
        
        
    def SetValue(self, value):
        start = self.GetInsertionPoint()
        wx.TextCtrl.SetValue(self, value)
        end = self.GetLastPosition()
        style = self.GetDefaultStyle()
        font = style.GetFont()
        font.SetFamily(wx.FONTFAMILY_TELETYPE )
        style.SetFont(font)
        self.SetStyle(start, end, style)
        if self._isMarkupTag(value, afTextCtrl.HTML_TAG):
            self.mode = afTextCtrl.MODE_HTML
        elif self._isMarkupTag(value, afTextCtrl.REST_TAG):
            self.mode = afTextCtrl.MODE_REST
        else:
            self.mode = afTextCtrl.MODE_PLAIN
            

    def OnContextMenu(self, event):
        text = self.GetValue()
        if self._isMarkupTag(text, afTextCtrl.REST_TAG):
            self.mode = afTextCtrl.MODE_REST
            index = -1
        elif self._isMarkupTag(text, afTextCtrl.HTML_TAG):
            self.mode = afTextCtrl.MODE_HTML
            index = -2
        else:
            self.mode = afTextCtrl.MODE_PLAIN
            index = -3
            
        for menuitem in filter(lambda item: item is not None, self.menuitems):
            self.menu.Enable(menuitem.id, menuitem.enabler()) 
        self.menu.Check(self.menuitems[index].id, True)
        self.PopupMenu(self.menu)
        
        
    def true(self): 
        return True
        
        
    def _CanFormat(self):
        '''Return true if we can perform text formating commands'''
        return self.CanCut() and (self.mode != afTextCtrl.MODE_PLAIN)
        
    
    def _CanInsertImage(self):
        if self.mode == afTextCtrl.MODE_HTML:
            return self.IsEditable()
        if self.mode == afTextCtrl.MODE_PLAIN:
            return False
        (col, lineno) = self.PositionToXY(self.GetInsertionPoint())
        return self.IsEditable() and (col == 0) and len(self.GetLineText(lineno).strip()) == 0
        
        
    def handleUndo(self, evt): 
        self.Undo()
        
        
    def handleRedo(self, evt):
        self.Redo()
        
        
    def handleCut(self, evt):
        self.Cut()


    def handleCopy(self, evt):
        self.Copy()


    def handlePaste(self, evt):
        self.Paste()


    def handleDelete(self, evt):
        (start, to) = self.GetSelection()
        self.Remove(start, to)


    def handleSelectAll(self, evt):
        self.SetSelection(-1, -1)


    def handleBold(self, evt):
        if self.mode == afTextCtrl.MODE_HTML:
            self._insertTags('<b>', '</b>')
        else:
            self._insertTags('**', '**')
            
        
    def handleItalic(self, evt):
        if self.mode == afTextCtrl.MODE_HTML:
            self._insertTags('<i>', '</i>')
        else:
            self._insertTags('*', '*')


    def handleFixedWidth(self, evt):
        if self.mode == afTextCtrl.MODE_HTML:
            self._insertTags('<tt>', '</tt>')
        else:
            self._insertTags('``', '``')
            

    def _handleList(self, listtags, itemtags):
        '''Format selected text as list using listtags and itemtags'''
        (start, to) = self.GetSelection()
        lines = self.GetStringSelection().splitlines()
        lines[0] = lines[0].lstrip()
        
        if self.mode == afTextCtrl.MODE_HTML:
            tags = itemtags[0]
            lines = [listtags[0][0]] + lines + [listtags[0][1]]
        else:
            tags = itemtags[1]
            lines = [listtags[1][0]] + lines + [listtags[1][1]]
 
        # Handle list items spanning several lines; lines belonging to the same list item
        # starts with whitespace
        # If an item in lines list starts with whitespace, we append it to the previous
        # item and delete the currect item from lines
        i = 2
        while i < len(lines):
            if lines[i].startswith((' ','\t')):
                lines[i-1] += '\n' + ' '*len(tags[0]) +lines[i].lstrip()
                del lines[i]
            else:
                lines[i-1] = self._formatListItem(lines[i-1], tags)
                i += 1
            
        self.Replace(start, to, '\n'.join(lines))
            

    def handleBulletList(self, evt):
        self._handleList((('<ul>', '</ul>\n'), ('', '\n')), (('<li>','</li>'), ('* ', '')))


    def handleNumberedList(self, evt):
        self._handleList((('<ol>', '</ol>\n'), ('', '\n')), (('<li>','</li>'), ('#. ', '')))
        
    
    def handleInsertImage(self, evt):
        dlg = wx.FileDialog(
            self, message = _("Choose image file"),
            defaultDir = afconfig.basedir,
            defaultFile = "",
            wildcard = afresource.IMG_WILDCARD,
            style=wx.OPEN | wx.FILE_MUST_EXIST
            )
        dlgResult = dlg.ShowModal()
        path = dlg.GetPath()
        dlg.Destroy()
        if  dlgResult != wx.ID_OK: return
            
        # try to compute relative path
        reffolder = afconfig.basedir
        folder = os.path.dirname(path)
        path = os.path.join(getRelFolder(reffolder, folder), os.path.basename(path))
        
        if self.mode == afTextCtrl.MODE_HTML:
            self.WriteText('<p><img src="%s" /></p>' % path)
            return
            
        (col, lineno) = self.PositionToXY(self.GetInsertionPoint())
        (previousline, nextline) = ('', '')
        if lineno > 0:
            previousline = self.GetLineText(lineno-1).strip()
        if lineno < self.GetNumberOfLines() - 1:
            nextline = self.GetLineText(lineno+1).strip()
        
        inserttext = ''
        if len(previousline) != 0:
            inserttext += '\n'
        inserttext += '.. image:: %s' % path
        if len(nextline) != 0:
            inserttext += '\n'
        self.WriteText(inserttext)
        
        
    def handleHTML(self, evt):
        self._handleMarkup(afTextCtrl.HTML_TAG)
        
        
    def handleREST(self, evt):
        self._handleMarkup(afTextCtrl.REST_TAG)


    def handlePlainText(self, evt):
        self._handleMarkup('')
        
    
    def _handleMarkup(self, tag):
        text = self.GetValue()
        text = self._removeMarkupTag(text, afTextCtrl.REST_TAG)
        text = self._removeMarkupTag(text, afTextCtrl.HTML_TAG)
        self.SetValue(tag+text)
        self.SetInsertionPoint(self.GetLastPosition())
        
    
    def _isMarkupTag(self, text, tag):
        return text.lstrip().upper().startswith(tag)

        
    def _removeMarkupTag(self, text, tag):
        if self._isMarkupTag(text, tag): 
            return text.lstrip()[len(tag):]
        else:
            return text
       
       
    def _insertTags(self, starttag, stoptag):
        (start, to) = self.GetSelection()
        to += len(starttag)
        self.SetInsertionPoint(start)
        self.WriteText(starttag)
        self.SetInsertionPoint(to)
        self.WriteText(stoptag)
        self.SetInsertionPoint(to+len(stoptag))
        
        
    def _formatListItem(self, line, tags):
        return tags[0] + line + tags[1]
    
    
    def handleTable(self, evt):
        '''Format a table'''
        (start, to) = self.GetSelection()
        text = self.GetStringSelection()
        self.Replace(start, to, formatTable(text, self.mode))
        
        
    def handleIndent(self, evt):
        (start, to) = self.GetSelection()
        lines = self.GetStringSelection().splitlines()
        lines = [' '*4+line for line in lines]
        self.Replace(start, to, '\n'.join(lines))
        

    def handleUnindent(self, evt):
        def doUnident(s):
            if s.startswith(4*' '): 
                return s[4:]
            else:
                return s
            
        (start, to) = self.GetSelection()
        lines = self.GetStringSelection().splitlines()
        lines = map(doUnident, lines)
        self.Replace(start, to, '\n'.join(lines))


def formatTable(text, mode=afTextCtrl.MODE_REST):
    numtabs = text.count('\t')
    for i in range(numtabs, 1, -1):
        text = text.replace('\t'*i, '\t')
    lines = text.splitlines()
    tabsperline = lines[0].count('\t')
    colsize = [0]*(tabsperline+1)
    for i in range(len(lines)):
        if lines[i].count('\t') != tabsperline: return text
        lines[i] = lines[i].split('\t')
        currentcolsize = map(len, lines[i])
        colsize = [max(cs, ccs) for cs, ccs in zip(colsize,  currentcolsize)]
        
    if mode == afTextCtrl.MODE_HTML:
        text = '<table border="1">\n'
        for line in lines:
            text += '<tr>\n'
            text +=  '\n'.join(['  <td> ' + item + ' </td>' for item in line])
            text += '\n</tr>\n'
        text += '</table>\n'
    else:
        text = ''
        sepline = ['-'*cs for cs in colsize]
        sepline = '+-' + '-+-'.join(sepline) + '-+\n'
        for line in lines:
            text += sepline
            text += '| ' + ' | '.join([item.ljust(cs) for item, cs in zip(line, colsize)]) + ' |\n'
        text += sepline
        
    return text
        
        
if __name__ == "__main__":
    import unittest

    class TestRelFolder(unittest.TestCase):
        def setUp(self):
            pass
            
        def tofolder(self, f):
            return f.replace('/', os.sep)
            
        def test1(self):
            reffolder = self.tofolder('/a/b/c')
            folder = self.tofolder('/a/b/d')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, self.tofolder('../d'))

        def test2(self):
            reffolder = self.tofolder('/a/b/c')
            folder = self.tofolder('/a/b/c/d')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, self.tofolder('d'))

        def test3(self):
            reffolder = self.tofolder('c:\\a\\b\\c')
            folder = self.tofolder('d:\\a\\b\\c')
            relfolder = getRelFolder(reffolder, folder)
            self.assertEqual(relfolder, folder)

    class TestFormatTable(unittest.TestCase):
        inputs = ['1\t123\t12\n1\t2\t3', 
                  '1\t\t2\t\t3\n11111\t2222\t3\n1\t\t2\t\t3',
                  '\n',
                  '\n\n',
                  '1\t11111111\n2\t22222\n']
        
        restresults = ['''\
+---+-----+----+
| 1 | 123 | 12 |
+---+-----+----+
| 1 | 2   | 3  |
+---+-----+----+
''', '''\
+-------+------+---+
| 1     | 2    | 3 |
+-------+------+---+
| 11111 | 2222 | 3 |
+-------+------+---+
| 1     | 2    | 3 |
+-------+------+---+
''', '''\
+--+
|  |
+--+
''', '''\
+--+
|  |
+--+
|  |
+--+
''','''\
+---+----------+
| 1 | 11111111 |
+---+----------+
| 2 | 22222    |
+---+----------+
''']
        htmlresults = ['''\
<table border="1">
<tr>
  <td> 1 </td>
  <td> 123 </td>
  <td> 12 </td>
</tr>
<tr>
  <td> 1 </td>
  <td> 2 </td>
  <td> 3 </td>
</tr>
</table>
''', '''\
<table border="1">
<tr>
  <td> 1 </td>
  <td> 2 </td>
  <td> 3 </td>
</tr>
<tr>
  <td> 11111 </td>
  <td> 2222 </td>
  <td> 3 </td>
</tr>
<tr>
  <td> 1 </td>
  <td> 2 </td>
  <td> 3 </td>
</tr>
</table>
''', '''\
<table border="1">
<tr>
  <td>  </td>
</tr>
</table>
''', '''\
<table border="1">
<tr>
  <td>  </td>
</tr>
<tr>
  <td>  </td>
</tr>
</table>
''','''\
<table border="1">
<tr>
  <td> 1 </td>
  <td> 11111111 </td>
</tr>
<tr>
  <td> 2 </td>
  <td> 22222 </td>
</tr>
</table>
''']
        
        def testorderRest(self):
            for input, result in zip(TestFormatTable.inputs, TestFormatTable.restresults):
                self.assertEqual(formatTable(input), result)
 
        def testHTML(self):
            for input, result in zip(TestFormatTable.inputs, TestFormatTable.htmlresults):
                self.assertEqual(formatTable(input, afTextCtrl.MODE_HTML), result)

    unittest.main()
        
