# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME main
AUTHOR Pfolg
TIME 2025/5/20 13:06
"""
import json
import os.path
import socket
import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QMessageBox, QApplication


class MyQWidget(QWidget):
    def __init__(self):
        super().__init__()

    # 忽略关闭事件
    def closeEvent(self, event):
        event.ignore()


def set_QWidget(window: QWidget, geometry: list[int, int, int, int], line1: str, line2: str):
    # 设定窗口
    window.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
    # 窗口位置和大小
    window.setGeometry(*geometry)
    # 定义标签和父级
    label1 = QLabel(parent=window)
    label2 = QLabel(parent=window)
    # 设置标签在Widget中位置
    label1.setGeometry(0, 0, 400, 50)
    label2.setGeometry(0, 20, 400, 50)
    # 设置样式
    label1.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0);
                color: rgba(255, 255, 255, .7);
                font-size: 18px;
                """)  # font-weight: bold;
    label2.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0);
                color: rgba(255, 255, 255, .7);
                font-size: 12px;
                """)
    font = QtGui.QFont()
    font.setFamily("Microsoft YaHei UI")
    font.setBold(False)
    label1.setFont(font)
    label2.setFont(font)
    # 设置文本
    label1.setText(line1)
    label2.setText(line2)
    # 启用透明度
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    # 窗口顶置，去标题栏，去除任务栏图标，鼠标穿透
    window.setWindowFlags(
        Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)


def single_instance(port: int):
    print("checking port")
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


def read_setting(file):
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


def write_setting(file):
    setting = {
        "line1": "Windows Hacked",
        "line2": "Go to http://127.0.0.1 to pay the ransom.",
        "port": 52520,
        "geometry": [1250, 720, 600, 100],
        "notify": True,
    }
    with open(file, "w", encoding="utf-8") as f:
        json.dump(setting, f, indent=4, ensure_ascii=False)

    return setting


if __name__ == '__main__':
    app = QApplication(sys.argv)

    setting_file = "text.json"
    setting_data = read_setting(setting_file)
    # 设置标签
    window = MyQWidget()
    set_QWidget(window, setting_data.get("geometry"), setting_data.get("line1"), setting_data.get("line2"))
    window.show()
    # 占用端口以识别单个实例
    lock_socket = single_instance(setting_data.get("port"))
    if setting_data.get("notify"):
        QMessageBox.information(
            None,
            "information",
            "The Water Mark is showing.\nYou can close it via Task Manager.",
        )
    sys.exit(app.exec())
