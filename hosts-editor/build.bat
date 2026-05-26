@echo off
chcp 65001 >nul
echo ========================================
echo   Hosts 编辑器 - 打包工具
echo ========================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

echo [1/2] 安装 PyInstaller...
pip install pyinstaller -q

echo [2/2] 开始打包...
pyinstaller --onefile --windowed --name "HostsEditor" --icon=NONE hosts_editor.py --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo [完成] 打包成功!
echo 可执行文件位置：dist\HostsEditor.exe
echo ========================================
echo.

:: 打开 dist 目录
explorer "%~dp0dist"

pause
