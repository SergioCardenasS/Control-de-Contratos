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
from models import comment
from controllers import controller_comment,controller_contract

class FinishProcessSetCode(QDialog):
	def __init__(self, contract ,parent=None):
		super(FinishProcessSetCode, self).__init__(parent)
		self.contract=contract
		#crear la ventana
		self.finishProcessSetCodeWindow()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(3*desktopSize.height()/4)
		left=(3*desktopSize.width()/4)
		self.resize(left, top)
		self.setWindowTitle('Finalizar Proceso')
		self.show()

	def finishProcessSetCodeWindow(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Aceptar Datos", self)
		undoicon = QIcon.fromTheme("window-new")
		self.crearBoton.setIcon(undoicon)
		self.atrasBoton = QPushButton("Atras", self)
		undoicon = QIcon.fromTheme("go-previous")
		self.atrasBoton.setIcon(undoicon)
		self.aComercialBoton = QPushButton("Regresar a Comercial", self)
		undoicon = QIcon.fromTheme("mail-send")
		self.aComercialBoton.setIcon(undoicon)
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

		#Esta lista de elementos tendra la query en lista
		for numEventos in range(len(listaCometarios)):
			self.tabla.setItem(numEventos,0, QTableWidgetItem(get_str_name_by_id_area(listaCometarios[numEventos].id_area)))
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment_date)))
			self.tabla.setItem(numEventos,2, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
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
		self.Is_Provisional = QLabel('Es Provisional')
		self.commentary = QLabel('Comentario')

		self.editCommentary = QTextEdit()
		self.editIs_Provisional = QRadioButton()

		#Tamano del boton
		self.atrasBoton.setFixedSize(150, 110)
		self.aComercialBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#iniciamos Datos
		self.editIs_Provisional.setChecked(bool(self.contract.contract_type))
		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3)
		grid.addWidget(self.Is_Provisional,7,2)
		grid.addWidget(self.editIs_Provisional,7,3)
		grid.addWidget(self.aComercialBoton,8,3)
		grid.addWidget(self.crearBoton,8,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.aComercialBoton, SIGNAL("clicked()"), self.FinishToComercialBoton)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishToSetCodeBoton)

	def FinishToComercialBoton(self):
		Commentary = unicode(self.editCommentary.toPlainText())
		db=get_connection()
		if(controller_contract.contract_is_equal(db,self.contract)):
			self.contract.mod_date = get_time_str()
			self.contract.id_process=PROCESS_SET_PO_ID
			if(self.contract.update(db.cursor())):
				new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_DESARROLLO_ID,Commentary,self.contract.mod_date])
				if(new_comment.insert(db.cursor())):
					db.commit()
					db.close()
					self.close()
				else:
					QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
					self.contract.id_process=PROCESS_SET_CODE_ID
					db.close()
			else:
				QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
				self.contract.id_process=PROCESS_SET_CODE_ID
				db.close()
		else:
			QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
			db.close()
			self.close()

	def FinishToSetCodeBoton(self):
		reply=QMessageBox.question(self, 'Message',"Esta Seguro de Aceptar la PO y el tipo de Contrato...",QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_contract.contract_is_equal(db,self.contract)):
				self.contract.mod_date = get_time_str()
				self.contract.id_process=PROCESS_SAVE_PRECONTRACT_ID
				self.contract.contract_type=ord(chr(self.editIs_Provisional.isChecked()))
				if(self.contract.update(db.cursor())):
						new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_DESARROLLO_ID,Commentary,self.contract.mod_date])
						if(new_comment.insert(db.cursor())):
								db.commit()
								db.close()
								self.close()
						else:
								QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
								self.contract.id_process=PROCESS_SET_CODE_ID
								db.close()
				else:
						QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
						self.contract.id_process=PROCESS_SET_CODE_ID
						db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
				db.close()
				self.close()
