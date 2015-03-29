from PyQt4 import QtCore, QtGui
import math

class CustomWidget(QtGui.QWidget):

    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self)
        self.pixmap = QtGui.QPixmap("test.png")
        self.layout = QtGui.QGridLayout(self)
    
        self.label = QtGui.QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label)

        self.altPressed = False
        self.middlePressed = False
        self.rightPressed = False
        self.scale = 1

        DefaultScale = 1
        self.pixmapScale = DefaultScale
        self.curScale = DefaultScale
        self.pixmapOffset = QtCore.QPoint()

        self.setFocusPolicy(QtCore.Qt.WheelFocus)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.black)

        if self.pixmap.isNull():
            painter.setPen(QtCore.Qt.white)
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter,
                    "Rendering initial image, please wait...")
            return

        if self.curScale == self.pixmapScale:
            painter.drawPixmap(self.pixmapOffset, self.pixmap)
        else:
            scaleFactor = self.pixmapScale / self.curScale
            newWidth = int(self.pixmap.width() * scaleFactor)
            newHeight = int(self.pixmap.height() * scaleFactor)
            newX = self.pixmapOffset.x() + (self.pixmap.width() - newWidth) / 2
            newY = self.pixmapOffset.y() + (self.pixmap.height() - newHeight) / 2

            painter.save()
            painter.translate(newX, newY)
            painter.scale(2, 2)
            exposed, _ = painter.matrix().inverted()
            exposed = exposed.mapRect(self.rect()).adjusted(-1, -1, 1, 1)
            painter.drawPixmap(exposed, self.pixmap, exposed)
            painter.restore()

        text = "Use mouse wheel or the '+' and '-' keys to zoom. Press and " \
                "hold left mouse button to scroll."
        metrics = painter.fontMetrics()
        textWidth = metrics.width(text)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 127))
        painter.drawRect((self.width() - textWidth) / 2 - 5, 0, textWidth + 10,
                metrics.lineSpacing() + 5)
        painter.setPen(QtCore.Qt.white)
        painter.drawText((self.width() - textWidth) / 2,
                metrics.leading() + metrics.ascent(), text)


    def wheelEvent(self, event):
        #self.newScale(event.delta(), 1.15)
        x = event.delta()
        self.scale += 1 * math.copysign(1, x)
        print ("Wheel Event")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Alt:
            self.altPressed = True
            QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Alt:
            self.altPressed = False
            Qt.QApplication.setOverrideCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        self._dragPos = event.pos()
        if event.button() == QtCore.Qt.MidButton:
            self.middlePressed = True
        if event.button() == QtCore.Qt.RightButton:
            self.rightPressed = True

        print "mouse Pressed"

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            self.middlePressed = False
        if event.button() == QtCore.Qt.RightButton:
            self.rightPressed = False

        print "mouse Release"

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

        print "mouse Move"

    def newScale(self, operator, factor):
        if operator > 0:
            self.pixmap.scaled(factor, factor,transformMode=QtCore.Qt.SmoothTransformation)
        if operator < 0:
            self.pixmap.scaled(1.0/factor, 1.0/factor,transformMode=QtCore.Qt.SmoothTransformation)

        print "In new Scale"

    def zoomIn(self):
        """Zoom in on image."""
        self.scaleImage(self._zoomFactorDelta)

    def zoomOut(self):
        """Zoom out on image."""
        self.scaleImage(1 / self._zoomFactorDelta)

    def scaleImage(self, factor, combine=True):
        """Scale image by factor.

        :param float factor: either new :attr:`zoomFactor` or amount to scale
                             current :attr:`zoomFactor`

        :param bool combine: if ``True`` scales the current
                             :attr:`zoomFactor` by factor.  Otherwise
                             just sets :attr:`zoomFactor` to factor"""
        if not self._pixmapItem.pixmap():
            return

        if combine:
            self.zoomFactor = self.zoomFactor * factor
        else:
            self.zoomFactor = factor


