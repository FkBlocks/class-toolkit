import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import platform
import json
import os
from tools.logger import logger


class Ball:
    def __init__(self, tools: dict):
        """
        初始化悬浮球窗口
        :param tools: 工具列表
        :type tools: dict
        """
        logger.info("开始初始化悬浮球窗口")
        self.tools = tools
        self.collapsed = True
        self.menu_win = None

        # 加载配置
        self.default_config = {
            "settings_button_color": "#0080ff",
            "floatball_color": "#409eff",
            "menu_color": "#409eff",
            "exit_button_color": "#ff4d4f",
            "ask_exit": True
        }
        self.config = self.load_config()

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # 计算屏幕右侧靠下位置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - 80  # 距离右边80像素
        y = screen_height - 400  # 距离底部400像素
        self.root.geometry(f"+{x}+{y}")


        # 平台兼容
        logger.info(f"当前平台: {platform.system()}")
        if platform.system() == 'Windows':
            self.root.attributes("-transparentcolor", "white")
            self.root.config(bg="white")
            canvas_bg = "white"
        else:
            self.root.attributes("-alpha", 0.7)
            self.root.config(bg="black")
            canvas_bg = "black"

        # 圆球画布
        self.canvas = tk.Canvas(self.root, width=60, height=60,
                                highlightthickness=0, bg=canvas_bg)
        self.canvas.pack()
        self.canvas.create_oval(4, 4, 56, 56, fill=self.config.get("floatball_color", "#409eff"), outline="")
        self.canvas.create_text(30, 30, text="工具", fill="#efefef", font=("Microsoft Yahei", 16))
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<ButtonRelease-1>", self.toggle)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<Escape>", self.quit)
        self.root.focus_set()  # 确保窗口能获取焦点
        self.click_start_pos = None  # 记录鼠标点击起始位置
        self.has_dragged = False  # 记录是否发生过拖拽
        logger.info("初始化完成")
        
    def toggle(self, event):
        """展开/收缩菜单"""
        # 如果发生过拖拽，不触发菜单切换
        if self.has_dragged:
            return

        action = "展开" if self.collapsed else "收起"
        logger.info(f"菜单 {action}")
        if self.collapsed:
            self.expand()
        else:
            self.collapse()

    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.json")

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def expand(self):
        """展开菜单"""
        # 重新加载配置
        self.config = self.load_config()

        # 更新悬浮球颜色
        self.canvas.itemconfig(1, fill=self.config.get("floatball_color", "#409eff"))

        self.collapsed = False
        self.menu_win = tk.Toplevel(self.root)
        self.menu_win.overrideredirect(True)
        self.menu_win.attributes("-topmost", True)
        self.menu_win.config(bg=self.config.get("menu_color", "#409eff"))
        x, y = self.root.winfo_x(), self.root.winfo_y()
        self.menu_win.geometry(f"+{x-120}+{y}")

        for name, path in self.tools.items():
            btn = tk.Button(self.menu_win, text=name, width=12, height=2,
                            relief="flat", bg=self.config.get("menu_color", "#409eff"), fg="white",
                            command=lambda n=name, p=path: self.run_tool(p))
            btn.pack(pady=2)

        # 设置按钮
        settings_btn = tk.Button(self.menu_win, text="设置", width=12, height=2,
                                relief="flat", bg=self.config.get("settings_button_color", "#409eff"), fg="white",
                                command=lambda: self.run_tool(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "settings.py")))
        settings_btn.pack(pady=2)

        # 退出按钮
        exit_btn = tk.Button(self.menu_win, text="退出", width=12, height=2,
                             relief="flat", bg=self.config.get("exit_button_color", "#ff4d4f"), fg="white",
                             command=self.quit)
        exit_btn.pack(pady=2)

    def collapse(self):
        """收缩菜单"""
        if self.menu_win:
            self.menu_win.destroy()
            self.menu_win = None
        self.collapsed = True

    
    def run_tool(self, path):
        """拉起工具，无黑框"""
        try:
            logger.info(f"运行工具：{path}")
            # 获取当前脚本所在目录作为工作目录
            cwd = os.path.dirname(os.path.abspath(__file__))
            if path.endswith(".py"):
                if platform.system() == 'Windows':
                    subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NO_WINDOW, cwd=cwd)
                else:
                    subprocess.Popen([sys.executable, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
            else:
                if platform.system() == 'Windows':
                    subprocess.Popen([path], creationflags=subprocess.CREATE_NO_WINDOW, cwd=cwd)
                else:
                    subprocess.Popen([path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
            self.collapse()
            logger.info(f"运行工具：{path} 成功")
        except Exception as e:
            logger.error(f"运行工具：{path} 失败：{e}")

    
    def start_drag(self, event):
        """拖拽移动: 记录初始位置"""
        self.x0, self.y0 = event.x, event.y
        self.click_start_pos = (event.x, event.y)
        self.has_dragged = False  # 重置拖拽标志
       

    def on_drag(self, event):
        """拖拽移动: 移动窗口"""
        self.has_dragged = True  # 标记已发生拖拽
        dx = event.x - self.x0
        dy = event.y - self.y0
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")

        # 如果菜单已展开，同步移动菜单窗口
        if self.menu_win:
            menu_x = x - 120
            menu_y = y
            self.menu_win.geometry(f"+{menu_x}+{menu_y}")

    
    def quit(self, _=None):
        """退出程序"""
        if self.menu_win:
            # 弹窗确认是否关闭
            # 设置：退出时询问，config.json: "ask_exit": true
            if self.config.get("ask_exit", True):
                if messagebox.askyesno("确认", "确认退出？"):
                    self.collapse()
                    self.root.destroy()
                    logger.info("程序退出")
                    sys.exit(0)
                else:
                    logger.info("取消退出")
            
            else:
                self.collapse()
                self.root.destroy()
                logger.info("程序退出")
                sys.exit(0)

    def run(self):
        """主循环"""
        self.root.mainloop()