# A float ball class toolkit suitable for large-screen touch all-in-one machines
# Copyright (C) 2026 FkBlocks
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import platform
import traceback as tb_module
from floatball import Ball
from tools.logger import create_logger
from tools.consts import DEFAULT_CONFIG


def check_platform():
    """
    检查运行平台是否是Windows，
    是继续运行，不是弹窗提示并退出
    """

    if platform.system() != "Windows":
        messagebox.showerror("错误", f"当前系统为 {platform.system()}，仅支持 Windows 平台运行。")
        sys.exit(1)

def ensure_config(project_root):
    """
    获取配置文件(config/config.json)，如果不存在则创建
    :param project_root: 项目根目录
    """
    cfg_dir = os.path.join(project_root, "config")
    cfg_path = os.path.join(cfg_dir, "config.json")
    default_config = DEFAULT_CONFIG
    os.makedirs(cfg_dir, exist_ok=True)
    if not os.path.exists(cfg_path):
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

# ... 导入部分 ...

# 获取项目根目录和资源目录
if getattr(sys, 'frozen', False):
    # 打包环境：原始 EXE 所在目录
    PROJECT_ROOT = os.path.dirname(os.path.abspath(sys.argv[0]))
    if hasattr(sys, '_MEIPASS'):
        RESOURCE_DIR = sys._MEIPASS   # 打包内部资源目录
    else:
        RESOURCE_DIR = PROJECT_ROOT
else:
    # 开发环境：脚本所在目录
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    RESOURCE_DIR = PROJECT_ROOT

# 确保配置文件存在（在 PROJECT_ROOT 下）
ensure_config(PROJECT_ROOT)

# 创建日志器
logger = create_logger(clear_log=True)
def check_and_fix_shortcut(project_root):
    if platform.system() != 'Windows':
        return
    try:
        from win32com.client import Dispatch
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        shortcut_path = os.path.join(startup_folder, 'class-toolkit.lnk')
        logger.info(f"快捷方式路径: {shortcut_path}")
        if not os.path.exists(shortcut_path):
            logger.info("快捷方式不存在，跳过检查")
            return

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        target_path = shortcut.Targetpath
        arguments = shortcut.Arguments

        # 期望的目标路径
        if getattr(sys, 'frozen', False):
            correct_target = os.path.abspath(sys.argv[0])   # 关键修改
            correct_arguments = ""
        else:
            correct_target = sys.executable
            main_path = os.path.join(project_root, "main.pyw")
            correct_arguments = f'"{main_path}"'

        # 比较并修复
        if (os.path.normpath(target_path).lower() != os.path.normpath(correct_target).lower() 
                or arguments != correct_arguments):
            logger.info("检测到快捷方式路径不正确，正在修复...")
            if getattr(sys, 'frozen', False):
                shortcut.Targetpath = correct_target
                shortcut.Arguments = ""
            else:
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = f'"{os.path.join(project_root, "main.pyw")}"'
            shortcut.WorkingDirectory = project_root
            shortcut.save()
            logger.info(f"快捷方式已修复，目标: {shortcut.Targetpath}")
        else:
            logger.info("快捷方式路径正确，无需修复")
    except Exception as e:
        logger.exception("检查/修复快捷方式失败")   # 记录完整异常


# 检查并修复快捷方式（支持便携版移动）
logger.info(f"=== 开机自启动检查 ===")
logger.info(f"项目根目录: {PROJECT_ROOT}")
logger.info(f"sys.executable: {sys.executable}")
logger.info(f"sys.executable (abs): {os.path.abspath(sys.executable)}")
logger.info(f"sys.frozen: {getattr(sys, 'frozen', False)}")
logger.info(f"sys._MEIPASS: {getattr(sys, '_MEIPASS', 'N/A')}")

# 检查是否在打包环境
if getattr(sys, 'frozen', False):
    logger.info("检测到打包环境")
    # 在打包环境中，sys.executable 应该就是 EXE 文件
    exe_path = os.path.abspath(sys.executable)
    logger.info(f"预期 EXE 路径: {exe_path}")
    logger.info(f"EXE 文件是否存在: {os.path.exists(exe_path)}")
else:
    logger.info("检测到开发环境")

check_and_fix_shortcut(PROJECT_ROOT)

# 主程序启动时清空日志
logger = create_logger(clear_log=True)

try:
    tools_path = os.path.join(PROJECT_ROOT, "tools.json")   # 注意：此时 PROJECT_ROOT 已经是原始 EXE 所在目录
    with open(tools_path, "r", encoding="utf-8") as f:
        TOOLS = json.load(f)
except FileNotFoundError:
    messagebox.showerror("错误", "tools.json 文件不存在")
    logger.error("tools.json 文件不存在")
    sys.exit(1)
def main():
    logger.info("开始运行程序")
    root = tk.Tk()
    root.withdraw()
    ball = Ball(TOOLS)
    ball.run()


if __name__ == "__main__":
    check_platform()
    main()