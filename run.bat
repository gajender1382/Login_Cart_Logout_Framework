@echo off
REM Sauce Demo — Login / Add to Cart / Logout Framework
REM Double-click to choose browser and run all tests

cd /d "%~dp0"
set PYTHONPATH=%~dp0

REM Activate virtual environment (install deps with: pip install -r requirements.txt)
call .venv\Scripts\activate.bat

echo.
echo ========================================
echo   Login / Cart / Logout Test Runner
echo ========================================
echo.
echo   1. Run on Chrome
echo   2. Run on Firefox
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" goto run_chrome
if "%choice%"=="2" goto run_firefox

echo Invalid choice. Please run again and enter 1 or 2.
pause
exit /b 1

:run_chrome
echo.
echo Running tests on Chrome...
pytest -s -v --html=./Reports/report.html --self-contained-html tests/ --browser chrome
goto end

:run_firefox
echo.
echo Running tests on Firefox...
pytest -s -v --html=./Reports/report.html --self-contained-html tests/ --browser firefox
goto end

:end
echo.
echo HTML report: Reports\report.html
pause
