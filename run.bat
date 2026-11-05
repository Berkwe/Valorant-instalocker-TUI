@echo off
title Instalocker
cd /d "%~dp0"
where py >nul 2>&1 && set "PYTHON=py" || set "PYTHON=python"
%PYTHON% run.py %*
if errorlevel 9009 (
    echo Python was not found. Install it from https://www.python.org/downloads/
    pause
)
