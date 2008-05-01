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
           COPYING.txt README.txt CHANGELOG.txt \
           $(addprefix locale\de\LC_MESSAGES\, afms.mo)

TR_SRC := testrunner.py $(wildcard tr*.py) $(wildcard _tr*.py) testrunner.pyw

ICON_SRC := $(wildcard icons/*.png) \
            $(addprefix icons/, mkimage.py README.txt COPYRIGHT.txt) 

DOC_SRC := $(addprefix doc\, afms.txt afms.html afmsdoc.css makedoc.cmd makedoc.sh) \
           $(wildcard doc\images\*.png) 

include version.py

VERSION := $(subst ",,$(VERSION))

DISTRIBDIR := distrib
ARCHIVE := $(addprefix $(DISTRIBDIR)/, $(addsuffix .tar, afms-$(VERSION)))
ZIPARCHIVE := $(addprefix $(DISTRIBDIR)/, $(addsuffix .zip, afms-$(VERSION)))
TARGETDIR := afms-$(VERSION)

all: distrib clean

distrib:
	cd doc && cmd /C makedoc.cmd
	mkdir $(TARGETDIR)
	mkdir $(DISTRIBDIR)
	cp --parents $(AFE_SRC) $(TARGETDIR)
	cp --parents $(TR_SRC) $(TARGETDIR)
	cp --parents $(DOC_SRC) $(TARGETDIR)
	tar --create --file $(ARCHIVE) $(TARGETDIR)
	gzip $(ARCHIVE)
	zip -r $(ZIPARCHIVE) $(TARGETDIR)

clean:
	-rm -r $(TARGETDIR)

veryclean:
	-rm -r $(DISTRIBDIR)
    
.PHONY: distrib
