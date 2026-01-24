import tkinter as tk
import threading
import os
# from PIL import Image, ImageTk
from logger import logger


class CountDownTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("大字倒计时")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.minutes = 1
        self.seconds = 0
        self.running = False
        self.after_id = None

        # ===== 顶部：分 / 秒 大按钮加减 =====
        top = tk.Frame(self.root)
        top.pack(pady=20)

        # 分钟区
        tk.Button(top, text="-", font=("", 40), padx=15, pady=5,
                  command=lambda: self.adjust(0, -1)).pack(side="left")
        self.min_lbl = tk.Label(top, text=f"{self.minutes:02d}", font=("", 80))
        self.min_lbl.pack(side="left", padx=10)
        tk.Button(top, text="+", font=("", 40), padx=15, pady=5,
                  command=lambda: self.adjust(0, 1)).pack(side="left")

        tk.Label(top, text=":", font=("", 80)).pack(side="left", padx=5)

        # 秒钟区
        tk.Button(top, text="-", font=("", 40), padx=15, pady=5,
                  command=lambda: self.adjust(1, -1)).pack(side="left")
        self.sec_lbl = tk.Label(top, text=f"{self.seconds:02d}", font=("", 80))
        self.sec_lbl.pack(side="left", padx=10)
        tk.Button(top, text="+", font=("", 40), padx=15, pady=5,
                  command=lambda: self.adjust(1, 1)).pack(side="left")

        # ===== 控制按钮 =====
        btn_bar = tk.Frame(self.root)
        btn_bar.pack(pady=15)
        tk.Button(btn_bar, text="开始", width=8, height=2, font=("", 18),
                  command=self.start).pack(side="left", padx=10)
        tk.Button(btn_bar, text="暂停", width=8, height=2, font=("", 18),
                  command=self.pause).pack(side="left", padx=10)
        tk.Button(btn_bar, text="复位", width=8, height=2, font=("", 18),
                  command=self.reset).pack(side="left", padx=10)

        # ===== 大字倒计时 =====
        self.big = tk.Label(self.root, text="01:00", font=("Microsoft YaHei", 200),
                            fg="#409eff", bg="black")
        self.big.pack(fill="both", expand=True, padx=20, pady=10)
        self.big.bind("<ButtonPress-1>", self.start_drag)
        self.big.bind("<B1-Motion>", self.on_drag)

        self.center_window(900, 500)
        logger.info("倒计时窗口启动成功")
        # # 添加水印图片到右边靠上位置
        # watermark_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs", "light.png")
        # if os.path.exists(watermark_path):
        #     try:
        #         watermark_img = Image.open(watermark_path)
        #         watermark_img = watermark_img.resize((120, 60), Image.Resampling.LANCZOS)
        #         watermark_photo = ImageTk.PhotoImage(watermark_img)
        #         watermark_label = tk.Label(self.root, image=watermark_photo)
        #         watermark_label.place(relx=1.0, rely=0.35, anchor="ne")
        #         watermark_label.image = watermark_photo  # 保持引用
        #     except Exception as e:
        #         print(f"加载水印图片失败：{e}")
        #         logger.error(f"加载水印图片失败：{e}")

        self.root.mainloop()

    # ---------- 逻辑 ----------
    def adjust(self, unit, delta):
        """unit=0 分钟，unit=1 秒钟；delta=±1"""
        if unit == 0:
            self.minutes = max(0, min(99, self.minutes + delta))
            self.min_lbl.config(text=f"{self.minutes:02d}")
        else:
            self.seconds = max(0, min(59, self.seconds + delta))
            self.sec_lbl.config(text=f"{self.seconds:02d}")
        self.update_big()

    def update_big(self):
        self.big.config(text=f"{self.minutes:02d}:{self.seconds:02d}")

    def start(self):
        logger.info("倒计时开始")
        if not self.running:
            self.running = True
            self.count_down()

    def pause(self):
        logger.info("倒计时暂停")
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)

    def reset(self):
        logger.info("倒计时复位")
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.big.config(fg="#409eff", )
        self.minutes = 1
        self.seconds = 0
        self.adjust(0, 0)      # 刷新分钟显示
        self.adjust(1, 0)      # 刷新秒钟显示
        
    def count_down(self):
        if self.running:     
            total = self.minutes * 60 + self.seconds       
            self.update_big()
            if total <= 0:
                self.running = False
                self.big.config(fg="red")
                threading.Thread(target=self._beep).start()
                return
            
            if self.seconds == 0:
                self.minutes -= 1
                self.seconds = 59
            else:
                self.seconds -= 1
            self.after_id = self.root.after(1000, self.count_down)

    def _beep(self):
        try:
            import winsound
            for _ in range(3):
                winsound.Beep(1000, 300)
        except Exception as e:
            logger.error(f"播放声音失败：{e}")
            import time
            for _ in range(3):
                print("\a", end="", flush=True)
                time.sleep(0.3)

    # ---------- 居中 + 拖拽 ----------
    def center_window(self, w, h):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def start_drag(self, e):
        self.x0, self.y0 = e.x, e.y

    def on_drag(self, e):
        dx = e.x - self.x0
        dy = e.y - self.y0
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    CountDownTimer()