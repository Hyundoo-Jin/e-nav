import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
import ship_class

class chat_gui(QMainWindow) :
    def __init__(self) :
        super().__init__()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.init_gui()

    def init_gui(self) :
        self.initGUI = initGUI()
        self.setWindowTitle('E-Nav Test')
        self.central_widget.addWidget(self.initGUI)
        self.setGeometry(300, 300, 400, 500)
        self.show()


class initGUI(QWidget) :
    def __init__(self) :
        super().__init__()
        self.mdi = QMdiArea()
        self.lbl1 = QLabel(self)
        image = QPixmap('ship.jpg')
        image = image.scaledToWidth(300)
        image = image.scaledToHeight(150)
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.lbl1.setPixmap(image)

        self.center_btn= QPushButton('센터')
        self.ship_btn = QPushButton('선박')

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.lbl1, 1, 0, 4, 0)
        self.grid.addWidget(self.center_btn, 5, 0)
        self.grid.addWidget(self.ship_btn, 6, 0)

        self.center_btn.clicked.connect(self.center_click)

        self.setLayout(self.grid)
        self.setWindowTitle('E-nav Test')  # 위젯 Title name 설정

    def center_click(self) :
        self.mode = 'center'
        try :
            self.grid.removeWidget(self.lbl1)
            self.lbl1.deleteLater()
            self.grid.removeWidget(self.center_btn)
            self.center_btn.deleteLater()
            self.grid.removeWidget(self.ship_btn)
            self.ship_btn.deleteLater()
        except :
            None

        self.formlayout = QFormLayout()

        self.nameedit = QLineEdit()
        self.callnameedit = QLineEdit()
        self.departureedit = QLineEdit()
        self.destinationedit = QLineEdit()
        self.speededit = QLineEdit()
        self.directionedit = QLineEdit()
        self.latitudeedit = QLineEdit()
        self.longitudeedit = QLineEdit()
        self.etaedit = QLineEdit()

        self.formlayout.addRow(QLabel('<b>선명</b>.'), self.nameedit)
        self.formlayout.addRow(QLabel('<b>호출명</b>'), self.callnameedit)
        self.formlayout.addRow(QLabel('<b>출발지</b>'), self.departureedit)
        self.formlayout.addRow(QLabel('<b>목적지</b>'), self.destinationedit)
        self.formlayout.addRow(QLabel('속도(노트)'), self.speededit)
        self.formlayout.addRow(QLabel('방향'), self.directionedit)
        self.formlayout.addRow(QLabel('위도'), self.latitudeedit)
        self.formlayout.addRow(QLabel('경도'), self.longitudeedit)
        self.formlayout.addRow(QLabel('ETA'), self.etaedit)

        self.grid.addLayout(self.formlayout, 1, 0)

        self.buttonbox = QHBoxLayout()

        accept_btn = QPushButton('적용')
        cancel_btn = QPushButton('취소')

        accept_btn.clicked.connect(self.get_inform)

        self.buttonbox.addWidget(accept_btn)
        self.buttonbox.addWidget(cancel_btn)

        self.grid.addLayout(self.buttonbox, 2, 0)

    def get_inform(self) :
        name = self.nameedit.text()
        callname = self.callnameedit.text()
        departure = self.departureedit.text()
        destination = self.destinationedit.text()
        latitude = self.latitudeedit.text()
        longitude = self.longitudeedit.text()
        eta = self.etaedit.text()

        if not (bool(name.strip()) & bool(callname.strip()) & bool(departure.strip()) & bool(destination.strip())) :
            errormsg = QMessageBox()
            errormsg.setIcon(QMessageBox.Critical)
            errormsg.setText('필요한 정보를 모두 입력해 주십시오.')
            errormsg.setWindowTitle('에러')
            errormsg.setStandardButtons(QMessageBox.Ok)
            errormsg.exec_()
            self.center_click()

        else :
            self.ship = ship_class.Ship(name = name, callname = callname, departure = departure,
                                    destination = destination)
            if bool(latitude) :
                self.ship.lat = latitude
            if bool(longitude) :
                self.ship.long = longitude
            if bool(eta) :
                self.ship.eta = eta
            self.chatting()

    def chatting(self) :
        self.layout()
        chat_ui = uic.loadUi('./chatting.ui')
        sub = QMdiSubWindow()
        temp2 = QLabel()
        sub.setWidget(temp2)
        sub.setWindowTitle('제발')
        self.mdi.addSubWindow(sub)
        sub.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = chat_gui()
    sys.exit(app.exec_())
