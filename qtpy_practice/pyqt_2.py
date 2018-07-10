import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QCoreApplication

class Exam(QWidget) :
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        btn = QPushButton('push me!', self)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        btn.clicked.connect(QCoreApplication.instance().quit)  # 버튼을 누르면 위젯을 종료

        self.resize(500, 500)
        self.setWindowTitle('두 번째 시간')

        self.show()

    def closeEvent(self, QCloseEvent) :
        ans = QMessageBox.question(self, '종료 확인', '종료하시겠습니까?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    # '종료 확인' : 팝업창 제목, '종료하시겠습니까?' : 팝업창 메세지
                    # Yes, No 두 가지 선택지 제공( | 사용), Default로 선택될 선택지
        if ans == QMessageBox.Yes :
            QCloseEvent.accept()
        else :
            QCloseEvent.ignore()
        # Yes 버튼을 눌렀을 때애만 창이 닫히도록 설정(이 코드가 없으면 No를 선택해도 닫힘.)
        

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())
