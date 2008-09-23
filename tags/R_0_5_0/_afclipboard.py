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

import pickle
import wx
import afresource

def copyArtefactToClipboard(dataobj, textobj):
    doc = wx.DataObjectComposite()
    doc.Add(dataobj)
    doc.Add(textobj)
    if wx.TheClipboard.Open():
        wx.TheClipboard.SetData(doc)
    wx.TheClipboard.Close()


def getArtefactFromClipboard():
    retval = None
    af_data = None
    af_kind = None
    if wx.TheClipboard.Open():
        if wx.TheClipboard.IsSupported(wx.CustomDataFormat('AFMS_FEATURE')):
            af_kind = 'AFMS_FEATURE'
            af_data = afFeatureDataObjectSimple()
        elif wx.TheClipboard.IsSupported(wx.CustomDataFormat('AFMS_REQUIREMENT')):
            af_kind = 'AFMS_REQUIREMENT'
            af_data = afRequirementDataObjectSimple()
        elif wx.TheClipboard.IsSupported(wx.CustomDataFormat('AFMS_USECASE')):
            af_kind = 'AFMS_USECASE'
            af_data = afUsecaseDataObjectSimple()
        elif wx.TheClipboard.IsSupported(wx.CustomDataFormat('AFMS_TESTCASE')):
            af_kind = 'AFMS_TESTCASE'
            af_data = afTestcaseDataObjectSimple()
        elif wx.TheClipboard.IsSupported(wx.CustomDataFormat('AFMS_TESTSUITE')):
            af_kind = 'AFMS_TESTSUITE'
            af_data = afTestsuiteDataObjectSimple()
        elif wx.TheClipboard.IsSupported(wx.CustomDataFormat('AFMS_SIMPLESECTION')):
            af_kind = 'AFMS_SIMPLESECTION'
            af_data = afSimpleSectionDataObjectSimple()
        elif wx.TheClipboard.IsSupported(wx.CustomDataFormat('AFMS_GLOSSARYENTRY')):
            af_kind = 'AFMS_GLOSSARYENTRY'
            af_data = afGlossaryEntryDataObjectSimple()

        if af_data is not None:
            if wx.TheClipboard.GetData(af_data):
                retval = pickle.loads(af_data.GetDataHere())

        wx.TheClipboard.Close();

    return (af_kind, retval)


class afArtefactDataObjectSimple(wx.PyDataObjectSimple):
    def __init__(self, artefact):
        assert 0==1 # has to be overriden!

    def GetDataHere(self):
        return self.data

    def GetDataSize(self):
        return len(self.data)

    def SetData(self, data):
        self.data = data
        return True


class afArtefactTextObjectSimple(wx.PyDataObjectSimple):
    def __init__(self, afkind, artefact):
        wx.PyDataObjectSimple.__init__(self, wx.DataFormat(wx.DF_TEXT))
        self.data = artefact
        self.afkind = afkind

    def GetDataHere(self):
        return self._formatData()

    def GetDataSize(self):
        return len(self._formatData())

    def _formatData(self):
        return self.data.getClipboardText()

    def SetData(self, data):
        self.data = data
        return True

# ---------------------------------------------------------------------

def copyFeatureToClipboard(feature):
    af_data = afFeatureDataObjectSimple(pickle.dumps(feature))
    af_text = afFeatureTextObjectSimple('AFMS_FEATURE', feature)
    copyArtefactToClipboard(af_data, af_text)


class afFeatureDataObjectSimple(afArtefactDataObjectSimple):
    def __init__(self, artefact = None):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('AFMS_FEATURE'))
        self.data = artefact


class afFeatureTextObjectSimple(afArtefactTextObjectSimple):
    pass

# ---------------------------------------------------------------------

def copyRequirementToClipboard(requirement):
    af_data = afRequirementDataObjectSimple(pickle.dumps(requirement))
    af_text = afRequirementTextObjectSimple('AFMS_REQUIREMENT', requirement)
    copyArtefactToClipboard(af_data, af_text)


class afRequirementDataObjectSimple(afArtefactDataObjectSimple):
    def __init__(self, artefact = None):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('AFMS_REQUIREMENT'))
        self.data = artefact


class afRequirementTextObjectSimple(afArtefactTextObjectSimple):
    pass

# ---------------------------------------------------------------------

def copyUsecaseToClipboard(usecase):
    af_data = afUsecaseDataObjectSimple(pickle.dumps(usecase))
    af_text = afUsecaseTextObjectSimple('AFMS_USECASE', usecase)
    copyArtefactToClipboard(af_data, af_text)


class afUsecaseDataObjectSimple(afArtefactDataObjectSimple):
    def __init__(self, artefact = None):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('AFMS_USECASE'))
        self.data = artefact


class afUsecaseTextObjectSimple(afArtefactTextObjectSimple):
    pass
# ---------------------------------------------------------------------

def copyTestcaseToClipboard(testcase):
    af_data = afTestcaseDataObjectSimple(pickle.dumps(testcase))
    af_text = afTestcaseTextObjectSimple('AFMS_TESTCASE', testcase)
    copyArtefactToClipboard(af_data, af_text)


class afTestcaseDataObjectSimple(afArtefactDataObjectSimple):
    def __init__(self, artefact = None):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('AFMS_TESTCASE'))
        self.data = artefact


class afTestcaseTextObjectSimple(afArtefactTextObjectSimple):
    pass

# ---------------------------------------------------------------------

def copyTestsuiteToClipboard(testsuite):
    af_data = afTestsuiteDataObjectSimple(pickle.dumps(testsuite))
    af_text = afTestsuiteTextObjectSimple('AFMS_TESTSUITE', testsuite)
    copyArtefactToClipboard(af_data, af_text)


class afTestsuiteDataObjectSimple(afArtefactDataObjectSimple):
    def __init__(self, artefact = None):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('AFMS_TESTSUITE'))
        self.data = artefact


class afTestsuiteTextObjectSimple(afArtefactTextObjectSimple):
    pass

# ---------------------------------------------------------------------

def copySimpleSectionToClipboard(simplesection):
    af_data = afSimpleSectionDataObjectSimple(pickle.dumps(simplesection))
    af_text = afSimpleSectionTextObjectSimple('AFMS_SIMPLESECTION', simplesection)
    copyArtefactToClipboard(af_data, af_text)


class afSimpleSectionDataObjectSimple(afArtefactDataObjectSimple):
    def __init__(self, artefact = None):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('AFMS_SIMPLESECTION'))
        self.data = artefact


class afSimpleSectionTextObjectSimple(afArtefactTextObjectSimple):
    pass

# ---------------------------------------------------------------------

def copyGlossaryEntryToClipboard(glossaryentry):
    af_data = afGlossaryEntryDataObjectSimple(pickle.dumps(glossaryentry))
    af_text = afGlossaryEntryTextObjectSimple('AFMS_GLOSSARYENTRY', glossaryentry)
    copyArtefactToClipboard(af_data, af_text)


class afGlossaryEntryDataObjectSimple(afArtefactDataObjectSimple):
    def __init__(self, artefact = None):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('AFMS_GLOSSARYENTRY'))
        self.data = artefact


class afGlossaryEntryTextObjectSimple(afArtefactTextObjectSimple):
    pass
