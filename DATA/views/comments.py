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
from controllers import controller_comment
from views.control import control_fin_process

class ventanaCommentarios(QDialog):
	def __init__(self, id_contract, with_control = False, parent=None):
		super(ventanaCommentarios, self).__init__(parent)
		self.liberado = False
		self.id_contract=id_contract
		self.with_control=with_control
		#crear la ventana
		self.control_singleton=False
		self.ventanaCreador()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(3*desktopSize.height()/4)
		left=(3*desktopSize.width()/4)
		self.resize(left, top)
		self.setWindowTitle('Ver Comentarios')
		self.show()

	def ventanaCreador(self):
		#Nombre de los campos
		#Creacion de botones
		self.aceptarBoton = QPushButton("OK", self)
		if(self.with_control):
			self.liberarContrato = QPushButton("Liberar Contrato", self)
		#Creando el grid
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
		#self.tabla.resizeColumnsToContents()
		#Numero de items o filas
		db=get_connection()
		listaCometarios = controller_comment.get_all_comments_by_id_contract(db,self.id_contract)
		db.close()
		self.rows = len(listaCometarios)
		self.stringRow = ''
		#Creamos las columnas
		self.tabla.setColumnCount(SIZE_COLUMNS_COMMENT)
		self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS_COMMENT).split(SPLIT))
		#Por ahora solo creamos el numero de filas o items
		self.tabla.setRowCount(self.rows)
		color=False
		#Esta lista de elementos tendra la query en lista
		for numEventos in range(len(listaCometarios)):
			self.tabla.setItem(numEventos,0, QTableWidgetItem(get_str_name_by_id_area(listaCometarios[numEventos].id_area)))
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment_date)))
			self.tabla.setItem(numEventos,2, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
			if(color):
				self.tabla.item(numEventos,0).setBackground(QColor(ColorGRAY,ColorGRAY,ColorGRAY))
				self.tabla.item(numEventos,1).setBackground(QColor(ColorGRAY,ColorGRAY,ColorGRAY))
				self.tabla.item(numEventos,2).setBackground(QColor(ColorGRAY,ColorGRAY,ColorGRAY))
				color=False
			else:
				color=True
			#Agregando texEdit()
			#self.btn_sell = QTextEdit()
			#self.btn_sell.setText(self.tabla.item(numEventos,1).text())
			#self.tabla.setCellWidget(numEventos,1,self.btn_sell)
			#self.btn_sell.setReadOnly(True)

			# Ahora necesitamos un orden en las filas, podriamos hacerlo con el id o si con el mismo iterador de esta variable numEventos
			self.stringRow = self.stringRow + str(numEventos+1) + ";"

		#Ahora creamos dicha filas de numeros o ids
		self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))

		self.tabla.setColumnWidth(0, WIDTH_COLUMN_COMMENT)
		self.tabla.resizeRowsToContents()
		self.tabla.horizontalHeader().setStretchLastSection(True)

		#Crearemos un grid ponde estaran todos nuestro widgets
		grid = QGridLayout()

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(6)
		grid.setVerticalSpacing(5)

		#Tamano del boton
		self.aceptarBoton.setFixedSize(150, 110)
		if(self.with_control):
			self.liberarContrato.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.aceptarBoton,2,4)
		if(self.with_control):
			grid.addWidget(self.liberarContrato,1,4)
		grid.addWidget(self.tabla,1,0,5,3)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.aceptarBoton.clicked.connect(self.close)
		if(self.with_control):
			self.liberarContrato.clicked.connect(self.free_contract)

	def free_contract(self):
		if(self.control_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
		else:
			self.control_singleton=True
			ventana = control_fin_process.FinishProcessFreeContract(id_contract=self.id_contract)
			ventana.exec_()
			self.control_singleton=False
			if(ventana.liberado):
				self.liberado = True
				self.close()
