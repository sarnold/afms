Folder appltest contains testcases and testsuites for AFMS applications
based on Pythons unittest framework.
Tests run only on Win32 operating system because pywinauto
(http://pywinauto.openqa.org/) is used for remote controlling the
application

A patched version of pywinauto 0.3.7 is required. Apply win32_controls.py.patch
to the file pywinauto/controls/win32_controls.py:
    cp win32_controls.py win32_controls.py.org
    patch win32_controls.py win32_controls.py.patch
