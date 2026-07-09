@echo off
REM Run all tests on Chrome

cd /d "%~dp0"
call .venv\Scripts\activate.bat

echo Running all tests on Chrome...
pytest -s -v --html=./Reports/report.html --self-contained-html tests/ --browser chrome

echo.
echo HTML report: Reports\report.html
pause
