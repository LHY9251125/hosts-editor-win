@echo off
echo 正在启动 Hosts 编辑器...
echo 需要管理员权限来修改 hosts 文件
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    python "%~dp0hosts_editor.py"
) else (
    :: 请求管理员权限
    powershell -Command "Start-Process cmd -ArgumentList '/c', 'cd /d \"%~dp0\" && python hosts_editor.py' -Verb RunAs"
)
