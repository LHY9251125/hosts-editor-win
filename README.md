# 运维开发学习

一个 Windows Hosts 文件编辑器，用于方便地查看和修改系统 hosts 配置。

## 项目结构

```
yunwei-dev-learning/
├── hosts-editor/          # Hosts 文件编辑器
│   ├── hosts_editor.py    # 主程序
│   ├── build.bat          # 构建脚本
│   ├── setup.py           # PyInstaller 配置
│   └── dist/              # 编译输出目录
```

## Hosts 编辑器

一个简单易用的 Windows hosts 文件管理工具。

### 功能特点

- **快速添加**：通过表单快速添加 IP 和域名映射
- **直接编辑**：在文本框中直接编辑 hosts 文件内容
- **备份与恢复**：自动创建备份，支持从历史备份恢复
- **管理员提示**：提醒用户以管理员身份运行
- **快捷键支持**：`Ctrl+S` 保存，`Ctrl+R` 刷新

### 使用方法

#### 运行程序

1. 下载 `HostsEditor.exe`
2. 右键选择 **"以管理员身份运行"**
3. 开始编辑 hosts 文件

#### 从源码运行

```bash
cd hosts-editor
python hosts_editor.py
```

#### 编译打包

```bash
cd hosts-editor
python setup.py py2exe
# 或使用 build.bat
```

### 系统要求

- Windows 操作系统
- Python 3.x（从源码运行时）
- 管理员权限（修改 hosts 文件需要）

## 许可协议

MIT License