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

class control_window(QWidget):
	def __init__(self):
		super(control_window, self).__init__()
		#Dar tamano a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height())-(size.height())
		left=(desktopSize.width())-(size.width())
		self.move(left, top)
		#Creacion de conexion a BD
		#abrimos el creador de la pantalla
		self.pantallasCreador()
		self.setWindowTitle('Administrador')
		self.show()
		self.Refresh_Numbers()

	def pantallasCreador(self):
		#Un temporal para saber en que boton estamos
		self.AREA_ACTUAL_ID=AREA_COMERCIAL_ID
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
		comercial_button = QPushButton('Comercial', self)
		abastecimiento_button = QPushButton('Abastecimiento', self)
		desarrollo_button = QPushButton('Desarrollo', self)
		ingenieria_button = QPushButton('Ingenieria', self)
		planificacion_button = QPushButton('Planificacion', self)
		refresh_button = QPushButton('Actualizar', self)
		finish_button = QPushButton('Contratos Finalizados', self)

		#Le damos funcionalidades a cada boton
		self.connect(refresh_button, SIGNAL("clicked()"), self.Actualizar)
		self.connect(comercial_button, SIGNAL("clicked()"), self.tablaComercial)
		self.connect(abastecimiento_button, SIGNAL("clicked()"), self.tablaAbastecimiento)
		self.connect(desarrollo_button, SIGNAL("clicked()"), self.tablaDesarrollo)
		self.connect(ingenieria_button, SIGNAL("clicked()"), self.tablaIngenieria)
		self.connect(planificacion_button, SIGNAL("clicked()"), self.tablaPlanificacion)
		self.connect(finish_button, SIGNAL("clicked()"), self.tablaFinalizados)

		#Le damos posicion a nuestros botones
		comercial_button.move(50, 150)
		abastecimiento_button.move(50, 250)
		desarrollo_button.move(50, 350)
		ingenieria_button.move(50, 450)
		planificacion_button.move(50, 550)
		refresh_button.move(400,550)
		finish_button.move(400,350)

		#Ahora le damos un tamano a nuestros botones
		comercial_button.setFixedSize(150, 110)
		abastecimiento_button.setFixedSize(150, 110)
		desarrollo_button.setFixedSize(150, 110)
		ingenieria_button.setFixedSize(150, 110)
		planificacion_button.setFixedSize(150, 110)
		refresh_button.setFixedSize(150, 110)
		finish_button.setFixedSize(180, 110)

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(6)
		grid.setVerticalSpacing(5)

		#Agregamos los widgets al grid
		grid.addWidget(comercial_button,1,0)
		grid.addWidget(abastecimiento_button,1,2)
		grid.addWidget(desarrollo_button,1,4)
		grid.addWidget(ingenieria_button,1,6)
		grid.addWidget(planificacion_button,1,8)
		grid.addWidget(refresh_button,5,4)
		grid.addWidget(finish_button,5,2)
		grid.addWidget(self.tabla,2,0,3,9)

		#Por ultimo agregamos todo el Layout con todos nuestros widgets
		self.setLayout(grid)

	def refresh_table(self,AREA_ID):
		self.LimpiarTabla()
		#Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
		VALUE_DESC=False
		if(AREA_ID==AREA_CONTROL_ID):
			VALUE_DESC=True
		db=get_connection()
		self.listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ID),VALUE_DESC)
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
			self.tabla.setItem(numContratos,2, QTableWidgetItem(get_str_name_from_id_process(self.listaContratos[numContratos].id_process)))
			self.tabla.setItem(numContratos,3, QTableWidgetItem(get_str_contract_type(self.listaContratos[numContratos].contract_type)))
			self.tabla.setItem(numContratos,4, QTableWidgetItem(str(self.listaContratos[numContratos].init_date)))
			self.tabla.setItem(numContratos,5, QTableWidgetItem(str(self.listaContratos[numContratos].mod_date)))
			if (time_pass_one_day(str(self.listaContratos[numContratos].mod_date)) == True):
				self.tabla.item(numContratos, 5).setBackground(QColor(238,0,0))	
			else:
				self.tabla.item(numContratos, 5).setBackground(QColor(0,205,0))
			self.tabla.item(numContratos, 5).setTextColor(QColor(255, 255, 255))
			self.tabla.setItem(numContratos,6, QTableWidgetItem(str(self.listaContratos[numContratos].iteration_number)))
			self.btn_sell = QPushButton('Ver Comentarios')
			self.btn_sell.clicked.connect(self.VerComentarios)
			self.tabla.setCellWidget(numContratos,7,self.btn_sell)
			stringRow = stringRow + str(numContratos+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

	def VerComentarios(self):
		button = qApp.focusWidget()
		index = self.tabla.indexAt(button.pos())
		if index.isValid():
			ventana = comments.ventanaCommentarios(id_contract=self.listaContratos[index.row()].id_contract).exec_()

	def tablaComercial(self):
		self.AREA_ACTUAL_ID=AREA_COMERCIAL_ID
		self.refresh_table(AREA_COMERCIAL_ID)

	def tablaAbastecimiento(self):
		self.AREA_ACTUAL_ID=AREA_ABASTECIMIENTOS_ID
		self.refresh_table(AREA_ABASTECIMIENTOS_ID)
    
	def tablaDesarrollo(self):
		self.AREA_ACTUAL_ID=AREA_DESARROLLO_ID
		self.refresh_table(AREA_DESARROLLO_ID)

	def tablaIngenieria(self):
		self.AREA_ACTUAL_ID=AREA_INGENIERIA_ID
		self.refresh_table(AREA_INGENIERIA_ID)

	def tablaPlanificacion(self):
		self.AREA_ACTUAL_ID=AREA_PLANIFICACION_ID
		self.refresh_table(AREA_PLANIFICACION_ID)

	def tablaFinalizados(self):
		self.AREA_ACTUAL_ID=AREA_CONTROL_ID
		self.refresh_table(AREA_CONTROL_ID)

	def Actualizar(self):
		self.Refresh_Numbers()
		self.refresh_table(self.AREA_ACTUAL_ID)

	def Refresh_Numbers(self):
		print "oa"
		#db=get_connection()
		#TemplistaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ID))
		#db.close()

	def LimpiarTabla(self):
		self.tabla.clear();
		self.tabla.setRowCount(0);
		self.tabla.setColumnCount(SIZE_COLUMNS)
		self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS).split(SPLIT))
