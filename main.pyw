import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import platform
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

# 获取项目根目录
if getattr(sys, 'frozen', False):
    # 打包环境：使用 exe 所在目录作为根目录
    PROJECT_ROOT = os.path.dirname(sys.executable)
else:
    # 开发环境：使用脚本所在目录
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 确保配置文件存在并加载
ensure_config(PROJECT_ROOT)

# 主程序启动时清空日志
logger = create_logger(clear_log=True)

try:
    TOOLS = json.load(open(os.path.join(PROJECT_ROOT, "tools.json"), "r", encoding="utf-8"))
except FileNotFoundError:
    messagebox.showerror("错误", "tools.json 文件不存在，创建后重试")
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