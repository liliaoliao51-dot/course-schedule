@echo off
chcp 65001 >nul
title 课表应用 - 一键启动
cd /d "%~dp0"
python start.py
pause
