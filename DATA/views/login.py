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
from controllers import controller_area

class login_window(QDialog):
	def __init__(self, parent=None):
		super(login_window, self).__init__(parent)

		self.ingresarBoton = QPushButton("Ingresar", self)
		self.cancelarBoton = QPushButton("Salir")

		luser = QLabel('Area')
		lpassword = QLabel('Password')

		self.editUser = QComboBox() 
		self.editPassword = QLineEdit()
		
		self.db=get_connection()
		self.db_connected=True
		area_list=controller_area.get_all_areas(self.db)
		for area_element in area_list:
			self.editUser.addItem(area_element.name)
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
		top=(desktopSize.height()/2)-(size.height()/4)
		left=(desktopSize.width()/2)-(size.width()/4)
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
			actual_area=controller_area.get_area_by_name(self.db,name)
			if(actual_area.password==passwd):
				self.actual_id=actual_area.id_area
				self.accept()
			else:
				QMessageBox.warning(self, 'Error',LOGIN_ERROR_BAD_PASS, QMessageBox.Ok)
				self.editPassword.setText('')

	def get_actual_id(self):
		return self.actual_id
	def close_db(self):
		if(self.db_connected):
			self.db_connected=False
			self.db.close()
