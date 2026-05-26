@echo off
chcp 65001 >nul
title Hosts 编辑器 - IT 基础架构组

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run
)

:: 请求管理员权限
echo 正在请求管理员权限...
powershell -Command "Start-Process '%~f0' -Verb RunAs"
exit /b

:run
:: 获取脚本所在目录
cd /d "%~dp0"

:: 启动程序
echo 正在启动 Hosts 编辑器...
echo.
echo ========================================
echo   IT 基础架构组开发 - Hosts 文件编辑器
echo ========================================
echo.

start "" "HostsEditor.exe"

exit
