import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, qApp
from PyQt5.QtCore import QCoreApplication

class Exam(QMainWindow) :   # 메뉴, 상태 표시줄은 widget이 아니라 mainwindow 사용
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.statusBar()
        self.statusBar().showMessage('안녕하세요')

        menu = self.menuBar()
        menu_file = menu.addMenu('File')
        menu_edit = menu.addMenu('Edit')
        menu_view = menu.addMenu('View')

        file_exit = QAction('EXIT', self)
        file_exit.setShortcut('ctrl + Q')
        file_exit.setStatusTip('누르면 영원히 빠이빠이')
        file_exit.triggered.connect(qApp.quit)
        menu_file.addAction(file_exit)

        file_new = QMenu('New', self)
        file_new_txt = QAction('text', self)
        file_new_py = QAction('python', self)

        view_stat = QAction('상태 표시줄', self, checkable = True) # checkable한 menu 추가
        view_stat.setChecked(True)
        view_stat.triggered.connect(self.tglStat)

        file_new.addAction(file_new_py)
        file_new.addAction(file_new_txt)
        menu_file.addMenu(file_new)
        menu_view.addAction(view_stat)

        self.resize(450, 400)
        self.show()

    def tglStat(self, state) :
        if state :
            self.statusBar().show()
        else :
            self.statusBar().hide()

    def contextMenuEvent(self, QContextMenuEvent) :   # 우클릭 했을 때 나타나는 컨텍스트 메뉴 추가하기
        cm = QMenu(self)
        quit = cm.addAction('Quit')
        action = cm.exec_(self.mapToGlobal(QContextMenuEvent.pos())) # mapToGlobal은 어떤 동작이 실행되는 위치(이 경우에는 우클릭한 위치)를 가져오는 함수

        if action == quit :
            qApp.quit()

app = QApplication(sys.argv)
w = Exam()
sys.exit(app.exec_())
