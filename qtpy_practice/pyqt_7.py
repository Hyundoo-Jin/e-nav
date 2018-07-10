import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication

class Example(QWidget) :
    def __init__(self) :
        super().__init__()

        self.initUI()

    def initUI(self) :
        lcd = QLCDNumber(self)   # LCD화면의 숫자 표현(위젯)
        sld = QSlider(Qt.Horizontal, self)   # 진행 슬라이더

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)   # 개채 배치하기

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)   # QLCDNumber에 있는 display 함수와 sld 슬라이더를 연결시킴

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('signal and slot')
        self.show()

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
