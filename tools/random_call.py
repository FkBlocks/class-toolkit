import sys
import os
import random
from logger import logger  # 假设您已有日志模块
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QSpinBox,
                             QPushButton, QRadioButton, QVBoxLayout,
                             QHBoxLayout, QButtonGroup, QDialog, QTextEdit)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QScreen


class BatchRollCall(QWidget):
    """批量随机点名工具"""

    def __init__(self):
        super().__init__()
        self.names = self.load_names()  # 加载名单
        self.init_ui()
        self.center_window()
        logger.info("随机点名初始化成功")

    def init_ui(self):
        self.setWindowTitle("批量随机点名")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # 主布局（垂直）
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 人数选择行
        top_content = QHBoxLayout()
        top_content.addWidget(QLabel("本次点名人数："))
        self.spin_count = QSpinBox()
        self.spin_count.setMinimum(1)
        self.spin_count.setMaximum(len(self.names))
        self.spin_count.setValue(1)
        self.spin_count.setFixedWidth(60)
        top_content.addWidget(self.spin_count)
        # 将内容放入一个外层水平布局，左右加伸缩项实现整体居中
        top_row = QHBoxLayout()
        top_row.addStretch()
        top_row.addLayout(top_content)
        top_row.addStretch()
        main_layout.addLayout(top_row)

        # 大按钮
        self.btn_roll = QPushButton("点名！")
        self.btn_roll.setFont(QFont("Microsoft YaHei", 18))
        self.btn_roll.setFixedSize(120, 50)
        self.btn_roll.setStyleSheet("""
                        QPushButton {
                            background-color: #ffffff;
                            color: black;
                            border: 1px solid black;
                            border-radius: 5px;}""")
        self.btn_roll.clicked.connect(self.roll)
        # 用水平布局包裹按钮
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.btn_roll)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

        # 模式选择行
        mode_content = QHBoxLayout()
        self.radio_name = QRadioButton("点名")
        self.radio_num = QRadioButton("点学号")
        self.radio_name.setChecked(True)
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.radio_name, 1)
        self.mode_group.addButton(self.radio_num, 2)
        mode_content.addWidget(self.radio_name)
        mode_content.addWidget(self.radio_num)
        # 外层居中布局
        mode_row = QHBoxLayout()
        mode_row.addStretch()
        mode_row.addLayout(mode_content)
        mode_row.addStretch()
        main_layout.addLayout(mode_row)

        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")
        # 同样用水平布局包裹使其居中
        status_row = QHBoxLayout()
        status_row.addStretch()
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        main_layout.addLayout(status_row)

        main_layout.activate()
        hint = main_layout.sizeHint()
        self.setFixedSize(450, hint.height())

    # 工具方法
    def load_names(self):
        """加载名单，与 Tkinter 版本逻辑相同"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "files", "names.txt")
        if not os.path.isfile(path):
            # 文件不存在时生成默认名单（仅用于演示）
            logger.warning("名单文件不存在，使用默认名单")
            return [f"同学{i:02d}" for i in range(1, 51)]
        with open(path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def center_window(self):
        """使主窗口居中显示"""
        screen = QApplication.primaryScreen().availableGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def roll(self):
        """点名方法"""
        mode = "name" if self.radio_name.isChecked() else "num"
        total = len(self.names)
        n = self.spin_count.value()

        if n > total:
            self.status_label.setText("人数超过名单总数！")
            logger.warning(f"点名人数 {n} 超过总数 {total}")
            return
        else:
            self.status_label.clear()  # 清空错误提示

        if mode == "name":
            selected = random.sample(self.names, n)
        else:  # 学号模式
            # 生成格式化学号：01, 02, ...
            students = [f"{i+1:02d}" for i in range(total)]
            selected = random.sample(students, n)

        self.show_result(selected)

    def show_result(self, selected):
        """显示结果窗口"""
        dialog = QDialog(self)
        dialog.setWindowTitle("点名结果")
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        dialog.resize(500, 500)

        # 使结果窗口居中
        self.center_dialog(dialog)

        # 创建文本显示区域
        text_edit = QTextEdit(dialog)
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Microsoft YaHei", 32))
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #f7f7f7;
                color: #409eff;
                border: none;
            }
        """)
        # 插入选中的名单，每行一个
        text_edit.setText("\n".join(selected))

        # 创建“再点一次”按钮
        btn_again = QPushButton("再点一次")
        btn_again.setFixedSize(120, 50)
        btn_again.setStyleSheet("""
            QPushButton {
                background-color: #409eff;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #66b1ff;
            }
        """)

        # 按钮点击：关闭当前窗口并重新点名
        btn_again.clicked.connect(lambda: [dialog.accept(), self.roll()])

        # 布局
        layout = QVBoxLayout(dialog)
        layout.addWidget(text_edit)
        layout.addWidget(btn_again, alignment=Qt.AlignmentFlag.AlignCenter)
        dialog.setLayout(layout)

        dialog.exec()  # 模态显示，也可用 show() 但需要处理生命周期
        logger.info("点名完成")

    def center_dialog(self, dialog):
        """将对话框居中于主窗口"""
        # 获取主窗口和对话框的尺寸
        main_geo = self.geometry()
        main_center = main_geo.center()
        dialog_geo = dialog.geometry()
        new_x = main_center.x() - dialog_geo.width() // 2
        new_y = main_center.y() - dialog_geo.height() // 2
        dialog.move(new_x, new_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BatchRollCall()
    window.show()
    sys.exit(app.exec())