import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
import ParryCD


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JadeWoken")
        self.setGeometry(100, 100, 800, 600) 
        self.setWindowIcon (QIcon("BigheadJaden.jpg"))
        self.initUi()
        
        label = QLabel("JadeWoken", self)
        label.setStyleSheet('font-size: 30px')
        label.setGeometry(310, 10, 200, 200)

        me = QLabel(self)
        me.setGeometry(300, 200, 200, 200)
        me.setPixmap(QPixmap("BigheadJaden.jpg"))
        me.setScaledContents(True)
        
    def initUi(self):
        bton = QPushButton("Toggle Parry CD", self)
        bton.setGeometry(150, 200, 100, 75)
        bton.setStyleSheet('font-size: 10px')
        bton.clicked.connect(ParryCD.overlay)
        
        



def test():
    print('working')

def main():
    app = QApplication(sys.argv)
    wdw = MainWindow()
    wdw.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()