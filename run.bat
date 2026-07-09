@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python -m pytest -s -v --html=./Reports/report.html --self-contained-html tests/ --browser chrome

REM Skip pause on Jenkins (pause blocks the build)
if defined JENKINS_URL goto :eof
if defined BUILD_NUMBER goto :eof
pause
