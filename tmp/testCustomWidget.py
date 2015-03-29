from PyQt4 import QtCore, QtGui
import math


class MyQGraphicsView(QtGui.QGraphicsView):
    def __init__(self,parent = None):
        QtGui.QGraphicsView.__init__(self)
        #super(MyQGraphicsView, self).mouseMoveEvent(event)
        self.path = "test.png"

        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.setRenderHints(QtGui.QPainter.Antialiasing)
        self.altPressed = False
        self.middlePressed = False
        self.rightPressed = False

        self.pixmap = QtGui.QPixmap()
        self.pixmap.load(self.path)
        self.pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation)
        self.graphicsPixmapItem = QtGui.QGraphicsPixmapItem(self.pixmap)

        self.graphicsScene = QtGui.QGraphicsScene()
        self.graphicsScene.addItem(self.graphicsPixmapItem)

        self.setScene(self.graphicsScene)


    def wheelEvent(self, event):
        self.newScale(event.delta(), 1.15,)

    def mousePressEvent(self, event):
        self._dragPos = event.pos()
        if event.button() == QtCore.Qt.MidButton:
            self.middlePressed = True
        if event.button() == QtCore.Qt.RightButton:
            self.rightPressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self.middlePressed = False
        if event.button() == QtCore.Qt.RightButton:
            self.rightPressed = False

    def mouseMoveEvent(self, event):
        if self.altPressed:
            newPos = event.pos()

            if self.middlePressed:
                diff = newPos - self._dragPos
                self._dragPos = newPos
                QApplication.setOverrideCursor(Qt.ClosedHandCursor)
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
                event.accept()
            if self.rightPressed:
                diff = newPos - self._dragPos
                self._dragPos = newPos
                QApplication.setOverrideCursor(Qt.SizeAllCursor)
                self.newScale(diff.x(), 1.01)

    def newScale(self, operator, factor):
        if operator > 0:
            self.scale(factor, factor)
        if operator < 0:
            self.scale(1.0/factor, 1.0/factor)
