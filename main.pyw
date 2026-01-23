import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
from floatball import Ball
from tools.logger import create_logger

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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