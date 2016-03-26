#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#Import de Modulos
BASE_DIR='..'
sys.path.insert(0,BASE_DIR)
from constants import *
from views import login
from views.control import control_view

def main():
	app = QApplication(sys.argv)
	Login = login.login_window()
	if Login.exec_() == QDialog.Accepted:
		Login.close_db()
		actual_id=Login.get_actual_id()
		window = None
		if(actual_id==AREA_CONTROL_ID):
			window = control_view.control_window()
		else:
			return
		screenGeometry = QApplication.desktop().availableGeometry()
		window.resize(screenGeometry.width(), screenGeometry.height())
		window.showMaximized()
		app.exec_()
	Login.close_db()

if __name__ == '__main__':
	main()

