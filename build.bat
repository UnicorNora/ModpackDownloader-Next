@echo off
rmdir bin /s /q
pyinstaller -n CurseModpackDownloader --onefile --noupx "download.py"
rmdir build /s /q
REN dist bin
PAUSE