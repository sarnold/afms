@echo off
rem Create HTML documentation using docutils

call rst2html --stylesheet=afmsdoc.css index.txt index.html
call rst2html --stylesheet=afmsdoc.css afeditor.txt afeditor.html
call rst2html --stylesheet=afmsdoc.css testrunner.txt testrunner.html
call rst2html --stylesheet=afmsdoc.css markup.txt markup.html
call rst2html --stylesheet=afmsdoc.css acknowledgement.txt acknowledgement.html
call rst2html --stylesheet=afmsdoc.css changelog.txt changelog.html
