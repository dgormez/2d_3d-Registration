from PyQt4 import QtCore, QtGui

class CustomWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent)

        self.thread = RenderThread()
        self.pixmap = QtGui.QPixmap()
        self.pixmapOffset = QtCore.QPoint()
        self.lastDragPos = QtCore.QPoint()

        self.centerX = DefaultCenterX
        self.centerY = DefaultCenterY
        self.pixmapScale = DefaultScale
        self.curScale = DefaultScale

        self.thread.renderedImage.connect(self.updatePixmap)

        self.setWindowTitle("Mandelbrot")
        self.setCursor(QtCore.Qt.CrossCursor)
        self.resize(550, 400)

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
            painter.scale(scaleFactor, scaleFactor)
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

    def resizeEvent(self, event):
        self.thread.render(self.centerX, self.centerY, self.curScale,
                self.size())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Plus:
            self.zoom(ZoomInFactor)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.zoom(ZoomOutFactor)
        elif event.key() == QtCore.Qt.Key_Left:
            self.scroll(-ScrollStep, 0)
        elif event.key() == QtCore.Qt.Key_Right:
            self.scroll(+ScrollStep, 0)
        elif event.key() == QtCore.Qt.Key_Down:
            self.scroll(0, -ScrollStep)
        elif event.key() == QtCore.Qt.Key_Up:
            self.scroll(0, +ScrollStep)
        else:
            super(CustomWidget, self).keyPressEvent(event)

    def wheelEvent(self, event):
        numDegrees = event.delta() / 8
        numSteps = numDegrees / 15.0
        self.zoom(pow(ZoomInFactor, numSteps))

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.lastDragPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.pixmapOffset += event.pos() - self.lastDragPos
            self.lastDragPos = QtCore.QPoint(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pixmapOffset += event.pos() - self.lastDragPos
            self.lastDragPos = QtCore.QPoint()

            deltaX = (self.width() - self.pixmap.width()) / 2 - self.pixmapOffset.x()
            deltaY = (self.height() - self.pixmap.height()) / 2 - self.pixmapOffset.y()
            self.scroll(deltaX, deltaY)

    def updatePixmap(self, image, scaleFactor):
        if not self.lastDragPos.isNull():
            return

        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.pixmapOffset = QtCore.QPoint()
        self.lastDragPosition = QtCore.QPoint()
        self.pixmapScale = scaleFactor
        self.update()

    def zoom(self, zoomFactor):
        self.curScale *= zoomFactor
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale,
                self.size())

    def scroll(self, deltaX, deltaY):
        self.centerX += deltaX * self.curScale
        self.centerY += deltaY * self.curScale
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale,
                self.size())