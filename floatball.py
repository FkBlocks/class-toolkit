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
        self.animating = False
        self.anim_step = 0
        self.target_x = 0
        self.menu_start_x = 0

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
        # 如果正在动画中，不重复展开
        if self.animating:
            return
        
        # 重新加载配置
        self.config = self.load_config()

        # 更新悬浮球颜色
        self.canvas.itemconfig(1, fill=self.config.get("floatball_color", "#409eff"))

        self.collapsed = False
        self.menu_win = tk.Toplevel(self.root)
        self.menu_win.overrideredirect(True)
        self.menu_win.attributes("-topmost", True)
        self.menu_win.config(bg=self.config.get("menu_color", "#409eff"))
        self.menu_win.attributes("-alpha", 0.0)  # 初始透明度为0
        
        # 获取悬浮球位置
        x, y = self.root.winfo_x(), self.root.winfo_y()
        
        # 目标位置（悬浮球左侧，距离悬浮球10像素）
        self.target_x = x - 130
        
        # 初始位置（悬浮球中心位置，从球内部发射）
        self.menu_start_x = x - 30
        
        # 设置初始位置（从球中心开始）
        self.menu_win.geometry(f"+{self.menu_start_x}+{y}")

        for name, path in self.tools.items():
            btn = tk.Button(self.menu_win, text=name, width=12, height=2,
                            relief="flat", bg=self.config.get("menu_color", "#409eff"), fg="white",
                            command=lambda n=name, p=path: self.run_tool(p))
            btn.pack(pady=2)

        # 设置按钮
        settings_btn = tk.Button(self.menu_win, text="设置", width=12, height=2,
                                relief="flat", bg=self.config.get("settings_button_color", "#0080ff"), fg="white",
                                command=lambda: self.run_tool(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "settings.py")))
        settings_btn.pack(pady=2)

        # 退出按钮
        exit_btn = tk.Button(self.menu_win, text="退出", width=12, height=2,
                             relief="flat", bg=self.config.get("exit_button_color", "#ff4d4f"), fg="white",
                             command=self.quit)
        exit_btn.pack(pady=2)
        
        # 开始展开动画
        self.animating = True
        self.anim_step = 0
        self.animate_expand()

    def collapse(self):
        """收缩菜单"""
        if self.menu_win and not self.animating:
            self.animating = True
            self.anim_step = 0
            self.menu_start_x = self.menu_win.winfo_x()
            self.target_x = self.menu_start_x + 240  # 向右移动240像素消失
            self.animate_collapse()

    
    def run_tool(self, path):
        """拉起工具，无黑框"""
        if self.animating:
            return  # 动画中不响应
            
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
            messagebox.showerror("错误", f"运行工具：{path} 失败：{e}")
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

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 获取窗口尺寸
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # 限制窗口在屏幕内
        x = max(0, min(x, screen_width - window_width))
        y = max(0, min(y, screen_height - window_height))

        self.root.geometry(f"+{x}+{y}")

        # 如果菜单已展开，同步移动菜单窗口（悬浮球左侧，距离10像素）
        if self.menu_win:
            menu_x = max(0, min(x - 130, screen_width - 130))
            menu_y = max(0, min(y, screen_height - 120))  # 防止菜单窗口超出屏幕
            
            self.menu_win.geometry(f"+{menu_x}+{menu_y}")

    def animate_expand(self):
        """展开动画：从球内发射出来 + 淡入"""
        if not self.menu_win:
            self.animating = False
            return
        
        self.anim_step += 1
        
        # 使用缓动函数让动画更自然
        progress = min(self.anim_step / 20, 1.0)  # 20帧完成动画
        ease_progress = 1 - (1 - progress) ** 3  # 缓出效果
        
        # 计算当前X位置（从球中心向左移动）
        current_x = int(self.menu_start_x + (self.target_x - self.menu_start_x) * ease_progress)
        
        # 计算透明度（淡入效果，前半段快速淡入）
        alpha = min(progress * 1.5, 1.0)
        self.menu_win.attributes("-alpha", alpha)
        
        # 更新位置
        x, y = self.root.winfo_x(), self.root.winfo_y()
        self.menu_win.geometry(f"+{current_x}+{y}")
        
        if self.anim_step < 20:
            # 继续动画
            self.root.after(16, self.animate_expand)  # 约60fps
        else:
            # 动画完成
            self.menu_win.attributes("-alpha", 1.0)  # 确保完全显示
            self.animating = False
            logger.info("菜单展开动画完成")

    def animate_collapse(self):
        """收缩动画：收回到球内 + 淡出"""
        if not self.menu_win:
            self.animating = False
            self.collapsed = True
            return
        
        self.anim_step += 1
        
        # 使用缓动函数让动画更自然
        progress = min(self.anim_step / 20, 1.0)  # 20帧完成动画
        ease_progress = progress ** 3  # 缓入效果
        
        # 获取悬浮球中心位置
        x, y = self.root.winfo_x(), self.root.winfo_y()
        ball_center_x = x - 30
        
        # 计算当前X位置（从当前位置回到球中心）
        current_x = int(self.menu_start_x + (ball_center_x - self.menu_start_x) * ease_progress)
        
        # 计算透明度（淡出效果，后半段快速淡出）
        alpha = 1.0 - progress * 1.5
        if alpha < 0:
            alpha = 0
        self.menu_win.attributes("-alpha", alpha)
        
        # 更新位置
        self.menu_win.geometry(f"+{current_x}+{y}")
        
        if self.anim_step < 20:
            # 继续动画
            self.root.after(16, self.animate_collapse)
        else:
            # 动画完成，销毁菜单
            if self.menu_win:
                self.menu_win.destroy()
                self.menu_win = None
            self.animating = False
            self.collapsed = True
            logger.info("菜单收起动画完成")

    
    def quit(self, _=None):
        """退出程序"""
        if self.animating:
            # 如果正在动画中，等待动画完成
            return
            
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