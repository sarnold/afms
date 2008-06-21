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

import sys

from wx.tools import img2py


command_lines = [
    "-a -u -n TCNew tc_new.png icons.py",
    "-a -u -n FNew f_new.png icons.py",
    "-a -u -n TSNew ts_new.png icons.py",
    "-a -u -n RQNew rq_new.png icons.py",
    "-a -u -n UCNew uc_new.png icons.py",
    "-a -u -n ProdNew 24-tab-add.png icons.py",
    "-a -u -n ProdOpen 24-tab-open.png icons.py",
    "-a -u -n AFDelete 24-tag-remove.png icons.py",
    "-a -u -n TrashEmpty user-trash.png icons.py",
    "-a -u -n TrashFull user-trash-full.png icons.py",
    "-a -u -n app32x32 applications-system_32x32.png icons.py",
    "-a -u -n app16x16 applications-system_16x16.png icons.py",
    "-a -u -n TRFail 16-message-warn.png icons.py",
    "-a -u -n TRPass 16-circle-green-check.png icons.py",
    "-a -u -n TRPend 16-circle-blue.png icons.py",
    "-a -u -n TRSkip 16-circle-blue-delete.png icons.py",
    "-a -u -n TRRun 24-arrow-next.png icons.py",
    "-a -u -n AFCopy 24-tag-manager.png icons.py",
    "-a -u -n AFDelete 24-tag-remove.png icons.py",
    "-a -u -n AFPaste 24-tag-add.png icons.py",
    "-a -u -n AFEdit 24-tag-pencil.png icons.py",
    "-a -u -n SNew s_new.png icons.py",
    ]
    
if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)
