import tkinter as tk
from tkinter import Toplevel, scrolledtext, messagebox
import random
import os
# from PIL import Image, ImageTk
from logger import logger

class BatchRollCall:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("批量随机点名")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        # 读取名单
        self.names = self.load_names()
        # print(self.names)
        logger.info(f"随机点名初始化成功")

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
                  command=self.roll).pack(pady=15)

        # 状态提示
        self.status = tk.Label(self.root, text="", fg="red")
        self.status.pack()

        # 主窗口居中
        self.center_window(self.root, 400, 140)

        # # 添加水印图片到主窗口右下角
        # watermark_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs", "light.png")
        # if os.path.exists(watermark_path):
        #     try:
        #         watermark_img = Image.open(watermark_path)
        #         watermark_img = watermark_img.resize((120, 60), Image.Resampling.LANCZOS)
        #         watermark_photo = ImageTk.PhotoImage(watermark_img)
        #         watermark_label = tk.Label(self.root, image=watermark_photo)
        #         watermark_label.place(relx=1.0, rely=1.0, anchor="se")
        #         watermark_label.image = watermark_photo  # 保持引用
        #     except Exception as e:
        #         logger.warning(f"加载水印图片失败：{e}")

        self.root.mainloop()

    # ---------- 工具方法 ----------
    def load_names(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "names.txt")
        if not os.path.isfile(path):
            messagebox.showerror("错误", "名单文件不存在！使用默认名单。")
            logger.warning("名单文件不存在")
            return [f"同学{i:02d}" for i in range(1, 51)]
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def center_window(self, window, width, height):
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def roll(self):
        n = self.count_var.get()
        if n > len(self.names):
            self.status.config(text="人数超过名单总数！")
            logger.warning(f"用户输入点名数超过名单总数: {n}/{len(self.names)}")
            return
        selected = random.sample(self.names, n)
        self.show_result(selected)

    def show_result(self, selected):
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

        # # 添加水印图片到右下角
        # watermark_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs", "light.png")
        # if os.path.exists(watermark_path):
        #     try:
        #         watermark_img = Image.open(watermark_path)
        #         watermark_img = watermark_img.resize((120, 60), Image.Resampling.LANCZOS)
        #         watermark_photo = ImageTk.PhotoImage(watermark_img)
        #         watermark_label = tk.Label(top, image=watermark_photo, bg="#f7f7f7")
        #         watermark_label.place(relx=1.0, rely=1.0, anchor="se")
        #         watermark_label.image = watermark_photo  # 保持引用
        #     except Exception as e:
        #         logger.warning(f"加载水印图片失败：{e}")

        tk.Button(top, text="再点一次",
                  command=lambda: [top.destroy(), self.roll()],
                  width=12, height=2, bg="#409eff", fg="white").pack(pady=10)
        logger.info("点名完成")

if __name__ == "__main__":
    BatchRollCall()
