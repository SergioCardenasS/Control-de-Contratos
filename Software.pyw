#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#Import de Modulos
BASE_DIR='DATA'
sys.path.insert(0,BASE_DIR)
from constants import *
from views import login
from views.control import control_view
from views.abastecimientos import abastecimiento_view
from views.comercial import comercial_view
from views.desarrollo import desarrollo_view
from views.ingenieria import ingenieria_view
from views.planificacion import planificacion_view
from views.logistica import logistica_avios_view
from views.calidad import calidad_avios_view

def main():
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon('icon.png'))
	Login = login.login_window()
	if Login.exec_() == QDialog.Accepted:
		Login.close_db()
		actual_id=Login.get_actual_id()
		window = None
		if(actual_id==AREA_CONTROL_ID):
			window = control_view.control_window()
		elif(actual_id==AREA_COMERCIAL_ID):
			window = comercial_view.comercial_window()
		elif(actual_id==AREA_ABASTECIMIENTOS_ID):
			window = abastecimiento_view.abastecimiento_window()
		elif(actual_id==AREA_DESARROLLO_ID):
			window = desarrollo_view.desarrollo_window()
		elif(actual_id==AREA_INGENIERIA_ID):
			window = ingenieria_view.ingenieria_window()
		elif(actual_id==AREA_PLANIFICACION_ID):
			window = planificacion_view.planificacion_window()
		elif(actual_id==AREA_LOGISTICA_ID):
			window = logistica_avios_view.logistica_window()
		elif(actual_id==AREA_CALIDAD_ID):
			window = calidad_avios_view.calidad_window()
		else:
			return
		screenGeometry = QApplication.desktop().availableGeometry()
		window.resize(screenGeometry.width(), screenGeometry.height())
		window.showMaximized()
		app.exec_()
	Login.close_db()

if __name__ == '__main__':
	main()

