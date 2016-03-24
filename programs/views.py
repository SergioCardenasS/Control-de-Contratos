#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from dateutil.tz import tzlocal
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime, timedelta, date


class ventanaPrincial(QWidget):
  	def __init__(self):
  		super(ventanaPrincial, self).__init__()
  		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height())-(size.height())
		left=(desktopSize.width())-(size.width())
		self.move(left, top)
  		self.setWindowTitle('ventanaPrincial')
  		self.show()



class ventanaLogin(QDialog):
	def __init__(self, parent=None):
		super(ventanaLogin, self).__init__(parent)

		self.ingresarBoton = QPushButton("Ingresar", self)
		self.cancelarBoton = QPushButton("Cancelar")

		luser = QLabel('User')
		lpassword = QLabel('Password')

		self.editUser = QLineEdit() 
		self.editPassword = QLineEdit()

		grid = QGridLayout()
			
		grid.addWidget(luser,1,0)
		grid.addWidget(self.editUser,1,1)

		grid.addWidget(lpassword,2,0)
		grid.addWidget(self.editPassword,2,1)

		grid.addWidget(self.ingresarBoton,3,1)
		grid.addWidget(self.cancelarBoton,3,2)

		self.setLayout(grid)

		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)-(size.height()/2)
		left=(desktopSize.width()/2)-(size.width()/2)
		self.move(left, top)
		self.setWindowTitle('Login')
		self.show()

		self.cancelarBoton.clicked.connect(self.close)
		self.connect(self.ingresarBoton, SIGNAL("clicked()"), self.Ingresar)

	def Ingresar(self):
		#Validar user y password
		self.accept()
		

def main():
  app = QApplication(sys.argv)
  login = ventanaLogin()
  if login.exec_() == QDialog.Accepted:
  	window = ventanaPrincial()
  	screenGeometry = QApplication.desktop().availableGeometry()
  	window.resize(screenGeometry.width(), screenGeometry.height())
  	window.showMaximized()
  	sys.exit(app.exec_())


if __name__ == '__main__':
  main()  