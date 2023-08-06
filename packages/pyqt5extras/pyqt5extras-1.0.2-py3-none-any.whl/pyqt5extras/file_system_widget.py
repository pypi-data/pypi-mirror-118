#!/usr/bin/env python
# coding=utf-8
# @Time    : 2021/8/26 16:09
# @Author  : 江斌
# @Software: PyCharm
import os
import sys
from PyQt5 import QtGui, QtWidgets, QtCore


class FileSystemTreeWidget(QtWidgets.QTreeView):
    """ 系统文件列表框。
        1. 双击文件/文件夹，打开文件/文件夹；
        2. 右键菜单：a.复制文件路径；b.打开文件目录。
    """

    def __init__(self, parent=None, use_default_slot=True):
        """
        :param parent:
        :param use_default_slot: 使用默认槽函数。
        """
        super(FileSystemTreeWidget, self).__init__(parent)
        self.use_default_slot = use_default_slot
        self.widget_name = 'FileTree'
        self.__model = QtWidgets.QFileSystemModel(self)
        self.__model.setRootPath(QtCore.QDir.rootPath())
        self.setModel(self.__model)

        self.cur_item = None
        self.init_ui()
        if use_default_slot:
            self.connect_signal()

    def init_ui(self):
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 60)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.setAcceptDrops(True)

    def get_current_item(self):
        return self.cur_item

    def set_root_dir(self, path):
        """ 设置根目录。 """
        self.setRootIndex(self.__model.index(path))
        self.setWindowTitle(f'{self.widget_name}:{path}')

    def connect_signal(self):
        self.customContextMenuRequested.connect(self.create_menu)
        self.clicked.connect(self.on_clicked)
        self.doubleClicked.connect(self.on_double_clicked)

    def on_clicked(self):
        """ 双击事件。 use_default_slot=True时启用。"""
        index = self.currentIndex()
        model = index.model()
        self.cur_item = model.filePath(index)

    def on_double_clicked(self):
        """ 双击打开文件/目录。 use_default_slot=True时启用。"""
        os.startfile(self.cur_item)

    def create_menu(self, pos):
        """ create context menu. use_default_slot=True时启用。 """
        menu = QtWidgets.QMenu(self)
        open_action = menu.addAction("打开文件目录...")
        copy_action = menu.addAction("复制文件路径...")
        open_action.triggered.connect(self.open_current_dir)
        copy_action.triggered.connect(self.copy_path)
        menu.exec_(self.mapToGlobal(pos))

    def open_current_dir(self):
        """ 打开当前文件所在目录。 """
        d = self.cur_item if os.path.isdir(self.cur_item) else os.path.dirname(self.cur_item)
        os.startfile(d)

    def copy_path(self):
        """ 复制当前文件路径。"""
        clipboard = QtWidgets.QApplication.clipboard()
        print(type(self.cur_item))
        clipboard.setText(self.cur_item)

    def dragEnterEvent(self, e):
        """ 允许用户拖动一个目录到该窗口。
        when drag a directory in to the widget, change the root dir to this directory."""
        mime_data = e.mimeData()
        if mime_data.hasUrls:
            url = mime_data.urls()[0].toLocalFile()
            d = os.path.dirname(url) if os.path.isfile(url) else url
            if os.path.isdir(d):
                self.set_root_dir(d)
            e.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    asset = FileSystemTreeWidget(use_default_slot=True)
    asset.set_root_dir(r"C:\users")
    asset.set_root_dir(r"D:\data\Retarget")
    asset.show()

    sys.exit(app.exec_())
