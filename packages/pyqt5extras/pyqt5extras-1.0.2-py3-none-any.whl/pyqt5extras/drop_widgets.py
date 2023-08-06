#!/usr/bin/env python
# coding=utf-8
# @Time    : 2021/8/24 19:07
# @Author  : 江斌
# @Software: PyCharm
import os
import sys
import json
import copy
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QDrag

BTN_WIDTH = 70
BTN_HEIGHT = 80
ICON_WIDTH = 60
ICON_HEIGHT = 60


class DroppableToolButton(QtWidgets.QToolButton):
    """可拖拽按钮。"""

    def __init__(self, name, type=None, image_path=None, parent=None, user_data=None):
        super(DroppableToolButton, self).__init__(parent)
        self.user_data = user_data
        self.setFixedWidth(BTN_WIDTH)
        self.setFixedHeight(BTN_HEIGHT)
        self.name = name
        self.type = type
        self.image_path = image_path
        # self.setText(name)
        if os.path.exists(self.image_path):
            self.setIcon(QtGui.QIcon(self.image_path.strip()))
            self.setIconSize(QtCore.QSize(ICON_WIDTH, ICON_HEIGHT))
        self.borderColor = QColor(190, 190, 190)
        self.borderWidth = 3
        self.placeholder = 'C'
        self.setText(self.name)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    @property
    def data(self):
        return dict(name=self.name, type=self.type, image_path=self.image_path)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        mimeData.setText(json.dumps(self.data))
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec_(Qt.MoveAction)
        self.setDown(False)
        self.setAcceptDrops(False)

    def __str__(self):
        return f"DroppableToolButton(name='{self.name}', user_data='{self.user_data}')"

    def __repr__(self):
        return str(self)

    def paintEvent(self, event):
        super(DroppableToolButton, self).paintEvent(event)
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing, on=True)
        pen = QPen(self.borderColor, self.borderWidth, Qt.DotLine, Qt.RoundCap)
        font = QtGui.QFont('Serif', 30, QtGui.QFont.Light)
        pt.setPen(pen)
        pt.setFont(font)
        x = int(self.width() * 0.1)
        y = int(self.height() * 0.5)
        # pt.drawText(x, y, self.placeholder)
        pt.end()


class DropButtonWidget(QWidget):
    """可拖拽区域。"""
    drop_signal = pyqtSignal(object, object)  # idx
    data_signal = pyqtSignal(object)

    def __init__(self, idx=0):
        super(DropButtonWidget, self).__init__()
        self.idx = idx
        self.widget = None
        self.setAcceptDrops(True)
        self.setFixedWidth(BTN_WIDTH)
        self.setFixedHeight(BTN_HEIGHT)
        self.hoverBackground = QColor(0, 245, 250)
        self.borderColor = QColor(190, 190, 190)
        self.borderRadius = 5  # 26
        self.borderWidth = 2
        self.placeholder = 'Drop here!'
        self.dragEnter = False
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.addSpacing(1)
        self.setLayout(self.layout)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_root_menu)

    def show_root_menu(self, pos):
        if self.widget:
            menu = QtWidgets.QMenu()
            action1 = QtWidgets.QAction("移除", parent=menu)
            action1.triggered.connect(self.clear_widget)
            actions = [
                action1,
                # action2
            ]
            menu.addActions(actions)
            menu.exec_(self.mapToGlobal(pos))

    def clear_widget(self):
        if self.widget:
            self.layout.removeWidget(self.widget)
            self.widget = None
            print(f'clear_widget: {self.widget} {self.layout.count()}')

    def replace_widget(self, widget):
        old_widget = self.widget
        if self.widget:
            self.layout.removeWidget(self.widget)
        if widget:
            widget.user_data = dict(parent_idx=self.idx)
            self.layout.addWidget(widget)
            self.widget = widget
        return old_widget

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            self.dragEnter = True
            event.accept()
            self.repaint()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.dragEnter = False
        self.repaint()

    def on_clicked(self):
        self.data_signal.emit(self.widget.data)

    def dropEvent(self, event):
        mime = event.mimeData()
        data = mime.text()
        d = json.loads(data)
        if self.widget:  # 占位已经有控件
            self.drop_signal.emit(self.idx, self.widget)
            self.layout.removeWidget(self.widget)
        skil_item = DroppableToolButton(**d, user_data=dict(parent_idx=self.idx))
        skil_item.clicked.connect(self.on_clicked)
        self.layout.addWidget(skil_item)
        self.widget = skil_item
        self.dragEnter = False
        self.repaint()

    def paintEvent(self, event):
        super(DropButtonWidget, self).paintEvent(event)
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing, on=True)

        pen = QPen(self.borderColor, self.borderWidth, Qt.DotLine, Qt.RoundCap)
        pt.setPen(pen)

        if self.dragEnter:
            brush = QBrush(self.hoverBackground)
            pt.setBrush(brush)

        x = int(self.width() * 0.1)
        y = int(self.height() * 0.5)
        pt.drawText(x, y, self.placeholder)
        pt.drawRoundedRect(self.borderWidth, self.borderWidth, self.width() - self.borderWidth * 2,
                           self.height() - self.borderWidth * 2, self.borderRadius, self.borderRadius)

        pt.end()


class CustomToolRowWidget(QWidget):
    data_signal = pyqtSignal(object)

    def __init__(self, num=10):
        super(CustomToolRowWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setMinimumSize(120, 65)
        self.hoverBackground = QColor(0, 245, 250)
        self.borderColor = QColor(190, 190, 190)
        self.borderRadius = 5  # 26
        self.borderWidth = 6
        self.num = num
        self.init_ui()

    def on_clicked(self, data):
        self.data_signal.emit(data)

    def on_drop(self, idx, widget):
        if widget.user_data:
            parent_idx = widget.user_data['parent_idx']
            self.btns[parent_idx].clear_widget()
        # for i in range(idx, len(self.btns) - 1):
        #     widget = self.btns[i + 1].replace_widget(widget)

    def init_ui(self):
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.addSpacing(1)
        self.setLayout(self.layout)
        self.btns = []
        for i in range(self.num):
            btn = DropButtonWidget(idx=i)
            btn.data_signal.connect(self.on_clicked)
            # btn.drop_signal.connect(self.on_drop)
            self.btns.append(btn)
            self.layout.addWidget(btn)


class CustomToolWidget(QWidget):
    """ 多行用户自定义粘贴区域 """
    data_signal = pyqtSignal(object)

    def __init__(self, rows=3):
        super(CustomToolWidget, self).__init__()
        self.rows = rows
        self.widgets = []
        self.init_ui()

    def on_clicked(self, data):
        self.data_signal.emit(data)

    def init_ui(self):
        layout = QVBoxLayout()
        for i in range(self.rows):
            widget = CustomToolRowWidget()
            widget.data_signal.connect(self.on_clicked)
            layout.addWidget(widget)
            self.widgets.append(widget)
        self.setLayout(layout)


class SkillListWidget(QWidget):
    """ 技能列表控件 """
    data_signal = pyqtSignal(object)

    def __init__(self, parent, data, num_per_row=15):
        super().__init__(parent=parent)

        self.buttons = []
        self.data = data
        self.num_per_row = num_per_row
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        for t, sub_list in self.data.items():
            sub_layout = QtWidgets.QHBoxLayout()
            grid_layout = QtWidgets.QGridLayout()  # 一行10个技能
            label = QtWidgets.QLabel(t)
            label.setFixedWidth(60)
            label.setFixedHeight(100)
            sub_layout.addWidget(label)
            sub_layout.addLayout(grid_layout)
            for idx, item in enumerate(sub_list):
                row, col = divmod(idx, self.num_per_row)
                skill_item = DroppableToolButton(name=item['name'],
                                                 type=item['type'],
                                                 image_path=item['image_path'])
                skill_item.clicked.connect(self.btn_clicked)
                grid_layout.addWidget(skill_item, row, col)

            layout.addLayout(sub_layout)
        self.setLayout(layout)

    def btn_clicked(self):
        self.data_signal.emit(self.sender().data)


def get_fake_data(num=10):
    item = {"name": "欢呼", "type": "基础",
            "image_path": r"gift_cola.png"}
    data = {
        "基础": [],
        "标准": [],
        "表演": [],
    }
    for i in range(num):
        new_item = copy.deepcopy(item)
        new_item['name'] = item['name'] + str(i)
        for k, v in data.items():
            v.append(new_item)
    return data


def my_print(d):
    print(f'data:{d}')


def test():
    app = QApplication(sys.argv)
    w = CustomToolWidget()  # 快捷窗
    w.data_signal.connect(my_print)
    s = SkillListWidget(parent=None, data=get_fake_data())  # 技能窗
    s.data_signal.connect(my_print)
    w.show()
    s.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
