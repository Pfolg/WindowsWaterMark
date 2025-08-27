# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME Watermelon
AUTHOR Pfolg
TIME 2025/6/17 13:26
"""
import json
import os
import socket
import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QWidget, QLabel, QApplication, QVBoxLayout, QHBoxLayout


# 读取屏幕长宽
def get_screen_info() -> tuple:
    # 获取现有的 QApplication 实例
    _app = QApplication.instance()

    if _app is not None:
        screen = _app.primaryScreen().geometry()

        return screen.width(), screen.height()
    else:
        return 800, 600


def single_instance(port: int):
    print("checking port")
    if not port:
        port = 20520
    try:
        # 选择一个不常用的端口
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", port))
    except socket.error:
        print("Another simple is running, quit")
        QMessageBox.warning(
            None,
            "Warning",
            f"port: {port} is using, maybe there is an instance running \nor change the port.")
        sys.exit()
    return sock


def read_setting(file) -> dict:
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                # 这里大概会有bug
                setting: dict = json.load(f)
        except Exception as e:
            QMessageBox.critical(None, "Error", "An error happened when reading setting.\n" + str(e))
            print(str(e))
            return write_setting(file)
        if setting:
            return setting
        else:
            return write_setting(file)
    else:
        return write_setting(file)


def write_setting(file) -> dict:
    setting = {
        "line1": "Windows Hacked",
        "line2": "Go to http://127.0.0.1 to pay the ransom.",
        "port": 20520,
        "ratio": {
            "up": 8,
            "down": 1,
            "right": 1,
            "left": 20
        },
    }
    with open(file, "w", encoding="utf-8") as f:
        json.dump(setting, f, indent=4, ensure_ascii=False)

    return setting


class MyQWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.header_label = QLabel(self)
        self.content_label = QLabel(self)
        self.w, self.h = get_screen_info()
        self.setGeometry(0, 0, self.w, self.h)
        self.init_labels()

        # 启用透明度
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # 窗口顶置，去标题栏，去除任务栏图标，鼠标穿透
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)

    def setLabels(self, a: str, b: str) -> None:
        self.header_label.setText(a)
        self.content_label.setText(b)

    def init_labels(self):
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setBold(False)
        self.header_label.setStyleSheet("""
                        background-color: rgba(0, 0, 0, 0);
                        color: rgba(255, 255, 255, .7);
                        font-size: 18px;
                        """)  # font-weight: bold;
        self.content_label.setStyleSheet("""
                        background-color: rgba(0, 0, 0, 0);
                        color: rgba(255, 255, 255, .7);
                        font-size: 12px;
                        """)
        self.header_label.setFont(font)
        self.content_label.setFont(font)

    def adjust_label(self, up: int = 8, down: int = 1, left: int = 20, right: int = 1) -> None:
        # 清除现有布局
        if self.layout():
            QWidget().setLayout(self.layout())

        main_layout = QVBoxLayout(self)
        # 上方空白 (拉伸因子 = up)
        main_layout.addStretch(up)

        # 水平布局容器
        h_container = QHBoxLayout()
        # 左侧空白 (拉伸因子 = left)
        h_container.addStretch(left)

        # 文字容器
        text_layout = QVBoxLayout()
        text_layout.addWidget(self.header_label)
        text_layout.addWidget(self.content_label)
        h_container.addLayout(text_layout)

        # 右侧空白 (拉伸因子 = right)
        h_container.addStretch(right)

        # 添加水平容器到主布局
        main_layout.addLayout(h_container)

        # 下方空白 (拉伸因子 = down)
        main_layout.addStretch(down)

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()


if __name__ == '__main__':
    setting_file = "text.json"
    setting_data = read_setting(setting_file)
    print(setting_data)
    instance = single_instance(setting_data.get("port"))
    app = QApplication(sys.argv)
    Window = MyQWidget()
    try:
        ratio: dict = setting_data.get("ratio")
        Window.adjust_label(ratio.get("up"), ratio.get("down"), ratio.get("left"), ratio.get("right"))
    except Exception as e:
        print(e)
        Window.adjust_label()
    Window.setLabels(setting_data.get("line1"), setting_data.get("line2"))
    Window.show()
    sys.exit(app.exec())
