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

    d = {
    'bugtracker_url' : 'http://sourceforge.net/tracker/?func=add&group_id=219925&atid=1048159',
    'feature_url'    : 'http://sourceforge.net/tracker/?func=add&group_id=219925&atid=1048162',
    'patch_url'      : 'http://sourceforge.net/tracker/?func=add&group_id=219925&atid=1048161'}
    info.feedback=_("""<p><b>Feedback about this program is welcome and encouraged!</b></p>
<p>
Please report any bugs to the bug tracker at <a href="%(bugtracker_url)s">%(bugtracker_url)s</a>
</p>
<p>
Requests for new features may be entered at <a href="%(feature_url)s">%(feature_url)s</a>
</p>
<p>
Patches are welcome at <a href="%(patch_url)s">%(patch_url)s</a>
</p>
""")
    info.feedback = info.feedback % d

    return info


