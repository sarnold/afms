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

from afresource import _
import version

def getInfo(info):
    info.Name = "AFMS Editor"
    info.Version = version.VERSION
    info.Copyright = u"Copyright (C) 2008 Achim Köhler"
    info.Description = _("Editor for the Artefact Management System")
    info.WebSite = ("http://sourceforge.net/projects/afms/", "Artefact Management System Homepage")
    info.Developers = [ u"Achim Köhler" ]
    info.License = _("""This program comes with ABSOLUTELY NO WARRANTY; 
This is free software, and you are welcome to redistribute it
under the terms of the GNU General Public License; see the accompanied file COPYING for details.""")

    return info


