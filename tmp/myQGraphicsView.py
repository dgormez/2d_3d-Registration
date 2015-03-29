import sys
from PyQt4 import QtGui, QtCore



class CustomWidget(QtGui.QWidget):

    def __init__(self,parent = None):
        super(CustomWidget, self).__init__(parent)
        #QWidget.__init__(self, parent)
        #self.setFocusPolicy(Qt.WheelFocus)
        #self.setRenderHints(QPainter.Antialiasing)
        self.altPressed = False
        self.middlePressed = False
        self.rightPressed = False

        self.initUI()
    
    def paintEvent(self, ev):
        p = QPainter(self)

    def initUI(self):
        pixmap = QtGui.QPixmap("test.png")
        pixItem = QtGui.QGraphicsPixmapItem(pixmap)

    def wheelEvent(self, event):
        self.newScale(event.delta(), 1.15)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.altPressed = True
            QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.altPressed = False
            QApplication.setOverrideCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        self._dragPos = event.pos()
        if event.button() == Qt.MidButton:
            self.middlePressed = True
        if event.button() == Qt.RightButton:
            self.rightPressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MidButton:
            self.middlePressed = False
        if event.button() == Qt.RightButton:
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