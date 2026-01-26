import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
from floatball import Ball
from tools.logger import create_logger


def ensure_config(project_root):
    """
    获取配置文件(config/config.json)，如果不存在则创建
    :param project_root: 项目根目录
    """
    cfg_dir = os.path.join(project_root, "config")
    cfg_path = os.path.join(cfg_dir, "config.json")
    default_config = {
        "settings_button_color": "#0080ff",
        "floatball_color": "#409eff",
        "menu_color": "#409eff",
        "exit_button_color": "#ff4d4f",
        "ask_exit": True
    }
    os.makedirs(cfg_dir, exist_ok=True)
    if not os.path.exists(cfg_path):
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)

# 获取项目根目录
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
    main()