#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Hosts 文件编辑器
一个简单的小工具，用于方便地查看和修改 Windows 系统的 hosts 文件
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import shutil
from datetime import datetime


class HostsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Hosts 文件编辑器")
        self.root.geometry("800x600")

        # Windows hosts 文件路径
        self.hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        self.backup_dir = os.path.join(os.path.dirname(__file__), "backups")

        # 创建备份目录
        os.makedirs(self.backup_dir, exist_ok=True)

        self.setup_ui()
        self.load_hosts()

    def setup_ui(self):
        # 标题栏 - 部门信息
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(title_frame, text="IT 基础架构组开发", font=("Microsoft YaHei", 12, "bold"),
                  foreground="#1a73e8").pack(side=tk.LEFT)
        ttk.Label(title_frame, text="  -  Hosts 文件编辑器", font=("Microsoft YaHei", 10),
                  foreground="#666666").pack(side=tk.LEFT)

        # 管理员提示标签
        ttk.Label(title_frame, text="⚠ 请以管理员身份运行", font=("Microsoft YaHei", 9),
                  foreground="#d93025").pack(side=tk.RIGHT)

        # 顶部工具栏
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(toolbar, text="Hosts 文件路径:").pack(side=tk.LEFT)
        ttk.Label(toolbar, text=self.hosts_path, foreground="gray").pack(side=tk.LEFT, padx=5)

        ttk.Button(toolbar, text="刷新", command=self.load_hosts).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="保存", command=self.save_hosts).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="备份", command=self.create_backup).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="恢复备份", command=self.restore_backup).pack(side=tk.RIGHT, padx=2)

        # 添加区域
        add_frame = ttk.LabelFrame(self.root, text="快速添加", padding=10)
        add_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(add_frame, text="IP 地址:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_entry = ttk.Entry(add_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, "127.0.0.1")

        ttk.Label(add_frame, text="域名:").grid(row=0, column=2, padx=5, pady=5)
        self.domain_entry = ttk.Entry(add_frame, width=30)
        self.domain_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(add_frame, text="添加", command=self.add_entry).grid(row=0, column=4, padx=10, pady=5)

        # 编辑区域
        edit_frame = ttk.LabelFrame(self.root, text="Hosts 内容 (可直接编辑)", padding=10)
        edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_editor = scrolledtext.ScrolledText(edit_frame, wrap=tk.NONE, width=80, height=20)
        self.text_editor.pack(fill=tk.BOTH, expand=True)

        # 底部状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=10, pady=5)

        # 快捷键绑定
        self.root.bind('<Control-s>', lambda e: self.save_hosts())
        self.root.bind('<Control-r>', lambda e: self.load_hosts())

    def load_hosts(self):
        """读取 hosts 文件内容"""
        try:
            if not os.path.exists(self.hosts_path):
                messagebox.showerror("错误", f"找不到 hosts 文件：{self.hosts_path}")
                return

            with open(self.hosts_path, 'r', encoding='utf-8') as f:
                content = f.read()

            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, content)
            self.status_var.set(f"已加载 - {self.hosts_path}")

        except PermissionError:
            messagebox.showerror("权限错误", "需要以管理员身份运行才能修改 hosts 文件！\n\n请右键点击程序，选择'以管理员身份运行'")
            self.status_var.set("错误：需要管理员权限")
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(self.hosts_path, 'r', encoding='gbk') as f:
                    content = f.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, content)
                self.status_var.set(f"已加载 - {self.hosts_path} (GBK 编码)")
            except Exception as e:
                messagebox.showerror("错误", f"无法读取 hosts 文件：{e}")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取 hosts 文件：{e}")
            self.status_var.set(f"错误：{e}")

    def save_hosts(self):
        """保存 hosts 文件"""
        try:
            content = self.text_editor.get(1.0, tk.END).rstrip()

            # 先创建备份
            self.create_backup(silent=True)

            with open(self.hosts_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.status_var.set("保存成功！")
            messagebox.showinfo("成功", "Hosts 文件已保存！")

        except PermissionError:
            messagebox.showerror("权限错误", "需要以管理员身份运行才能修改 hosts 文件！\n\n请右键点击程序，选择'以管理员身份运行'")
            self.status_var.set("错误：需要管理员权限")
        except Exception as e:
            messagebox.showerror("错误", f"无法保存 hosts 文件：{e}")
            self.status_var.set(f"错误：{e}")

    def add_entry(self):
        """快速添加 hosts 条目"""
        ip = self.ip_entry.get().strip()
        domain = self.domain_entry.get().strip()

        if not ip or not domain:
            messagebox.showwarning("警告", "请输入 IP 地址和域名")
            return

        # 在末尾添加新条目
        self.text_editor.insert(tk.END, f"\n{ip} {domain}")
        self.status_var.set(f"已添加：{ip} {domain}")
        self.domain_entry.delete(0, tk.END)

    def create_backup(self, silent=False):
        """创建 hosts 文件备份"""
        try:
            if not os.path.exists(self.hosts_path):
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"hosts_backup_{timestamp}")

            shutil.copy2(self.hosts_path, backup_path)

            if not silent:
                self.status_var.set("备份已创建")
                messagebox.showinfo("成功", f"备份已保存到:\n{backup_path}")

        except Exception as e:
            if not silent:
                messagebox.showerror("错误", f"创建备份失败：{e}")

    def restore_backup(self):
        """从备份恢复"""
        try:
            # 获取备份文件列表
            backups = [f for f in os.listdir(self.backup_dir) if f.startswith("hosts_backup_")]

            if not backups:
                messagebox.showinfo("提示", "没有找到备份文件")
                return

            # 创建选择对话框
            restore_window = tk.Toplevel(self.root)
            restore_window.title("恢复备份")
            restore_window.geometry("400x300")

            ttk.Label(restore_window, text="选择要恢复的备份:").pack(pady=10)

            listbox = tk.Listbox(restore_window, width=50)
            listbox.pack(fill=tk.BOTH, expand=True, padx=10)

            for backup in sorted(backups, reverse=True):
                listbox.insert(tk.END, backup)

            def do_restore():
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning("警告", "请选择一个备份文件")
                    return

                backup_file = listbox.get(selection[0])
                backup_path = os.path.join(self.backup_dir, backup_file)

                if messagebox.askyesno("确认", f"确定要恢复到 {backup_file}?\n当前内容将丢失。"):
                    try:
                        shutil.copy2(backup_path, self.hosts_path)
                        self.load_hosts()
                        restore_window.destroy()
                        self.status_var.set(f"已恢复到 {backup_file}")
                        messagebox.showinfo("成功", "恢复成功！")
                    except PermissionError:
                        messagebox.showerror("权限错误", "需要以管理员身份运行")
                    except Exception as e:
                        messagebox.showerror("错误", f"恢复失败：{e}")

            ttk.Button(restore_window, text="恢复", command=do_restore).pack(pady=10)

        except Exception as e:
            messagebox.showerror("错误", f"无法列出备份：{e}")


def main():
    root = tk.Tk()
    app = HostsEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
