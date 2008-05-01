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
Several filter view classes for each kind of artefacts.
"""

import wx
import  wx.lib.scrolledpanel as scrolled
import afresource
import _affilter


class afNoFilterView(scrolled.ScrolledPanel):
    def __init__(self, parent):
        self.btnId = None
        scrolled.ScrolledPanel.__init__(self, parent, id=-1, style=wx.SUNKEN_BORDER  )
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddStretchSpacer(1)
        vbox.Add(wx.StaticText(self, -1, _('No filter available')), 0, wx.ALIGN_CENTER )
        vbox.AddStretchSpacer(1)
        self.SetSizer(vbox)
        self.Layout()
        self.SetAutoLayout(True)
        self.SetupScrolling()

    def GetFilterContent(self):
        return _affilter.afNoFilter()


class afBaseFilterView(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.applied = False

    def AddButtons(self, btnId):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        labels = [_('Apply'), _('Reset'), _('Save'), _('Load')]
        for label in labels:
            btn = wx.Button(self, btnId, label)
            btnId += 1
            hbox.Add(btn)
        self.vbox.Add(hbox, 0, wx.ALL|wx.EXPAND, 5)


    def AddTextFieldWidget(self, hbox, choices, fieldnames):
        sizer = wx.BoxSizer(wx.VERTICAL)
        stext = wx.StaticText(self, -1, _('Text field')+':')
        size = stext.GetSize()
        size[0] = -1
        size[1] *= 6
        style = wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB
        lbox = wx.ListBox(self, choices=choices, size=size, style=style)
        sizer.Add(stext)
        sizer.Add(lbox, 1, wx.TOP | wx.EXPAND, 5)
        hbox.Add(sizer, 0, wx.ALL, 5)
        self.lbox_textfields = lbox
        self.fieldnames = fieldnames

        sizer = wx.BoxSizer(wx.VERTICAL)
        stext = wx.StaticText(self, -1, _('Condition')+':')
        combo = wx.ComboBox(self, -1, choices = [_(i) for i in afresource.TEXTFILTER], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        sizer.Add(stext)
        sizer.Add(combo, 0, wx.TOP | wx.EXPAND, 5)
        sizer.AddStretchSpacer(1)
        self.combo_textcondition = combo

        stext = wx.StaticText(self, -1, _('Word/String')+':')
        tfield = wx.TextCtrl(self, -1, "")
        sizer.Add(stext, 0, wx.TOP, 10)
        sizer.Add(tfield, 0, wx.TOP | wx.EXPAND | wx.ALIGN_TOP, 5)
        hbox.Add(sizer, 0, wx.ALL, 5)
        hbox.AddSpacer(20)
        self.tfield_textpattern = tfield

        self.lbox_size = size

    def AddListboxWidget(self, box, style, title, choices):
        sizer = wx.BoxSizer(wx.VERTICAL)
        stext = wx.StaticText(self, -1, title+':')
        lbox = wx.ListBox(self, choices=choices, size=self.lbox_size, style=style)
        sizer.Add(stext)
        sizer.Add(lbox, 1, wx.TOP | wx.EXPAND, 5)
        box.Add(sizer, 0, wx.ALL, 5)
        return lbox

    def AddPriorityWidget(self, box, style):
        self.lbox_priority = self.AddListboxWidget(box, style, _('Priority'), [_(i) for i in afresource.PRIORITY_NAME])

    def AddStatusWidget(self, box, style):
        self.lbox_status = self.AddListboxWidget(box, style, _('Status'), [_(i) for i in afresource.STATUS_NAME])

    def AddRiskWidget(self, box, style):
        self.lbox_risk = self.AddListboxWidget(box, style, _('Risk'), [_(i) for i in afresource.RISK_NAME])

    def AddVersionWidget(self, box, style):
        self.lbox_version  = self.AddListboxWidget(box, style, _('Version'), [])

    def AddChangeSearchWidget(self, box):
        stext = wx.StaticText(self, -1, _('Changed between'))
        self.changedate_from = wx.DatePickerCtrl(self, dt=wx.DateTimeFromDMY(1, 0, 2000), size=wx.DefaultSize, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        box.Add(stext, 0, wx.ALIGN_CENTER)
        box.Add(self.changedate_from, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        stext = wx.StaticText(self, -1, _('and'))
        self.changedate_to = wx.DatePickerCtrl(self, size=wx.DefaultSize, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        box.Add(stext, 0, wx.ALIGN_CENTER)
        box.Add(self.changedate_to, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)
        stext = wx.StaticText(self, -1, _('by'))
        self.combo_changedby = wx.ComboBox(self, -1, choices = [], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        box.Add(stext, 0, wx.ALIGN_CENTER)
        box.Add(self.combo_changedby, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)

    def ResetFilterClick(self, evt):
        self.tfield_textpattern.Clear()
        self.combo_textcondition.SetSelection(wx.NOT_FOUND)
        self.changedate_to.SetValue(wx.DateTime_Now())
        self.changedate_from.SetValue(wx.DateTimeFromDMY(1, 0, 2000))
        self.combo_changedby.SetSelection(0)

    def GetFilterContent(self, flt):
        flt.textfields = [self.fieldnames[i] for i in self.lbox_textfields.GetSelections()]
        flt.textcondition = self.combo_textcondition.GetSelection()
        flt.textpattern = self.tfield_textpattern.GetValue()

        todate = self.changedate_to.GetValue()
        todate.SetHour(23)
        todate.SetMinute(59)
        todate.SetSecond(59)
        flt.changedto = todate.Format(afresource.TIME_FORMAT)
        flt.changedfrom   = self.changedate_from.GetValue().Format(afresource.TIME_FORMAT)
        if self.combo_changedby.GetSelection() == 0:
            flt.changedby = ''
        else:
            flt.changedby = self.combo_changedby.GetValue()

        return flt


    def updateCombobox(self, combo, values):
        selectedvalue = combo.GetValue()
        combo.Clear()
        for value in values:
            combo.Append(value)
        # set selection to first item
        combo.SetSelection(0)
        # restore previous selection if any
        combo.SetValue(selectedvalue)


    def updateListbox(self, listbox, values):
        selections = listbox.GetSelections()
        selectedvalues = [listbox.GetString(i) for i in selections]
        listbox.Clear()
        for value in values:
            listbox.Append(value)
        # restore previous selection if any
        for value in selectedvalues:
            listbox.SetStringSelection(value)


    def InitFilterContent(self, ff):
        values = ff.changedbylist
        values.insert(0, _('anyone'))
        self.updateCombobox(self.combo_changedby, values)

#-------------------------------------------------------------------------------

class afFeatureFilterView(afBaseFilterView):
    def __init__(self, parent):
        super(afFeatureFilterView, self).__init__(parent)
        self.btnId = wx.NewId()
        self.AddButtons(self.btnId)
        self.Bind(wx.EVT_BUTTON, self.ApplyFilterClick, id=self.btnId+0)
        self.Bind(wx.EVT_BUTTON, self.ResetFilterClick, id=self.btnId+1)
        self.Bind(wx.EVT_BUTTON, self.SaveFilterClick, id=self.btnId+2)
        self.Bind(wx.EVT_BUTTON, self.LoadFilterClick, id=self.btnId+3)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 1)

        self.AddTextFieldWidget(hbox, [_("Title"), _("Description")], ['title', 'description'])

        style = wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB
        self.AddPriorityWidget(hbox, style)
        self.AddStatusWidget(hbox, style)
        self.AddRiskWidget(hbox, style)
        self.AddVersionWidget(hbox, style)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 0, wx.ALL|wx.EXPAND, 5)
        self.AddChangeSearchWidget(hbox)

        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.SetupScrolling()


    def ApplyFilterClick(self, evt):
        self.applied = True
        evt.SetClientData('FEATURES')
        evt.Skip()


    def ResetFilterClick(self, evt):
        self.applied = False
        super(afFeatureFilterView, self).ResetFilterClick(evt)
        for lbox in [self.lbox_textfields, self.lbox_priority, self.lbox_status, self.lbox_risk, self.lbox_version]:
            for i in range(lbox.GetCount()):
                lbox.Deselect(i)
        evt.SetClientData('FEATURES')
        evt.Skip()


    def SaveFilterClick(self, evt):
        print 'Save'


    def LoadFilterClick(self, evt):
        print 'Load'


    def InitFilterContent(self, ff):
        super(afFeatureFilterView, self).InitFilterContent(ff)
        self.updateListbox(self.lbox_version, ff.version)


    def GetFilterContent(self):
        ff = super(afFeatureFilterView, self).GetFilterContent(_affilter.afFeatureFilter())
        ff.priority = self.lbox_priority.GetSelections()
        ff.status = self.lbox_status.GetSelections()
        ff.risk = self.lbox_risk.GetSelections()
        ff.version =[self.lbox_version.GetString(i) for i in self.lbox_version.GetSelections()]
        ff.applied = self.applied
        return ff

#-------------------------------------------------------------------------------

class afRequirementFilterView(afBaseFilterView):
    def __init__(self, parent):
        super(afRequirementFilterView, self).__init__(parent)
        self.btnId = wx.NewId()
        self.AddButtons(self.btnId)
        self.Bind(wx.EVT_BUTTON, self.ApplyFilterClick, id=self.btnId+0)
        self.Bind(wx.EVT_BUTTON, self.ResetFilterClick, id=self.btnId+1)
        self.Bind(wx.EVT_BUTTON, self.SaveFilterClick, id=self.btnId+2)
        self.Bind(wx.EVT_BUTTON, self.LoadFilterClick, id=self.btnId+3)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 1)

        self.AddTextFieldWidget(hbox, [_("Title"), _("Description"), _("Origin"), _("Rationale")],
            ['title', 'description', 'origin', 'rationale'])

        style = wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB
        self.AddPriorityWidget(hbox, style)
        self.AddStatusWidget(hbox, style)
        self.AddVersionWidget(hbox, style)

        self.lbox_complexity = self.AddListboxWidget(hbox, style, _('Complexity'), [_(i) for i in afresource.COMPLEXITY_NAME])
        self.lbox_category = self.AddListboxWidget(hbox, style, _('Category'), [_(i) for i in afresource.CATEGORY_NAME])
        self.lbox_effort = self.AddListboxWidget(hbox, style, _('Effort'), [_(i) for i in afresource.EFFORT_NAME])
        self.lbox_assigned = self.AddListboxWidget(hbox, style, _('Assigned'), [])

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 0, wx.ALL|wx.EXPAND, 5)
        self.AddChangeSearchWidget(hbox)

        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.SetupScrolling()


    def ApplyFilterClick(self, evt):
        self.applied = True
        evt.SetClientData('REQUIREMENTS')
        evt.Skip()


    def ResetFilterClick(self, evt):
        self.applied = False
        super(afRequirementFilterView, self).ResetFilterClick(evt)
        for lbox in [self.lbox_textfields, self.lbox_priority, self.lbox_status, self.lbox_effort, self.lbox_version,
                     self.lbox_assigned, self.lbox_category, self.lbox_complexity]:
            for i in range(lbox.GetCount()):
                lbox.Deselect(i)
        evt.SetClientData('REQUIREMENTS')
        evt.Skip()


    def SaveFilterClick(self, evt):
        print 'Save'


    def LoadFilterClick(self, evt):
        print 'Load'


    def InitFilterContent(self, ff):
        super(afRequirementFilterView, self).InitFilterContent(ff)
        self.updateListbox(self.lbox_assigned, ff.assigned)
        self.updateListbox(self.lbox_version, ff.version)


    def GetFilterContent(self):
        ff = super(afRequirementFilterView, self).GetFilterContent(_affilter.afRequirementFilter())
        ff.priority = self.lbox_priority.GetSelections()
        ff.status = self.lbox_status.GetSelections()
        ff.complexity = self.lbox_complexity.GetSelections()
        ff. category = self.lbox_category.GetSelections()
        ff.effort = self.lbox_effort.GetSelections()
        ff.version =[self.lbox_version.GetString(i) for i in self.lbox_version.GetSelections()]
        ff.assigned = [self.lbox_assigned.GetString(i) for i in self.lbox_assigned.GetSelections()]
        ff.applied = self.applied
        return ff

#-------------------------------------------------------------------------------

class afUsecaseFilterView(afBaseFilterView):
    def __init__(self, parent):
        super(afUsecaseFilterView, self).__init__(parent)
        self.btnId = wx.NewId()
        self.AddButtons(self.btnId)
        self.Bind(wx.EVT_BUTTON, self.ApplyFilterClick, id=self.btnId+0)
        self.Bind(wx.EVT_BUTTON, self.ResetFilterClick, id=self.btnId+1)
        self.Bind(wx.EVT_BUTTON, self.SaveFilterClick, id=self.btnId+2)
        self.Bind(wx.EVT_BUTTON, self.LoadFilterClick, id=self.btnId+3)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 1)

        self.AddTextFieldWidget(hbox, [_("Summary"), _("Prerequisites"), _("Main scenario"), _("Alt scenario"), _("Notes")],
            ['title', 'prerequisites', 'mainscenario', 'altscenario', 'notes'])

        style = wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB
        self.AddPriorityWidget(hbox, style)

        self.lbox_usefrequency = self.AddListboxWidget(hbox, style, _('Use frequency'), [_(i) for i in afresource.USEFREQUENCY_NAME])
        self.lbox_stakeholders = self.AddListboxWidget(hbox, style, _('Stakeholders'), [])
        self.lbox_actors = self.AddListboxWidget(hbox, style, _('Actors'), [])

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 0, wx.ALL|wx.EXPAND, 5)
        self.AddChangeSearchWidget(hbox)

        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.SetupScrolling()


    def ApplyFilterClick(self, evt):
        self.applied = True
        evt.SetClientData('USECASES')
        evt.Skip()


    def ResetFilterClick(self, evt):
        self.applied = False
        super(afUsecaseFilterView, self).ResetFilterClick(evt)
        for lbox in [self.lbox_textfields, self.lbox_priority, self.lbox_usefrequency,
                     self.lbox_stakeholders, self.lbox_actors]:
            for i in range(lbox.GetCount()):
                lbox.Deselect(i)
        evt.SetClientData('USECASES')
        evt.Skip()


    def SaveFilterClick(self, evt):
        print 'Save'


    def LoadFilterClick(self, evt):
        print 'Load'


    def InitFilterContent(self, ff):
        super(afUsecaseFilterView, self).InitFilterContent(ff)
        self.updateListbox(self.lbox_stakeholders, ff.stakeholders)
        self.updateListbox(self.lbox_actors, ff.actors)


    def GetFilterContent(self):
        ff = super(afUsecaseFilterView, self).GetFilterContent(_affilter.afUsecaseFilter())
        ff.priority = self.lbox_priority.GetSelections()
        ff.usefrequency = self.lbox_usefrequency.GetSelections()
        ff.actors =[self.lbox_actors.GetString(i) for i in self.lbox_actors.GetSelections()]
        ff.stakeholders = [self.lbox_stakeholders.GetString(i) for i in self.lbox_stakeholders.GetSelections()]
        ff.applied = self.applied
        return ff

#-------------------------------------------------------------------------------

class afTestcaseFilterView(afBaseFilterView):
    def __init__(self, parent):
        super(afTestcaseFilterView, self).__init__(parent)
        self.btnId = wx.NewId()
        self.AddButtons(self.btnId)
        self.Bind(wx.EVT_BUTTON, self.ApplyFilterClick, id=self.btnId+0)
        self.Bind(wx.EVT_BUTTON, self.ResetFilterClick, id=self.btnId+1)
        self.Bind(wx.EVT_BUTTON, self.SaveFilterClick, id=self.btnId+2)
        self.Bind(wx.EVT_BUTTON, self.LoadFilterClick, id=self.btnId+3)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 1)

        self.AddTextFieldWidget(hbox, [_("Title"), _("Purpose"), _("Prerequisite"), _("Testdata"), _("Steps"), _("Notes & Questions")],
            ['title', 'purpose', 'prerequisite', 'testdata', 'steps', 'notes'])

        style = wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB
        self.AddVersionWidget(hbox, style)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 0, wx.ALL|wx.EXPAND, 5)
        self.AddChangeSearchWidget(hbox)

        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.SetupScrolling()


    def ApplyFilterClick(self, evt):
        self.applied = True
        evt.SetClientData('TESTCASES')
        evt.Skip()


    def ResetFilterClick(self, evt):
        self.applied = False
        super(afTestcaseFilterView, self).ResetFilterClick(evt)
        for lbox in [self.lbox_textfields, self.lbox_version]:
            for i in range(lbox.GetCount()):
                lbox.Deselect(i)
        evt.SetClientData('TESTCASES')
        evt.Skip()


    def SaveFilterClick(self, evt):
        print 'Save'


    def LoadFilterClick(self, evt):
        print 'Load'


    def InitFilterContent(self, ff):
        super(afTestcaseFilterView, self).InitFilterContent(ff)
        self.updateListbox(self.lbox_version, ff.version)


    def GetFilterContent(self):
        ff = super(afTestcaseFilterView, self).GetFilterContent(_affilter.afTestcaseFilter())
        ff.version =[self.lbox_version.GetString(i) for i in self.lbox_version.GetSelections()]
        ff.applied = self.applied
        return ff

#-------------------------------------------------------------------------------

class afTestsuiteFilterView(afBaseFilterView):
    def __init__(self, parent):
        super(afTestsuiteFilterView, self).__init__(parent)
        self.btnId = wx.NewId()
        self.AddButtons(self.btnId)
        self.Bind(wx.EVT_BUTTON, self.ApplyFilterClick, id=self.btnId+0)
        self.Bind(wx.EVT_BUTTON, self.ResetFilterClick, id=self.btnId+1)
        self.Bind(wx.EVT_BUTTON, self.SaveFilterClick, id=self.btnId+2)
        self.Bind(wx.EVT_BUTTON, self.LoadFilterClick, id=self.btnId+3)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(hbox, 1)

        self.AddTextFieldWidget(hbox, [_("Title"), _("Description")], ['title', 'description'])

        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.SetupScrolling()


    def ApplyFilterClick(self, evt):
        self.applied = True
        evt.SetClientData('TESTSUITES')
        evt.Skip()


    def ResetFilterClick(self, evt):
        self.applied = False
        for lbox in [self.lbox_textfields]:
            for i in range(lbox.GetCount()):
                lbox.Deselect(i)
        evt.SetClientData('TESTSUITES')
        evt.Skip()


    def SaveFilterClick(self, evt):
        print 'Save'


    def LoadFilterClick(self, evt):
        print 'Load'


    def InitFilterContent(self, ff):
        pass


    def GetFilterContent(self):
        ff = _affilter.afTestsuiteFilter()
        ff.textfields = [self.fieldnames[i] for i in self.lbox_textfields.GetSelections()]
        ff.textcondition = self.combo_textcondition.GetSelection()
        ff.textpattern = self.tfield_textpattern.GetValue()
        ff.applied = self.applied
        return ff
