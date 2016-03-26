
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        data1 = ['row1','row2','row3','row4']
        data2 = ['1','2.0','3.00000001','3.9999999']

        self.table.setRowCount(4)

        for index in range(4):
            item1 = QTableWidgetItem(data1[index])
            self.table.setItem(index,0,item1)
            item2 = QTableWidgetItem(data2[index])
            self.table.setItem(index,1,item2)
            self.btn_sell = QPushButton('Edit')
            self.btn_sell.clicked.connect(self.handleButtonClicked)
            self.table.setCellWidget(index,2,self.btn_sell)
        grid = QGridLayout()

        grid.addWidget(self.table,1,0)
        self.setLayout(grid)
        self.show()

    def handleButtonClicked(self):
        button = qApp.focusWidget()
        # or button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())

app = QApplication(sys.argv)
windo=MainWindow()
sys.exit(app.exec_())