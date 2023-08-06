#!/usr/bin/env python
# coding=utf-8
# @Time    : 2021/8/25 18:59
# @Author  : 江斌
# @Software: PyCharm
import sys
from pyqt5extras.imagebox import ImageBox
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap, QMovie, QImage, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint


class ImageToolTip(ImageBox):
    def __init__(self, image=None, text='', text_size=15, text_height=15, parent=None, keepAspectRatio=True):
        super(ImageToolTip, self).__init__(parent=parent, source=image, keepAspectRatio=keepAspectRatio)
        self.hoverBackground = QColor(245, 245, 250)
        self.borderColor = QColor(245, 245, 250)  # QColor(190, 190, 190)
        self.textColor = QColor(190, 190, 190)  # QColor(190, 190, 190)
        self.borderWidth = 3
        self.borderRadius = 3
        self.tip_size = 25

        self.image = image
        self.text = text
        self.text_height = text_height
        self.text_size = text_size
        self.setContentsMargins(0, 0, 0, text_height + self.tip_size)
        self.installEventFilter(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(QtCore.Qt.WindowModal)

    def paintEvent(self, event):
        pt = QPainter()
        pt.begin(self)
        pt.setRenderHint(QPainter.Antialiasing, on=True)

        pen = QPen(self.borderColor, self.borderWidth, Qt.SolidLine, Qt.RoundCap)
        pt.setPen(pen)
        brush = QBrush(self.hoverBackground)
        pt.setBrush(brush)
        pt.drawRoundedRect(self.borderWidth, self.borderWidth, self.width() - 3,
                           self.height() - 25, self.borderRadius, self.borderRadius)
        w = self.width()
        h = self.height() - self.tip_size
        # 2----1
        #  \3/
        points = [
            QPoint(w, h),  # 1
            QPoint(w, h) + QPoint(int(-self.tip_size * 1.5), 0),  # 2
            QPoint(w, h) + QPoint(int(-self.tip_size * 0.5), int(self.tip_size * 0.9)),  # 3
            QPoint(w, h),  # 1
        ]
        pt.drawPolygon(QtGui.QPolygon(points), 4)
        pt.end()

        super(ImageToolTip, self).paintEvent(event)

        pt.begin(self)
        if self.text:
            font = QtGui.QFont('Serif', self.text_size, QtGui.QFont.Light)
            pen = QPen(self.textColor, self.borderWidth, Qt.SolidLine, Qt.RoundCap)
            pt.setFont(font)
            pt.setPen(pen)
            pt.drawText(10, int(self.height() - self.tip_size), self.text)
        pt.end()

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.close()
        return False


def test():
    app = QtWidgets.QApplication(sys.argv)
    b = ImageToolTip(image=r"https://www.baidu.com/img/flexible/logo/pc/result.png",
                     text='图: QQ截图20200729134257.png')
    b.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
