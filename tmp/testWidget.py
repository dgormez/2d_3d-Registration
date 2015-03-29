import sys,os
from PyQt4 import QtGui, QtCore


class TestWidget(QWidget):

    def __init__(self, *args):
        apply(QWidget.__init__, (self,) + args)
        self.setGeometry(10, 10, 50, 250)
        self.pixmap = TypoGraph(0, self.width(), self.height())
        self.timer = self.startTimer(100)

    def paintEvent(self, ev):
        bitBlt(self, 0, 0, self.pixmap, 0, 0, self.width(), self.height())

    def timerEvent(self, ev):
        self.pixmap.update(whrandom.randrange(0, 300))
        bitBlt(self, 0, 0, self.pixmap, 0, 0, self.width(), self.height())

if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL('lastWindowClosed()'),a,SLOT('quit()'))
    w = TestWidget()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()