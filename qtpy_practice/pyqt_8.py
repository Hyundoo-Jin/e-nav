import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication

class Example(QWidget) :
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()

    def keyPressEvent(self, e) :   # 함수를 정의. keyPressEvent라는 함수가 이미 존재, 재정의
        if e.key() == Qt.Key_Escape :   # Escape키가 눌렸을 때 close()함수를 수행
            self.close()

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
