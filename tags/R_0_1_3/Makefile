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

AFE_SRC := $(wildcard af*.py) $(wildcard _af*.py) version.py afeditor.pyw \
           COPYING.txt README.txt CHANGELOG.txt

TR_SRC := testrunner.py $(wildcard tr*.py) $(wildcard _tr*.py) testrunner.pyw

ICON_SRC := $(wildcard icons/*.png) \
            $(addprefix icons/, mkimage.py README.txt COPYRIGHT.txt) 

DOC_SRC := $(addprefix doc/, afms.txt afms.html afmsdoc.css makedoc.cmd makedoc.sh) \
           $(wildcard doc/images/*.png) 

include version.py

VERSION := $(subst ",,$(VERSION))

ARCHIVE := $(addsuffix .tar, afms-$(VERSION))
ZIPARCHIVE := $(addsuffix .zip, afms-$(VERSION))

all: distrib

distrib:
	tar --create --file $(ARCHIVE) $(AFE_SRC)
	tar --file $(ARCHIVE) --append $(TR_SRC)
	tar --file $(ARCHIVE) --append $(ICON_SRC)
	tar --file $(ARCHIVE) --append $(DOC_SRC)
	gzip $(ARCHIVE)
	zip $(ZIPARCHIVE) $(AFE_SRC) $(TR_SRC) $(ICON_SRC) $(DOC_SRC)

