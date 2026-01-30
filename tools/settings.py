import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
import json
import os
import sys
import subprocess
import platform
import copy
from logger import logger


class Settings:
    def __init__(self):
        # 获取项目根目录
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.window = tk.Tk()
        self.window.title("设置")
        self.center_window(self.window, 800, 600)

        # 加载配置
        self.default_config = {
            "settings_button_color": "#0080ff",
            "floatball_color": "#409eff",
            "menu_color": "#409eff",
            "exit_button_color": "#ff4d4f",
            "ask_exit": True
        }
        self.config = self.load_config()
        self.tools = self.load_tools()


        # 主框架
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧分类面板
        self.left_panel = ttk.Frame(self.main_frame, width=150)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # 右侧设置面板
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 分类列表
        self.categories = ["常规", "外观", "功能", "关于"]
        self.categories_button = []
        self.current_category = tk.StringVar(value=self.categories[0])

        for i, category in enumerate(self.categories):
            btn = ttk.Button(
                self.left_panel,
                text=category,
                command=lambda c=category: self.show_category(c)
            )
            btn.pack(fill=tk.X, pady=5, padx=5)
            self.categories_button.append(btn)

        # 底部关闭按钮
        bottom_frame = ttk.Frame(self.left_panel)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=5)

        close_btn = ttk.Button(
            bottom_frame,
            text="关闭",
            command=self.window.destroy,
            width=12
        )
        close_btn.pack(pady=5)

        self.window.mainloop()

    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(self.project_root, "config", "config.json")
        
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
            

    def save_config(self):
        """保存配置文件"""
        config_path = os.path.join(self.project_root, "config", "config.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def load_tools(self):
        """加载工具列表"""
        tools_path = os.path.join(self.project_root, "tools.json")
        try:
            with open(tools_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def save_tools(self):
        """保存工具列表"""
        tools_path = os.path.join(self.project_root, "tools.json")
        with open(tools_path, "w", encoding="utf-8") as f:
            json.dump(self.tools, f, indent=4, ensure_ascii=False)

    def show_category(self, category):
        """显示指定分类的设置内容"""
        self.current_category.set(category)
        self.clear_right_panel()

        if category == "常规":
            self.show_general_settings()
            self.add_apply_button()
        elif category == "外观":
            self.show_appearance_settings()
            self.add_apply_button()
        elif category == "功能":
            self.show_function_settings()
            self.add_apply_button()
        elif category == "关于":
            self.show_about()

    def clear_right_panel(self):
        """清空右侧面板"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()

    def add_apply_button(self):
        """在右侧面板底部添加应用按钮"""
        bottom_frame = ttk.Frame(self.right_panel)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=20)

        apply_btn = ttk.Button(
            bottom_frame,
            text="应用",
            command=self.apply_settings,
            width=15
        )
        apply_btn.pack(side=tk.RIGHT)

    def show_general_settings(self):
        """显示常规设置"""
        title = ttk.Label(self.right_panel, text="常规设置", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        # 开机自启动选项
        try:
            autostart_status = self.check_autostart()
        except Exception as e:
            autostart_status = False
            logger.warning(f"检查开机自启动状态失败: {e}")

        self.autostart_var = tk.BooleanVar(value=autostart_status)
        autostart_frame = ttk.Frame(self.right_panel)
        autostart_frame.pack(pady=20, fill=tk.X, padx=20)

        autostart_check = ttk.Checkbutton(
            autostart_frame,
            text="开机自启动",
            variable=self.autostart_var,
            command=self.toggle_autostart
        )
        autostart_check.pack(side=tk.LEFT, padx=5)

        # 添加说明文字
        desc_label = ttk.Label(
            autostart_frame,
            text="（仅Windows系统支持）",
            foreground="gray",
            font=("Arial", 9)
        )
        desc_label.pack(side=tk.LEFT, padx=5)

        # 退出时是否询问
        if_ask = self.config.get("ask_exit", True)
        self.ask_exit_var = tk.BooleanVar(value=if_ask)
        ask_exit_frame = ttk.Frame(self.right_panel)
        ask_exit_frame.pack(pady=10, fill=tk.X, padx=20)

        ask_exit_check = ttk.Checkbutton(
            ask_exit_frame,
            text="退出时询问",
            variable=self.ask_exit_var,
            command=self.toggle_ask_exit
        )
        ask_exit_check.pack(side=tk.LEFT, padx=5)


        # 显示日志按钮
        show_log_btn = ttk.Button(
            self.right_panel,
            text="显示日志",
            command=self.show_log,
            width=20
        )
        show_log_btn.pack(pady=10)
    
    def toggle_ask_exit(self):
        """切换退出时询问设置"""
        self.config["ask_exit"] = self.ask_exit_var.get()
        self.save_config()
        
    def show_log(self):
        """显示日志"""
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log", "running.log")
        try:
            if platform.system() == "Windows":
                subprocess.Popen(['notepad.exe', log_path])
            elif platform.system() == "Darwin":
                subprocess.Popen(['open', 'a', 'TextEdit', log_path])
            elif platform.system() == "Linux":
                subprocess.Popen(['xdg-open', log_path])
        except Exception as e:
            logger.warning(f"打开日志文件失败: {e}")
            messagebox.showwarning("错误", "打开日志文件失败")
        
    def show_appearance_settings(self):
        """显示外观设置"""
        title = ttk.Label(self.right_panel, text="外观设置", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        # 悬浮球颜色
        floatball_frame = ttk.Frame(self.right_panel)
        floatball_frame.pack(pady=10, fill=tk.X, padx=20)

        ttk.Label(floatball_frame, text="悬浮球颜色:").pack(side=tk.LEFT, padx=5)

        floatball_color_btn = tk.Button(
            floatball_frame,
            bg=self.config.get("floatball_color", "#409eff"),
            width=10,
            command=lambda: self.choose_color("floatball_color", floatball_color_btn)
        )
        floatball_color_btn.pack(side=tk.LEFT, padx=5)

        # 菜单颜色
        menu_frame = ttk.Frame(self.right_panel)
        menu_frame.pack(pady=10, fill=tk.X, padx=20)

        ttk.Label(menu_frame, text="菜单颜色:").pack(side=tk.LEFT, padx=5)

        menu_color_btn = tk.Button(
            menu_frame,
            bg=self.config.get("menu_color", "#409eff"),
            width=10,
            command=lambda: self.choose_color("menu_color", menu_color_btn)
        )
        menu_color_btn.pack(side=tk.LEFT, padx=5)

        # 设置按钮颜色
        settings_frame = ttk.Frame(self.right_panel)
        settings_frame.pack(pady=10, fill=tk.X, padx=20)

        ttk.Label(settings_frame, text="设置按钮颜色:").pack(side=tk.LEFT, padx=5)

        settings_color_btn = tk.Button(
            settings_frame,
            bg=self.config.get("settings_button_color", "#0080ff"),
            width=10,
            command=lambda: self.choose_color("settings_button_color", settings_color_btn)
        )
        settings_color_btn.pack(side=tk.LEFT, padx=5)

        # 退出按钮颜色
        exit_frame = ttk.Frame(self.right_panel)
        exit_frame.pack(pady=10, fill=tk.X, padx=20)

        ttk.Label(exit_frame, text="退出按钮颜色:").pack(side=tk.LEFT, padx=5)

        exit_color_btn = tk.Button(
            exit_frame,
            bg=self.config.get("exit_button_color", "#ff4d4f"),
            width=10,
            command=lambda: self.choose_color("exit_button_color", exit_color_btn)
        )
        exit_color_btn.pack(side=tk.LEFT, padx=5)

        # 恢复默认设置按钮
        restore_btn = ttk.Button(
            self.right_panel,
            text="恢复默认设置",
            command=self.restore_default_settings,
            width=20
        )
        restore_btn.pack(pady=10)

    def show_function_settings(self):
        """显示功能设置"""
        title = ttk.Label(self.right_panel, text="功能设置", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        # 添加工具区域
        add_tool_frame = ttk.LabelFrame(self.right_panel, text="添加工具", padding=10)
        add_tool_frame.pack(pady=10, fill=tk.X, padx=20)

        # 工具名称
        name_frame = ttk.Frame(add_tool_frame)
        name_frame.pack(pady=5, fill=tk.X)

        ttk.Label(name_frame, text="工具名称:").pack(side=tk.LEFT, padx=5)

        name_entry = ttk.Entry(name_frame, width=30)
        name_entry.pack(side=tk.LEFT, padx=5)

        # 工具路径
        path_frame = ttk.Frame(add_tool_frame)
        path_frame.pack(pady=5, fill=tk.X)

        ttk.Label(path_frame, text="工具路径:").pack(side=tk.LEFT, padx=5)

        path_entry = ttk.Entry(path_frame, width=30)
        path_entry.pack(side=tk.LEFT, padx=5)

        browse_btn = ttk.Button(
            path_frame,
            text="浏览...",
            command=lambda: self.browse_file(path_entry)
        )
        browse_btn.pack(side=tk.LEFT, padx=5)

        # 添加按钮
        add_btn = ttk.Button(
            add_tool_frame,
            text="添加",
            command=lambda: self.add_tool(name_entry, path_entry)
        )
        add_btn.pack(pady=10)

        # 工具列表
        list_frame = ttk.LabelFrame(self.right_panel, text="工具列表", padding=10)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        self.tools_listbox = tk.Listbox(list_frame, height=10)
        self.tools_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        self.refresh_tools_list()

        # 删除按钮
        delete_btn = ttk.Button(
            list_frame,
            text="删除选中工具",
            command=self.delete_tool
        )
        delete_btn.pack(pady=5)

    def show_about(self):
        """显示关于信息"""
        title = ttk.Label(self.right_panel, text="关于", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        info_frame = ttk.Frame(self.right_panel)
        info_frame.pack(pady=20, padx=20)

        # 版本信息
        version_label = ttk.Label(info_frame, text="版本: 1.1.0", font=("Arial", 12))
        version_label.pack(pady=10)

        # 作者信息（预留）
        author_label = ttk.Label(info_frame, text="作者: FkBlocks", font=("Arial", 12))
        author_label.pack(pady=10)

        # 其他信息
        desc_label = ttk.Label(
            info_frame,
            text="课堂悬浮球工具箱应用",
            font=("Arial", 10),
            foreground="gray"
        )
        desc_label.pack(pady=10)

    def choose_color(self, key, button):
        """选择颜色"""
        color = colorchooser.askcolor(title="选择颜色", color=self.config.get(key))
        if color[1]:
            self.config[key] = color[1]
            button.config(bg=color[1])
            self.save_config()

    def browse_file(self, entry):
        """浏览文件"""
        file_path = filedialog.askopenfilename(
            title="选择工具文件",
            filetypes=[("所有文件", "*.*")]
        )
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def add_tool(self, name_entry, path_entry):
        """添加工具"""
        name = name_entry.get().strip()
        path = path_entry.get().strip()

        if not name or not path:
            messagebox.showwarning("警告", "请填写完整的工具信息")
            return

        if name in self.tools:
            messagebox.showwarning("警告", "该工具名称已存在")
            return

        self.tools[name] = path
        self.save_tools()
        self.refresh_tools_list()

        name_entry.delete(0, tk.END)
        path_entry.delete(0, tk.END)

        messagebox.showinfo("成功", "工具添加成功")

    def delete_tool(self):
        """删除工具"""
        selection = self.tools_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的工具")
            return

        tool_name = self.tools_listbox.get(selection[0])
        del self.tools[tool_name]
        self.save_tools()
        self.refresh_tools_list()

        messagebox.showinfo("成功", "工具删除成功")

    def refresh_tools_list(self):
        """刷新工具列表"""
        self.tools_listbox.delete(0, tk.END)
        for name in self.tools.keys():
            self.tools_listbox.insert(tk.END, name)

    def check_autostart(self):
        """检查是否已设置开机自启动"""
        if platform.system() != 'Windows':
            return False
        try:
            startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            shortcut_path = os.path.join(startup_folder, 'class-toolkit.lnk')
            return os.path.exists(shortcut_path)
        except:
            return False

    def toggle_autostart(self):
        """切换开机自启动状态"""
        if platform.system() != 'Windows':
            messagebox.showwarning("提示", "开机自启动功能仅支持Windows系统")
            self.autostart_var.set(False)
            return

        try:
            if platform.system() == 'Windows':
                import winshell
                from win32com.client import Dispatch

                startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                shortcut_path = os.path.join(startup_folder, 'class-toolkit.lnk')
                main_path = os.path.join(self.project_root, "main.pyw")

                if self.autostart_var.get():
                    # 创建快捷方式
                    shell = Dispatch('WScript.Shell')
                    shortcut = shell.CreateShortCut(shortcut_path)
                    shortcut.Targetpath = sys.executable
                    shortcut.Arguments = f'"{main_path}"'
                    shortcut.WorkingDirectory = self.project_root
                    shortcut.save()
                    messagebox.showinfo("成功", "已设置开机自启动")
                    logger.info("已设置开机自启动")
                else:
                    # 删除快捷方式
                    if os.path.exists(shortcut_path):
                        os.remove(shortcut_path)
                    messagebox.showinfo("成功", "已取消开机自启动")
                    logger.info("已取消开机自启动")
            else:
                self.autostart_var.set(False)


        except ImportError:
            messagebox.showerror("错误", "缺少必要的库，请安装 pywin32 winshell库")
            self.autostart_var.set(False)
            logger.error("缺少开机自启动所需的库")

        except Exception as e:
            messagebox.showerror("错误", f"操作失败：{e}")
            self.autostart_var.set(False)
            logger.error(f"设置开机自启动失败：{e}")

    def apply_settings(self):
        """应用设置"""
        self.save_config()
        self.save_tools()
        # messagebox.showinfo("成功", "设置已应用，请点击悬浮球查看效果")

    def restore_default_settings(self):
        """恢复默认设置"""
        if messagebox.askyesno("确认", "确定要恢复默认设置吗？所有设置都会恢复！"):
            self.config = copy.deepcopy(self.default_config)
            self.save_config()
            # 重新显示外观设置页面（使用show_category确保正确清空和渲染）
            self.show_category("外观")
            messagebox.showinfo("成功", "已恢复默认设置")

    def center_window(self, window, width, height):
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == '__main__':
    Settings()