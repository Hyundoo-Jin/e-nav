import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class Exam(QWidget) :
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        btn = QPushButton('asdcvb', self)  # 위젯에 버튼 추가
        btn.resize(btn.sizeHint())  # 버튼 크기만큼 창 크기 조정
        btn.setToolTip('툴팁입니다.<b>Bold글씨<\b>')  # 버튼 위에 마우스를 올렸을 때 나타나는 툴팁
        btn.move(20, 30)   # 버튼 위치 조정

        self.setGeometry(300, 300, 400, 500)   # 위젯의 크기, 위치 (x, y, 너비, 높이)
        self.setWindowTitle('첫 번째 연습입니다.')  # 위젯 Title name 설정

        self.show()

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())
