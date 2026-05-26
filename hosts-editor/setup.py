# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable
import sys

# 构建配置
build_options = {
    'packages': ['tkinter'],
    'excludes': ['tkinter.test'],
    'optimize': 2,
}

# 根据平台选择基础类型
base = 'Win32GUI' if sys.platform == 'win32' else None

setup(
    name="Hosts 编辑器",
    version="1.0",
    description="Windows Hosts 文件编辑器",
    options={"build_exe": build_options},
    executables=[
        Executable(
            "hosts_editor.py",
            base=base,
            icon=None,
            shortcut_name="Hosts 编辑器",
            shortcut_dir="DesktopFolder",
        )
    ]
)
