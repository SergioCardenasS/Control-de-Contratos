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

class ventanaCommentarios(QDialog):
	def __init__(self, id_contract, parent=None):
		super(ventanaCommentarios, self).__init__(parent)
		self.id_contract=id_contract
		#crear la ventana
		self.ventanaCreador()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)-(size.height()/2)
		left=(desktopSize.width()/2)-(size.width()/2)
		self.move(left, top)
		self.setWindowTitle('Ver Comentarios')
		self.show()

	def ventanaCreador(self):
		#Nombre de los campos
		#Creacion de botones
		self.aceptarBoton = QPushButton("OK", self)
		#Creando el grid
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
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

		#Estas variables son para darle un tamano dependiendo del texto pero solo para las columnas
		header = self.tabla.horizontalHeader()
		header.setResizeMode(QHeaderView.Stretch)

		#Esta lista de elementos tendra la query en lista
		for numEventos in range(len(listaCometarios)):
			self.tabla.setItem(numEventos,0, QTableWidgetItem(get_str_name_by_id_area(listaCometarios[numEventos].id_area)))
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
			# Ahora necesitamos un orden en las filas, podriamos hacerlo con el id o si con el mismo iterador de esta variable numEventos
			self.stringRow = self.stringRow + str(numEventos+1) + ";"

		#Ahora creamos dicha filas de numeros o ids
		self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))

		#Crearemos un grid ponde estaran todos nuestro widgets
		grid = QGridLayout()

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(6)
		grid.setVerticalSpacing(5)

		#Agregamos los widgets al grid
		grid.addWidget(self.aceptarBoton,2,4)
		grid.addWidget(self.tabla,2,0,3,3)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.aceptarBoton.clicked.connect(self.close)
