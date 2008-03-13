AFE_SRC := afeditor.py afconfig.py afexporthtml.py afexportxml.py \
           afinfo.py afmodel.py afresource.py  _afartefactlist.py \
           _afbasenotebook.py _afdocutils.py _afeditartefactdlg.py \
           _affeatureview.py _afhelper.py _afhtmlwindow.py _afimages.py \
           _afimportartefactdlg.py _afimporter.py _afmainframe.py \
           _afproductinformation.py _afproducttree.py _afrequirementview.py \
           _aftestcaseview.py _aftestsuiteview.py _aftrashinformation.py \
           _afusecaseview.py _afvalidators.py afmsreport.css version.py \
           _afclipboard.py \
           COPYING.txt README.txt CHANGELOG.txt

TR_SRC := testrunner.py trconfig.py trexporthtml.py trexportxml.py \
          trinfo.py trmodel.py _trcanceldlg.py _trexectestrundlg.py \
          _trinfotestrundlg.py _trmainframe.py _trnewtestrunwiz.py \
          _trtestcaseview.py _trtestresultview.py

ICON_SRC := 24-tag-manager.png 24-tag-add.png 16-arrow-down.png 16-circle-blue-delete.png \
            16-circle-blue.png 16-circle-green-check.png 16-circle-red-delete.png \
            16-message-warn.png 24-arrow-next.png 24-tab-add.png 24-tab-open.png \
            24-tag-pencil.png 24-tag-remove.png applications-system_16x16.png \
            applications-system_32x32.png f_new.PNG mkimage.py rq_new.PNG tc_new.png \
            tr-pass.png ts_new.PNG uc_new.PNG user-trash-full.png user-trash.png \
            mkimage.py README.txt COPYRIGHT.txt

ICON_SRC := $(addprefix icons/, $(ICON_SRC))

DOC_SRC := afms.txt afms.html afmsdoc.css makedoc.cmd makedoc.sh \
           images/screenshot_edit_product_html.png \
           images/screenshot_view_product_html.png \
           images/screenshot_overview.png

DOC_SRC := $(addprefix doc/, $(DOC_SRC))

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

