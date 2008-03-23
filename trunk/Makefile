AFE_SRC := $(wildcard af*.py) $(wildcard _af*.py) version.py \
           COPYING.txt README.txt CHANGELOG.txt

TR_SRC := testrunner.py $(wildcard tr*.py) $(wildcard _tr*.py)

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

