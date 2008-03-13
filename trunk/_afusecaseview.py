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

import wx
from _afhtmlwindow import *
from _afartefactlist import *
from _afvalidators import NotEmptyValidator
import _afbasenotebook
import afconfig
from afresource import _

# ID summary priority usefrequency actors stakeholders prerequisites mainscenario altscenario notes

class afUsecaseNotebook(_afbasenotebook.afBaseNotebook):
    def __init__(self, parent, id = -1, viewonly = True):
        _afbasenotebook.afBaseNotebook.__init__(self, parent, id, viewonly)
        color = parent.GetBackgroundColour()
        self.SetOwnBackgroundColour(color)
        panel1 = wx.Panel(self, -1)
        panel1.SetOwnBackgroundColour(color)

        labels1 = [_('Summary'), _('ID'), _('Priority'), _('Use frequency'), _('Stakeholders'), \
                    _('Actors'),  _('Prerequisites'), _('Main scenario'), _('Alt scenario'), _('Notes')]
        
        (width, height) = (0, 0)
        statictext = []
        for label in labels1:
            st = wx.StaticText(panel1, -1, label+':')
            (w, h) = st.GetSize()
            (width, height) =  (max(width, w), max(height, h))
            statictext.append(st)
            
        for st in statictext:
            st.SetMinSize((width,height))
        
        if viewonly:
            self.summary_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.id_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.priority_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.usefreq_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.actors_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.stakeholders_edit = wx.TextCtrl(panel1, -1, "", style = wx.TE_READONLY)
            self.prerequisite_edit = afHtmlWindow(panel1, -1)
            self.mainscenarion_edit = afHtmlWindow(panel1, -1)
            self.altscenario_edit = afHtmlWindow(panel1, -1)
            self.notes_edit = afHtmlWindow(panel1, -1)
            #(w, h) = self.prerequisite.GetSize()
            #self.prerequisite.SetMinSize((w, 3*h))
        else:
            self.summary_edit = wx.TextCtrl(panel1, -1, "", validator = NotEmptyValidator())
            self.id_edit = wx.TextCtrl(panel1, -1, "")
            self.priority_edit = wx.ComboBox(panel1, -1, choices = afresource.PRIORITY_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.usefreq_edit = wx.ComboBox(panel1, -1, choices = afresource.USEFREQUENCY_NAME, style=wx.CB_DROPDOWN | wx.CB_READONLY)
            self.actors_edit = wx.ComboBox(panel1, -1, choices = afresource.ACTOR_NAME, style=wx.CB_DROPDOWN)
            self.stakeholders_edit = wx.ComboBox(panel1, -1, choices = afresource.STAKEHOLDER_NAME, style=wx.CB_DROPDOWN)
            self.prerequisite_edit = wx.TextCtrl(panel1, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
            self.mainscenarion_edit = wx.TextCtrl(panel1, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
            self.altscenario_edit = wx.TextCtrl(panel1, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
            self.notes_edit = wx.TextCtrl(panel1, -1, "", style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)

            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.prerequisite_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.mainscenarion_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.altscenario_edit)
            self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.notes_edit)

        self.id_edit.Enable(False)
        edit = [self.summary_edit, self.id_edit, self.priority_edit, self.usefreq_edit, \
                self.stakeholders_edit, self.actors_edit, self.prerequisite_edit, self.mainscenarion_edit, self.altscenario_edit, self.notes_edit, ]

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        
        sizer = wx.FlexGridSizer(1, 2, 10, 10)
        sizer.Add(statictext[0], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(edit[0], 0, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)

        mainsizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)

        sizer = wx.FlexGridSizer(2, 4, 10, 10)
        for i in range(1,5):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
            sizer.Add(edit[i], 0, wx.EXPAND | wx.ALIGN_LEFT)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(3)
        sizer.SetFlexibleDirection(wx.HORIZONTAL)
        
        mainsizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        sizer = wx.FlexGridSizer(5, 2, 10, 10)
        for i in range(5,10):
            sizer.Add(statictext[i], 0, wx.EXPAND | wx.ALIGN_BOTTOM)
            sizer.Add(edit[i], 1, wx.EXPAND | wx.ALIGN_LEFT)

        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1, 1)
        sizer.AddGrowableRow(2, 2)
        sizer.AddGrowableRow(3, 2)
        sizer.AddGrowableRow(4, 1)
        sizer.SetFlexibleDirection(wx.BOTH)
        sizer.Layout()

        mainsizer.Add(sizer, 1, wx.ALL | wx.EXPAND, 10)
        
        panel1.SetSizer(mainsizer)
        panel1.Layout()
        self.AddPage(panel1, _("Usecase"))
        
        #-----------------------------------------------------------------

        # Related requirements panel; this relation could not be edited from here
        self.requirementlist = self.AddRelatedArtefactPanel(afRequirementList, _("Related Requirements"))
        
        #-----------------------------------------------------------------
        
        self.AddChangelogPanel()
        
        
    def InitContent(self, usecasedata):
        """
        requirementdata  is a tuple:
        ID summary priority usefrequency actors stakeholders prerequisites mainscenario altscenario notes
        """
        (basedata, related_requirements, changelist) = usecasedata
        self.summary_edit.SetValue(basedata[1])
        self.id_edit.SetValue(str(basedata[0]))
        self.priority_edit.SetValue(afresource.PRIORITY_NAME[basedata[2]])
        self.usefreq_edit.SetValue(afresource.USEFREQUENCY_NAME[basedata[3]])
        self.actors_edit.SetValue(basedata[4])
        self.stakeholders_edit.SetValue(basedata[5])
        self.prerequisite_edit.SetValue(basedata[6])
        self.mainscenarion_edit.SetValue(basedata[7])
        self.altscenario_edit.SetValue(basedata[8])
        self.notes_edit.SetValue(basedata[9])
        
        self.requirementlist.InitContent(related_requirements)
        
        if self.viewonly:
            self.changelist.InitContent(changelist)
        
        self.Show()
        self.GetParent().Layout()
        self.summary_edit.SetFocus()
        
        
    def GetContent(self):
        return ((int(self.id_edit.GetValue()),
            self.summary_edit.GetValue(),
            self.priority_edit.GetCurrentSelection(),
            self.usefreq_edit.GetCurrentSelection(),
            self.actors_edit.GetValue(),
            self.stakeholders_edit.GetValue(),
            self.prerequisite_edit.GetValue(),
            self.mainscenarion_edit.GetValue(),
            self.altscenario_edit.GetValue(),
            self.notes_edit.GetValue()), self.GetChangelogContent())

