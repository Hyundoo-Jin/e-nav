import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication

class Example(QWidget) :
    def __init__(self) :
        super().__init__()

        self.initUI()

    def initUI(self) :
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()     # 한 줄의 텍스트를 넣을 수 있는 텍스트 상자
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()   # 두 줄 이상의 텍스트를 넣을 수 있는 텍스트 상자

        grid = QGridLayout()
        grid.setSpacing(10)   # grid 사이의 공백 넣기

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)   # 다섯 줄 정도 사용하게 하겠음

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
