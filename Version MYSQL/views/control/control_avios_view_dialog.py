#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from controllers.controller_contract import *
from controllers.controller_process import *
from views import comments

class control_avios_view_dialog(QDialog):
	def __init__(self, parent=None):
		super(control_avios_view_dialog, self).__init__(parent)
		#Dar tamano a la pantalla
		size=self.size()
		self.resize(3*size.width()/2,size.height())
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)-(size.height()/2)
		left=(desktopSize.width()/2)-(size.width()/2)
		self.move(left, top)
		#Creacion de conexion a BD
		#abrimos el creador de la pantalla
		self.pantallasCreador()
		self.setWindowTitle(TITLE_APP+CONTROL_AVIOS_TITLE)
		self.show()
		self.control_singleton=False

	def pantallasCreador(self):
		print "hey"