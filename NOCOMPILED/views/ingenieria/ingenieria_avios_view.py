#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import contract, comment
from controllers import controller_process_avios, controller_avios, controller_contract
from views.ingenieria import ingenieria_avios_fin_process
from views.control import control_view_dialog
from views.control import control_avios_view_dialog

class ingenieria_window(QDialog):
	def __init__(self,parent=None):
		super(ingenieria_window, self).__init__(parent)
		#Dar tamano a la pantalla
		self.pantalla()
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=2*(desktopSize.height())/3
		left=3*(desktopSize.width())/4
		self.resize(left, top)
		#abrimos la pantalla princilal para todas las areas
		self.setWindowTitle(TITLE_APP+AVIOS_TITLE+INGENIERIA_TITLE)
		self.show()
		self.control_singleton=False
		self.admin_singleton=False

	def time_event(self):
		if(self.control_singleton==False):
			self.refresh_table(AREA_INGENIERIA_ID)

	def closeEvent(self,event):
		self.timer.stop()

	def pantalla(self):
		#TEMPORIZADOR
		self.timer = QTimer()
		self.connect(self.timer, SIGNAL("timeout()"), self.time_event)
		self.timer.start(TIMER_EVENT)
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
		#Numero de items o filas
		self.rows = 0
		#Creamos las columnas
		self.tabla.setColumnCount(SIZE_COLUMNS_AVIOS)
		self.tabla.setHorizontalHeaderLabels(AVIOS_TABLE_LIST)
		#Por ahora solo creamos el numero de filas o items
		self.tabla.setRowCount(0)

		#Estas variables son para darle un tamano dependiendo del texto pero solo para las columnas
		header = self.tabla.horizontalHeader()
		header.setResizeMode(QHeaderView.Stretch)

		#Ahora creamos dicha filas de numeros o ids
		self.tabla.setVerticalHeaderLabels([""])

		#Crearemos un grid ponde estaran todos nuestro widgets
		grid = QGridLayout()

		#Instaciamos botones
		aceptar_button = QPushButton('Actualizar', self)
		admin_button = QPushButton('Ver Status General',self)

		#Le damos funcionalidades a cada boton
		self.connect(aceptar_button, SIGNAL("clicked()"), self.Actualizar)
		self.connect(admin_button, SIGNAL("clicked()"), self.open_admin_button)

		#Le damos posicion a nuestros botones
		aceptar_button.move(400,550)
		admin_button.move(400,550)

		#Ahora le damos un tamano a nuestros botones
		aceptar_button.setFixedSize(150, 110)
		admin_button.setFixedSize(150,110)

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(6)
		grid.setVerticalSpacing(5)

		#Agregamos los widgets al grid
		grid.addWidget(aceptar_button,5,3)
		grid.addWidget(admin_button,5,5)
		grid.addWidget(self.tabla,1,0,3,9)

		#Por ultimo agregamos todo el Layout con todos nuestros widgets
		self.setLayout(grid)
		self.refresh_table(AREA_INGENIERIA_ID)

	def Actualizar(self):
		if(self.control_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
		else:
			self.control_singleton=True
			self.refresh_table(AREA_INGENIERIA_ID)
			self.control_singleton=False

	def LimpiarTabla(self):
		self.tabla.clear();
		self.tabla.setRowCount(0);
		self.tabla.setColumnCount(SIZE_COLUMNS_AVIOS)
		self.tabla.setHorizontalHeaderLabels(AVIOS_TABLE_LIST)

	def refresh_table(self,AREA_ID):
		self.LimpiarTabla()
		#Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
		db=get_connection()
		self.listaAvios = controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_ID))
		numEventos = self.rows
		#Guardamos el nuevo tamano de items
		self.rows = len(self.listaAvios)
		self.tabla.setRowCount(self.rows)
		#Este size hara los id o filas en string
		stringRow = ''
		#Ahora nuevamente sacamos todos los elementos
		for index in range(len(self.listaAvios)):
			#De esa forma actualizaremos
			actual_contract = controller_contract.get_contracts_by_id(db,self.listaAvios[index].id_contract)
			if(actual_contract):
				self.tabla.setItem(index,0, QTableWidgetItem(actual_contract.purchase_order))
				self.tabla.setItem(index,1, QTableWidgetItem(actual_contract.contract_number))
				self.tabla.setItem(index,2, QTableWidgetItem(actual_contract.special_contract))
				self.tabla.setItem(index,3, QTableWidgetItem(get_str_name_from_id_process_avios(self.listaAvios[index].id_process)))
				self.tabla.setItem(index,4, QTableWidgetItem(str(self.listaAvios[index].init_date)))
				self.tabla.setItem(index,5, QTableWidgetItem(str(self.listaAvios[index].mod_date)))
				if (time_pass_one_day(str(self.listaAvios[index].mod_date))):
					self.tabla.item(index, 5).setBackground(QColor(238,0,0))
				else:
					self.tabla.item(index, 5).setBackground(QColor(0,205,0))
				self.tabla.item(index, 5).setTextColor(QColor(255, 255, 255))
				self.tabla.setItem(index,6, QTableWidgetItem(str(self.listaAvios[index].llegada_date)))
				self.btn_sell = QPushButton('Finalizar')
				self.btn_sell.clicked.connect(self.Finalizar)
				self.tabla.setCellWidget(index,7,self.btn_sell)
				stringRow = stringRow + str(index+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))
		db.close()

	def Finalizar(self):
		if(self.control_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
		else:
			self.control_singleton=True
			button = qApp.focusWidget()
			index = self.tabla.indexAt(button.pos())
			if index.isValid():
				if(self.listaAvios[index.row()].id_process==PROCESS_AVIOS_FIN_ING_ID):
					ventana = ingenieria_avios_fin_process.FinishIngenieriaAvios(s_avios=self.listaAvios[index.row()]).exec_()
				self.refresh_table(AREA_INGENIERIA_ID)
			self.control_singleton=False

	def open_admin_button(self):
		if(self.admin_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_ADMIN_OPENED, QMessageBox.Ok)
		else:
			self.admin_singleton=True
			window=control_view_dialog.control_window_dialog().exec_()
			self.admin_singleton=False
