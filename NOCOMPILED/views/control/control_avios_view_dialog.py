#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
import control_view
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from controllers import controller_contract,controller_avios,controller_process_avios
from views import comments_avios

class control_avios_view_dialog(QDialog):
	def __init__(self, parent=None):
		super(control_avios_view_dialog, self).__init__(parent)
		#Dar tamano a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)-(size.height()/2)
		left=(desktopSize.width()/2)-(size.width())
		self.move(left, top)
		#Creacion de conexion a BD
		#abrimos el creador de la pantalla
		self.pantallasCreador()
		self.setWindowTitle(TITLE_APP+CONTROL_AVIOS_TITLE)
		self.show()
		self.Refresh_Numbers()
		self.control_singleton=False

	def pantallasCreador(self):
		self.listaAvios=[]
		self.AREA_ACTUAL_ID=AREA_DESARROLLO_ID
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.rows = 0
		self.stringRow = ''
		#Creamos las columnas
		self.tabla.setColumnCount(SIZE_COLUMNS_AVIOS)
		self.tabla.setHorizontalHeaderLabels(AVIOS_TABLE_LIST)
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
		self.desarrollo_button = QPushButton('Desarrollo', self)
		self.ingenieria_button = QPushButton('Ingenieria', self)
		self.logistica_button = QPushButton('Logistica', self)
		self.calidad_button = QPushButton('Control de Calidad', self)

		refresh_button = QPushButton('Actualizar', self)
		finish_button = QPushButton('Contratos Finalizados', self)
		search_button = QPushButton('Buscar Contrato', self)

		#Le damos funcionalidades a cada boton
		self.connect(refresh_button, SIGNAL("clicked()"), self.Actualizar)
		self.connect(self.desarrollo_button, SIGNAL("clicked()"), self.tablaDesarrollo)
		self.connect(self.ingenieria_button, SIGNAL("clicked()"), self.tablaIngenieria)
		self.connect(self.logistica_button, SIGNAL("clicked()"), self.tablaLogistica)
		self.connect(self.calidad_button, SIGNAL("clicked()"), self.tablaCalidad)
		self.connect(finish_button, SIGNAL("clicked()"), self.tablaFinalizados)
		self.connect(search_button, SIGNAL("clicked()"), self.buscaCodigoLista)

		#Le damos posicion a nuestros botones
		self.desarrollo_button.move(50, 350)
		self.ingenieria_button.move(50, 450)
		self.logistica_button.move(50, 550)
		self.calidad_button.move(50, 550)
		refresh_button.move(400,750)
		finish_button.move(400,550)
		search_button.move(400,350)

		#Ahora le damos un tamano a nuestros botones
		self.desarrollo_button.setFixedSize(150, 110)
		self.ingenieria_button.setFixedSize(150, 110)
		self.logistica_button.setFixedSize(150, 110)
		self.calidad_button.setFixedSize(150, 110)
		refresh_button.setFixedSize(150, 110)
		finish_button.setFixedSize(180, 110)
		search_button.setFixedSize(150, 110)

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(6)
		grid.setVerticalSpacing(5)

		#Agregamos los widgets al grid
		grid.addWidget(self.desarrollo_button,1,1)
		grid.addWidget(self.ingenieria_button,1,3)
		grid.addWidget(self.logistica_button,1,5)
		grid.addWidget(self.calidad_button,1,7)
		grid.addWidget(refresh_button,5,6)
		grid.addWidget(finish_button,5,4)
		grid.addWidget(search_button,5,2)
		grid.addWidget(self.tabla,2,0,3,9)

		#Por ultimo agregamos todo el Layout con todos nuestros widgets
		self.setLayout(grid)

	def LimpiarTabla(self):
		self.tabla.clear();
		self.tabla.setRowCount(0);
		self.tabla.setColumnCount(SIZE_COLUMNS_AVIOS)
		self.tabla.setHorizontalHeaderLabels(AVIOS_TABLE_LIST)

	def refresh_table(self,AREA_ID):
		self.LimpiarTabla()
		VALUE_DESC=False
		if(AREA_ID==AREA_CONTROL_ID):
			VALUE_DESC=True
		#Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
		db=get_connection()
		self.listaAvios = controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_ID),VALUE_DESC)
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
				datess=0
				if(self.listaAvios[index].id_process==PROCESS_AVIOS_FIN_DES_ID):
					datess=9
				if(self.listaAvios[index].id_process!=PROCESS_AVIOS_ACTIVATE_ID and self.listaAvios[index].id_process!=PROCESS_AVIOS_COMPLETED_ID):
					if (time_pass_one_day(str(self.listaAvios[index].mod_date),datess)):
						self.tabla.item(index, 5).setBackground(QColor(238,0,0))
					else:
						self.tabla.item(index, 5).setBackground(QColor(0,205,0))
					self.tabla.item(index, 5).setTextColor(QColor(255, 255, 255))
				self.tabla.setItem(index,6, QTableWidgetItem(str(self.listaAvios[index].llegada_date)))
				self.btn_sell = QPushButton('Ver Comentarios')
				self.btn_sell.clicked.connect(self.VerComentarios)
				self.tabla.setCellWidget(index,7,self.btn_sell)
				stringRow = stringRow + str(index+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))
		db.close()

	def VerComentarios(self):
		button = qApp.focusWidget()
		index = self.tabla.indexAt(button.pos())
		if index.isValid():
			ventana = comments_avios.ventanaCommentarios(id_avios=self.listaAvios[index.row()].id_avios).exec_()
    
	def tablaDesarrollo(self):
		db=get_connection()
		self.desarrollo_button.setText("Desarrollo ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_DESARROLLO_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_DESARROLLO_ID
		self.refresh_table(AREA_DESARROLLO_ID)

	def tablaIngenieria(self):
		db=get_connection()
		self.ingenieria_button.setText("Ingenieria ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_INGENIERIA_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_INGENIERIA_ID
		self.refresh_table(AREA_INGENIERIA_ID)

	def tablaLogistica(self):
		db=get_connection()
		self.logistica_button.setText("Logistica ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_LOGISTICA_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_LOGISTICA_ID
		self.refresh_table(AREA_LOGISTICA_ID)

	def tablaCalidad(self):
		db=get_connection()
		self.calidad_button.setText("Control de Calidad ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_CALIDAD_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_CALIDAD_ID
		self.refresh_table(AREA_CALIDAD_ID)

	def tablaFinalizados(self):
		self.AREA_ACTUAL_ID=AREA_CONTROL_ID
		self.refresh_table(AREA_CONTROL_ID)

	def Actualizar(self):
		self.Refresh_Numbers()
		self.refresh_table(self.AREA_ACTUAL_ID)

	def Refresh_Numbers(self):
		db=get_connection()
		self.desarrollo_button.setText("Desarrollo ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_DESARROLLO_ID))))+")")
		self.ingenieria_button.setText("Ingenieria ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_INGENIERIA_ID))))+")")
		self.logistica_button.setText("Logistica ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_LOGISTICA_ID))))+")")
		self.calidad_button.setText("Control de Calidad ("+str(len(controller_avios.get_avios_by_process_list(db,controller_process_avios.get_process_avios_by_id_area(db,AREA_CALIDAD_ID))))+")")
		db.close()

	def buscaCodigoLista(self):
		if(self.control_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
		else:
			self.control_singleton=True
			ventana = control_view.ventanaBusqueda()
			ventana.exec_()
			if(ventana.option):
				self.searchCodigo(ventana.purchase_order,ventana.contract_number,ventana.client,ventana.option)
			self.control_singleton=False

	def searchCodigo(self,str_po,str_code,str_client,searchoption):
		self.AREA_ACTUAL_ID=AREA_CONTROL_ID
		db=get_connection()
		if(searchoption==1):
			self.listaAvios=controller_avios.get_avios_by_po(db,str_po)
		elif(searchoption==2):
			self.listaAvios=controller_avios.get_avios_by_number(db,str_code)
		elif(searchoption==3):
			self.listaAvios=controller_avios.get_avios_by_client(db,str_client)
		self.LimpiarTabla()
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
				datess=0
				if(self.listaAvios[index].id_process==PROCESS_AVIOS_FIN_DES_ID):
					datess=9
				if(self.listaAvios[index].id_process!=PROCESS_AVIOS_ACTIVATE_ID and self.listaAvios[index].id_process!=PROCESS_AVIOS_COMPLETED_ID):
					if (time_pass_one_day(str(self.listaAvios[index].mod_date),datess)):
						self.tabla.item(index, 5).setBackground(QColor(238,0,0))
					else:
						self.tabla.item(index, 5).setBackground(QColor(0,205,0))
					self.tabla.item(index, 5).setTextColor(QColor(255, 255, 255))
				self.tabla.setItem(index,6, QTableWidgetItem(str(self.listaAvios[index].llegada_date)))
				self.btn_sell = QPushButton('Ver Comentarios')
				self.btn_sell.clicked.connect(self.VerComentarios)
				self.tabla.setCellWidget(index,7,self.btn_sell)
				stringRow = stringRow + str(index+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))
		db.close()