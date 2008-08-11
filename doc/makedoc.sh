# Create HTML documentation using docutils

python patch_release_info.py index.txt > tmp.txt
rst2html --stylesheet=afmsdoc.css tmp.txt index.html
rm tmp.txt
rst2html --stylesheet=afmsdoc.css afeditor.txt afeditor.html
rst2html --stylesheet=afmsdoc.css testrunner.txt testrunner.html
rst2html --stylesheet=afmsdoc.css markup.txt markup.html
rst2html --stylesheet=afmsdoc.css acknowledgement.txt acknowledgement.html
rst2html --stylesheet=afmsdoc.css changelog.txt changelog.html

