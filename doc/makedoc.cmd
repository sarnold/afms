@echo off
rem Create HTML documentation using docutils


python patch_release_info.py index.txt > tmp.txt
call rst2html --link-stylesheet --stylesheet=afmsdoc.css tmp.txt                index.htm
del tmp.txt                      
call rst2html --link-stylesheet --stylesheet=afmsdoc.css afeditor.txt           afeditor.htmx
call rst2html --link-stylesheet --stylesheet=afmsdoc.css testrunner.txt         testrunner.htm
call rst2html --link-stylesheet --stylesheet=afmsdoc.css markup.txt             markup.htm
call rst2html --link-stylesheet --stylesheet=afmsdoc.css acknowledgement.txt    acknowledgement.htm
call rst2html --link-stylesheet --stylesheet=afmsdoc.css changelog.txt          changelog.htm            
call rst2html --link-stylesheet --stylesheet=afmsdoc.css impressum.txt          impressum.html            
                              

python patch_html_head.py afeditor.htmx > afeditor.htm

python patch_html_body.py index.htm > index.html
python patch_html_body.py afeditor.htm > afeditor.html
python patch_html_body.py testrunner.htm > testrunner.html
python patch_html_body.py markup.htm > markup.html
python patch_html_body.py acknowledgement.htm > acknowledgement.html
python patch_html_body.py changelog.htm > changelog.html

rem *.htm don't have google ads
del index.htm afeditor.htm testrunner.htm markup.htm acknowledgement.htm changelog.htm       
del *.htmx

