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
from models import comment_avios
from controllers import controller_comment_avios,controller_contract,controller_avios

class StartAviosControl(QDialog):
	def __init__(self, s_avios ,parent=None):
		super(StartAviosControl, self).__init__(parent)
		self.avios=s_avios
		db=get_connection()
		self.contract=controller_contract.get_contracts_by_id(db,self.avios.id_contract)
		db.close()
		#crear la ventana
		self.pantalla()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)
		left=(desktopSize.width()/2)
		self.resize(left, top)
		self.setWindowTitle('Activar Control')
		self.show()

	def pantalla(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Iniciar Control", self)
		self.atrasBoton = QPushButton("Atras", self)
		#Creando el grid
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tabla.resizeColumnsToContents()
		#Numero de items o filas
		db=get_connection()
		listaCometarios = controller_comment_avios.get_all_comments_by_id_avios(db,self.avios.id_avios)
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
		grid.setHorizontalSpacing(9)
		grid.setVerticalSpacing(6)

		#Nombre de los imputs
		self.commentary = QLabel('Comentario')

		self.editCommentary = QTextEdit()
		#Tamano del boton
		self.atrasBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3)
		grid.addWidget(self.crearBoton,6,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.ActivateControl)

	def ActivateControl(self):
		reply=QMessageBox.question(self,
		'Message',"Esta Seguro de Iniciar un Control de Avios del contrato: "+str(self.contract.contract_number),
		QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_avios.avios_is_equal(db,self.avios)):
				self.avios.mod_date = get_time_str()
				self.avios.id_process=PROCESS_AVIOS_FIN_DES_ID
				if(self.avios.update(db.cursor())):
					new_comment = comment_avios.CommentAvios([self.avios.id_avios,1,AREA_DESARROLLO_ID,Commentary,self.avios.mod_date])
					if(new_comment.insert(db.cursor())):
						db.commit()
						db.close()
						self.close()
					else:
						QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
						self.avios.id_process=PROCESS_AVIOS_ACTIVATE_ID
						db.close()
				else:
					QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
					self.avios.id_process=PROCESS_AVIOS_ACTIVATE_ID
					db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_AVIOS, QMessageBox.Ok)
				db.close()
				self.close()

class FinishDesarrolloAvios(QDialog):
	def __init__(self, s_avios ,parent=None):
		super(FinishDesarrolloAvios, self).__init__(parent)
		self.avios=s_avios
		db=get_connection()
		self.contract=controller_contract.get_contracts_by_id(db,self.avios.id_contract)
		db.close()
		#crear la ventana
		self.pantalla()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)
		left=(desktopSize.width()/2)
		self.resize(left, top)
		self.setWindowTitle('Finalizar Trabajo')
		self.show()

	def pantalla(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Finalizar", self)
		self.atrasBoton = QPushButton("Atras", self)
		#Creando el grid
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.tabla.resizeColumnsToContents()
		#Numero de items o filas
		db=get_connection()
		listaCometarios = controller_comment_avios.get_all_comments_by_id_avios(db,self.avios.id_avios)
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
		grid.setHorizontalSpacing(9)
		grid.setVerticalSpacing(6)

		#Nombre de los imputs
		self.commentary = QLabel('Comentario')

		self.editCommentary = QTextEdit()
		#Tamano del boton
		self.atrasBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3)
		grid.addWidget(self.crearBoton,6,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishDesarrolloAviosTask)

	def FinishDesarrolloAviosTask(self):
		reply=QMessageBox.question(self,
		'Message',"Enviar a Ingenieria el Control de Avios del contrato: "+str(self.contract.contract_number),
		QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_avios.avios_is_equal(db,self.avios)):
				self.avios.mod_date = get_time_str()
				self.avios.id_process=PROCESS_AVIOS_FIN_ING_ID
				if(self.avios.update(db.cursor())):
					new_comment = comment_avios.CommentAvios([self.avios.id_avios,controller_comment_avios.get_next_number_comment_by_id_avios(db,self.avios.id_avios),AREA_DESARROLLO_ID,Commentary,self.avios.mod_date])
					if(new_comment.insert(db.cursor())):
						db.commit()
						db.close()
						self.close()
					else:
						QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
						self.avios.id_process=PROCESS_AVIOS_FIN_DES_ID
						db.close()
				else:
					QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
					self.avios.id_process=PROCESS_AVIOS_FIN_DES_ID
					db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_AVIOS, QMessageBox.Ok)
				db.close()
				self.close()
