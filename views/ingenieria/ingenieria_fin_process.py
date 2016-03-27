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

class FinishProcessSetWeight(QDialog):
	def __init__(self, contract ,parent=None):
		super(FinishProcessSetWeight, self).__init__(parent)
		self.contract=contract
		#crear la ventana
		self.finishProcessSetWeightWindow()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(3*desktopSize.height()/4)
		left=(3*desktopSize.width()/4)
		self.resize(left, top)
		self.setWindowTitle('Ver Comentarios')
		self.show()

	def finishProcessSetWeightWindow(self):
		#Nombre de los campos
		#Creacion de botones
		self.atrasBoton = QPushButton("Atras", self)
		self.crearBoton = QPushButton("Pesos Colocados", self)
		#Creando el grid
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tabla.resizeColumnsToContents()
		#Numero de items o filas
		db=get_connection()
		listaCometarios = controller_comment.get_all_comments_by_id_contract(db,self.contract.id_contract)
		db.close()
		self.rows = len(listaCometarios)
		self.stringRow = ''
		#Creamos las columnas
		self.tabla.setColumnCount(SIZE_COLUMNS_END)
		self.tabla.setHorizontalHeaderLabels(QString(TITLE_COLUMNS_END).split(SPLIT))
		#Por ahora solo creamos el numero de filas o items
		self.tabla.setRowCount(self.rows)

		#Estas variables son para darle un tamano dependiendo del texto pero solo para las columnas
		header = self.tabla.verticalHeader()
		header.setResizeMode(QHeaderView.Stretch)

		#Esta lista de elementos tendra la query en lista
		for numEventos in range(len(listaCometarios)):
			self.tabla.setItem(numEventos,0, QTableWidgetItem(get_str_name_by_id_area(listaCometarios[numEventos].id_area)))
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
			# Ahora necesitamos un orden en las filas, podriamos hacerlo con el id o si con el mismo iterador de esta variable numEventos
			self.stringRow = self.stringRow + str(numEventos+1) + ";"

		#Ahora creamos dicha filas de numeros o ids
		self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))
		self.tabla.setColumnWidth(0, WIDTH_COLUMN_COMMENT)
		self.tabla.horizontalHeader().setStretchLastSection(True)

		#Crearemos un grid ponde estaran todos nuestro widgets
		grid = QGridLayout()

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(9)
		grid.setVerticalSpacing(6)

		#Nombre de los imputs
		self.commentary = QLabel('Comentario')

		self.editCommentary = QTextEdit()

		#Tamano del boton
		self.atrasBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(250, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,5,2)
		grid.addWidget(self.editCommentary,5,3)
		grid.addWidget(self.crearBoton,7,3)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)