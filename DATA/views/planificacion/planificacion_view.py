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
from controllers.controller_contract import *
from controllers.controller_process import *
from views.planificacion import planificacion_fin_process
from views.control import control_view_dialog

class planificacion_window(QWidget):
	def __init__(self):
		super(planificacion_window, self).__init__()
		#Dar tamano a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height())-(size.height())
		left=(desktopSize.width())-(size.width())
		self.move(left, top)
		#abrimos la pantalla princilal para todas las areas
		self.pantallaDesarrollo()
		self.setWindowTitle(TITLE_APP+PLANIFICACION_TITLE)
		self.show()
		self.control_singleton=False
		self.admin_singleton=False

	def time_event(self):
		if(self.control_singleton==False):
			self.refresh_table(AREA_PLANIFICACION_ID)

	def closeEvent(self,event):
		self.timer.stop()

	def pantallaDesarrollo(self):
		#TEMPORIZADOR
		self.timer = QTimer()
		self.connect(self.timer, SIGNAL("timeout()"), self.time_event)
		self.timer.start(TIMER_EVENT)
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
		#Numero de items o filas
		self.rows = 0
		self.stringRow = ''
		#Creamos las columnas
		self.tabla.setColumnCount(SIZE_COLUMNS)
		self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS).split(SPLIT))
		#Por ahora solo creamos el numero de filas o items
		self.tabla.setRowCount(self.rows)

		#Estas variables son para darle un tamano dependiendo del texto pero solo para las columnas
		header = self.tabla.horizontalHeader()
		header.setResizeMode(QHeaderView.Stretch)

		#Ahora creamos dicha filas de numeros o ids
		self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))

		#Crearemos un grid ponde estaran todos nuestro widgets
		grid = QGridLayout()

		#Instaciamos botones
		aceptar_button = QPushButton('Actualizar', self)
		undoicon = QIcon.fromTheme("view-refresh")
		aceptar_button.setIcon(undoicon)
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
		self.refresh_table(AREA_PLANIFICACION_ID)

	def Actualizar(self):
		if(self.control_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
		else:
			self.control_singleton=True
			self.refresh_table(AREA_PLANIFICACION_ID)
			self.control_singleton=False

	def LimpiarTabla(self):
		self.tabla.clear();
		self.tabla.setRowCount(0);
		self.tabla.setColumnCount(SIZE_COLUMNS)
		self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS).split(SPLIT))

	def refresh_table(self,AREA_ID):
		self.LimpiarTabla()
		#Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
		db=get_connection()
		self.listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ID))
		db.close()
		numEventos = self.rows
		#Guardamos el nuevo tamano de items
		self.rows = len(self.listaContratos)
		self.tabla.setRowCount(self.rows)
		#Este size hara los id o filas en string
		stringRow = ''
		#Ahora nuevamente sacamos todos los elementos
		for numContratos in range(len(self.listaContratos)):
			#De esa forma actualizaremos
			self.tabla.setItem(numContratos,0, QTableWidgetItem(self.listaContratos[numContratos].purchase_order))
			self.tabla.setItem(numContratos,1, QTableWidgetItem(self.listaContratos[numContratos].contract_number))
			self.tabla.setItem(numContratos,2, QTableWidgetItem(self.listaContratos[numContratos].special_contract))
			self.tabla.setItem(numContratos,3, QTableWidgetItem(get_str_name_from_id_process(self.listaContratos[numContratos].id_process)))
			self.tabla.setItem(numContratos,4, QTableWidgetItem(get_str_contract_type(self.listaContratos[numContratos].contract_type)))
			self.tabla.setItem(numContratos,5, QTableWidgetItem(str(self.listaContratos[numContratos].init_date)))
			self.tabla.setItem(numContratos,6, QTableWidgetItem(str(self.listaContratos[numContratos].mod_date)))
			if (time_pass_one_day(str(self.listaContratos[numContratos].mod_date))):
				self.tabla.item(numContratos, 6).setBackground(QColor(238,0,0))
			else:
				self.tabla.item(numContratos, 6).setBackground(QColor(0,205,0))
			self.tabla.item(numContratos, 6).setTextColor(QColor(255, 255, 255))
			self.tabla.setItem(numContratos,7, QTableWidgetItem(str(self.listaContratos[numContratos].iteration_number)))
			self.btn_sell = QPushButton('Finalizar')
			self.btn_sell.clicked.connect(self.Finalizar)
			self.tabla.setCellWidget(numContratos,8,self.btn_sell)
			stringRow = stringRow + str(numContratos+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

	def Finalizar(self):
		if(self.control_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
		else:
			self.control_singleton=True
			button = qApp.focusWidget()
			index = self.tabla.indexAt(button.pos())
			if index.isValid():
				ventana = planificacion_fin_process.FinishProcessSetDate(contract=self.listaContratos[index.row()]).exec_()
				self.refresh_table(AREA_PLANIFICACION_ID)
			self.control_singleton=False

	def open_admin_button(self):
		if(self.admin_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_ADMIN_OPENED, QMessageBox.Ok)
		else:
			self.admin_singleton=True
			window=control_view_dialog.control_window_dialog().exec_()
			self.admin_singleton=False
