import tkinter as tk
import json
from floatball import Ball
from tools.logger import create_logger

# 主程序启动时清空日志
logger = create_logger(clear_log=True)

TOOLS = json.load(open("./tools.json", "r", encoding="utf-8"))

def main():
    logger.info("开始运行程序")
    root = tk.Tk()
    root.withdraw()
    ball = Ball(TOOLS)
    ball.run()


if __name__ == "__main__":
    main()