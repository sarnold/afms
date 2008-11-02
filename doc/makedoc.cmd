@echo off
rem Create HTML documentation using docutils


python patch_release_info.py index.txt > tmp.txt
call rst2html --link-stylesheet --stylesheet=afmsdoc.css tmp.txt index.html
del tmp.txt                      
call rst2html --link-stylesheet --stylesheet=afmsdoc.css afeditor.txt afeditor.htm
call rst2html --link-stylesheet --stylesheet=afmsdoc.css testrunner.txt testrunner.html
call rst2html --link-stylesheet --stylesheet=afmsdoc.css markup.txt markup.html
call rst2html --link-stylesheet --stylesheet=afmsdoc.css acknowledgement.txt acknowledgement.html
call rst2html --link-stylesheet --stylesheet=afmsdoc.css changelog.txt changelog.html
                              

python patch_html_head.py afeditor.htm > afeditor.html
