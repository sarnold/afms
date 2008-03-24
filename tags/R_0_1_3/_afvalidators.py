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

import wx
from afresource import _

class NotEmptyValidator(wx.PyValidator):
     """ This validator is used to ensure that the user has entered something
         into the text object editor dialog's text field.
     """
     def __init__(self, msg=_("Empty field not allowed") + "!"):
         """ Standard constructor.
         """
         wx.PyValidator.__init__(self)
         self.msg = msg


     def Clone(self):
         """ Standard cloner.

             Note that every validator must implement the Clone() method.
         """
         return NotEmptyValidator(self.msg)


     def Validate(self, win):
         """ Validate the contents of the given text control.
         """
         textCtrl = self.GetWindow()
         text = textCtrl.GetValue()

         if len(text) == 0:
             textCtrl.SetBackgroundColour("pink")
             textCtrl.Refresh()
             wx.MessageBox(self.msg, _("Error"), wx.ICON_ERROR)
             textCtrl.SetFocus()
             
             return False
         else:
             textCtrl.SetBackgroundColour(
                 wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
             textCtrl.Refresh()
             return True


     def TransferToWindow(self):
         """ Transfer data from validator to window.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
         return True # Prevent wxDialog from complaining.


     def TransferFromWindow(self):
         """ Transfer data from window to validator.

             The default implementation returns False, indicating that an error
             occurred.  We simply return True, as we don't do any data transfer.
         """
         return True # Prevent wxDialog from complaining.

#----------------------------------------------------------------------

class ArtefactHookValidator(wx.PyValidator):
     """ This validator uses a hook function to validate data of a artefact.
     """
     def __init__(self, hook):
         """ Standard constructor."""
         wx.PyValidator.__init__(self)
         self.hook = hook


     def Clone(self):
         """ Standard cloner."""
         return ArtefactHookValidator(self.hook)


     def Validate(self, win):
         """ Validate the contents of the given text control.
         """
         return self.hook()


     def TransferToWindow(self):
         """ Transfer data from validator to window."""
         return True # Prevent wxDialog from complaining.


     def TransferFromWindow(self):
         """ Transfer data from window to validator."""
         return True # Prevent wxDialog from complaining.
