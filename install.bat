@echo off
title Installing Dependencies...
python -m pip install -r ./requirements.txt
color b
cls
echo Downloaded all dependencies! Now you can run 'start.bat'.
PAUSE