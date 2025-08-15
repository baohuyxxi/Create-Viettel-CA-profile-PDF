@echo off
REM Xoá build cũ
rmdir /s /q build
rmdir /s /q dist

REM Đóng gói project
pyinstaller ^
    --onefile ^
    --noconsole ^
    --icon=icon.ico ^
    --add-data "signatures;signatures" ^
    --add-data "tools;tools" ^
    --add-data "ui;ui" ^
    main.py

pause
