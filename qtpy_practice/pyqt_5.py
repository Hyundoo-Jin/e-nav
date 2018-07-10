import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QHBoxLayout, QVBoxLayout

class Example(QWidget) :
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        lbl1 = QLabel('Zetcode', self)  # Label 레이아웃 추가. move는 x좌표, y좌표를 통해 위치 조정
        lbl1.move(15, 10)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for programmers', self)
        lbl3.move(55, 70)

        okbutton = QPushButton('Ok')
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()  # 가로 상자
        hbox.addStretch(1)   # 안 쪽 여백 크기
        hbox.addWidget(okbutton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
