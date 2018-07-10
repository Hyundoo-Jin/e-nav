import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu
from PyQt5.QtCore import QCoreApplication

class Exam(QMainWindow) :   # 메뉴, 상태 표시줄은 widget이 아니라 mainwindow 사용
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.statusBar()  # 상태 표시줄 추가
        self.statusBar().showMessage('안녕하세요')  # 상태 표시줄에 메세지 띄우기

        menu = self.menuBar()  # 메뉴바 추가
        menu_file = menu.addMenu('File')  # 'File'이라는 이름의 메뉴 추가
        menu_edit = menu.addMenu('Edit')

        file_exit = QAction('EXIT', self)  # 메뉴 객체 지정
        file_exit.setShortcut('ctrl + Q')  # 단축키 설정
        file_exit.setStatusTip('누르면 영원히 빠이빠이')
        file_exit.triggered.connect(QCoreApplication.instance().quit)
        menu_file.addAction(file_exit)  # 만들어진 객체를 그룹에 추가

        file_new = QMenu('New', self)  # 그룹 안의 액션그룹 만들기
        file_new_txt = QAction('text', self)  # 만들어진 액션그룹 안에 액션 추가
        file_new_py = QAction('python', self)
        file_new.addAction(file_new_py)  # 액션 추가하기
        file_new.addAction(file_new_txt)
        menu_file.addMenu(file_new)  # 만들어진 객체 그룹에 추가

        self.resize(450, 400)
        self.show()

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())
