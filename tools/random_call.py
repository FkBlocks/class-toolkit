import tkinter as tk
from tkinter import ttk, Toplevel, scrolledtext, messagebox
import random
import os
from logger import logger

class BatchRollCall:
    """批量随机点名工具"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("批量随机点名")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        # 读取名单
        self.names = self.load_names()
        # print(self.names)
        logger.info("随机点名初始化成功")

        # 顶部输入区
        top = tk.Frame(self.root)
        top.pack(pady=10)
        tk.Label(top, text="本次点名人数：").pack(side="left")
        self.count_var = tk.IntVar(value=1)
        tk.Spinbox(top,
                   from_=1,
                   to=len(self.names),
                   textvariable=self.count_var,
                   width=5).pack(side="left")

        # 大按钮
        tk.Button(self.root, text="点名！", font=("Microsoft YaHei", 18),
                  command=self.roll).pack(pady=5)

        # 名字/学号 模式选项卡
        self.mode_var = tk.StringVar(value="name")

        # 单选按钮容器
        radio_frame = tk.Frame(self.root)
        radio_frame.pack(pady=10)

        # 名字选项卡
        tk.Radiobutton(radio_frame, text="点名", variable=self.mode_var, value="name").pack(side="left", padx=10)

        # 学号选项卡
        tk.Radiobutton(radio_frame, text="点学号", variable=self.mode_var, value="num").pack(side="left", padx=10)

        # 状态提示
        self.status = tk.Label(self.root, text="", fg="red")
        self.status.pack()

        # 主窗口居中
        self.center_window(self.root, 450, 180)

        self.root.mainloop()

    # ---------- 工具方法 ----------
    def load_names(self):
        """加载名单"""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "names.txt")
        if not os.path.isfile(path):
            messagebox.showerror("错误", "名单文件不存在！仅支持学号模式")
            logger.warning("名单文件不存在")
            return [f"同学{i:02d}" for i in range(1, 51)]
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def center_window(self, window, width, height):
        """居中创建窗口"""
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def roll(self):
        """点名方法"""
        # 获取点名模式
        mode = self.mode_var.get()
        total = len(self.names)
        if mode == "name":
            n = self.count_var.get()
            if n > total:
                self.status.config(text="人数超过名单总数！")
                logger.warning(f"用户输入点名数超过名单总数: {n}/{len(self.names)}")
                return
            else:
                selected = random.sample(self.names, n)
                self.show_result(selected)
        
        else:
            n = self.count_var.get()
            if n > total:
                self.status.config(text="人数超过名单总数！")
                logger.warning(f"用户输入点名数超过名单总数: {n}/{len(self.names)}")
                return
            else:
                students = [f"{i+1:02d}" for i in range(1, total + 1)]
                selected = random.sample(students, n)
                self.show_result(selected)


    def show_result(self, selected):
        """显示结果窗口"""
        top = Toplevel(self.root)
        top.title("点名结果")
        top.attributes("-topmost", True)   # 弹窗置顶
        self.center_window(top, 500, 500)  # 居中

        txt = scrolledtext.ScrolledText(top, width=20, height=7,
                                        font=("Microsoft YaHei", 32),
                                        bg="#f7f7f7", fg="#409eff")
        txt.pack(padx=20, pady=20)
        for name in selected:
            txt.insert("end", name + "\n")
        txt.configure(state="disabled")

        tk.Button(top, text="再点一次",
                  command=lambda: [top.destroy(), self.roll()],
                  width=12, height=2, bg="#409eff", fg="white").pack(pady=10)
        logger.info("点名完成")

if __name__ == "__main__":
    BatchRollCall()
