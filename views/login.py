#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime

#Import de Modulos
BASE_DIR='..'
sys.path.insert(0,BASE_DIR)
from constants import *

class login_window(QDialog):
	def __init__(self, parent=None):
		super(login_window, self).__init__(parent)

		self.ingresarBoton = QPushButton("Ingresar", self)
		self.cancelarBoton = QPushButton("Cancelar")

		luser = QLabel('User')
		lpassword = QLabel('Password')

		self.editUser = QComboBox() 
		self.editPassword = QLineEdit()
		
		self.db=get_connection()
		cursor=self.db.cursor()
		cursor.execute("select name from Area")
		for row in cursor:
			self.editUser.addItem(row[0])
		self.editPassword.setEchoMode(QLineEdit.Password)

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
		name = str(self.editUser.currentText())
		passwd = str(self.editPassword.text())
		if(passwd==''):
			QMessageBox.warning(self, 'Error',LOGIN_ERROR_NO_PASS_TYPED, QMessageBox.Ok)
		else:
			cursor=self.db.cursor()
			select_pass="select password from Area where name='%s'"%(name)
			cursor.execute(select_pass)
			for row in cursor:
				if(row[0]==passwd):
					self.accept()
				else:
					QMessageBox.warning(self, 'Error',LOGIN_ERROR_BAD_PASS, QMessageBox.Ok)
					self.editPassword.setText('')

	def close_db(self):
		self.db.close()

