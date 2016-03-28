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
from controllers import controller_comment, controller_contract

class FinishProcessSetPO(QDialog):
	def __init__(self, contract ,parent=None):
		super(FinishProcessSetPO, self).__init__(parent)
		self.contract=contract
		#crear la ventana
		self.finishProcessSetPOWindow()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(3*desktopSize.height()/4)
		left=(3*desktopSize.width()/4)
		self.resize(left, top)
		self.setWindowTitle('Finalizar Proceso')
		self.show()

	def finishProcessSetPOWindow(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Enviar a Desarrollo", self)
		self.atrasBoton = QPushButton("Atras", self)
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
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
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
		self.poNumber = QLabel('Numero de PO')
		self.Is_Provisional = QLabel('Provisional')
		self.commentary = QLabel('Comentario')

		self.editPONumber = QLineEdit() 
		self.editIs_Provisional = QRadioButton()
		self.editCommentary = QTextEdit()

		#Tamano del boton
		self.atrasBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)
		#iniciamos Datos
		self.editIs_Provisional.setChecked(bool(self.contract.contract_type))
		self.editPONumber.setText(str(self.contract.purchase_order))
		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.poNumber,5,2)
		grid.addWidget(self.editPONumber,5,3)
		grid.addWidget(self.Is_Provisional,6,2)
		grid.addWidget(self.editIs_Provisional,6,3)
		grid.addWidget(self.commentary,7,2)
		grid.addWidget(self.editCommentary,7,3)
		grid.addWidget(self.crearBoton,8,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishToDesarrolloBoton)

	def FinishToDesarrolloBoton(self):
		PO = self.editPONumber.text()
		if(PO == ''):
			QMessageBox.warning(self, 'Error',CREATE_CONTRACT_ERROR_NO_PO_TYPED, QMessageBox.Ok)
		else:
			reply=QMessageBox.question(self, 'Message',"Esta Seguro de la informacion que esta enviando a Desarrollo...",QMessageBox.Yes,QMessageBox.No)
			if reply == QMessageBox.Yes:
				Commentary = unicode(self.editCommentary.toPlainText())
				db=get_connection()
				if(controller_contract.contract_is_equal(db,self.contract)):
					self.contract.purchase_order = PO
					self.contract.contract_type = ord(chr(self.editIs_Provisional.isChecked()))
					self.contract.mod_date = get_time_str()
					self.contract.id_process=PROCESS_SET_CODE_ID
					if(self.contract.update(db.cursor())):
                                                new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
                                                if(new_comment.insert(db.cursor())):
                                                        db.commit()
                                                        db.close()
                                                        self.close()
                                                else:
                                                        QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,',tildes)", QMessageBox.Ok)
                                                        self.contract.id_process=PROCESS_SET_PO_ID
                                                        db.close()
                                        else:
                                                QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,',tildes)", QMessageBox.Ok)
                                                self.contract.id_process=PROCESS_SET_PO_ID
                                                db.close()
				else:
					QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                                        db.close()
                                        self.close()

class FinishProcessSavePreContract(QDialog):
	def __init__(self, contract ,parent=None):
		super(FinishProcessSavePreContract, self).__init__(parent)
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
		self.crearBoton = QPushButton("PreContrato Firmado", self)
		self.atrasBoton = QPushButton("Atras", self)
		self.aComercialBoton = QPushButton("Regresar a Desarrollo", self)
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
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
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
		self.aComercialBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3)
		grid.addWidget(self.aComercialBoton,8,3)
		grid.addWidget(self.crearBoton,8,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.aComercialBoton, SIGNAL("clicked()"), self.FinishToDesarrolloBoton)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishToSavePreContratoBoton)

	def FinishToDesarrolloBoton(self):
		Commentary = unicode(self.editCommentary.toPlainText())
		db=get_connection()
		if(controller_contract.contract_is_equal(db,self.contract)):
			self.contract.mod_date = get_time_str()
			self.contract.id_process=PROCESS_SET_CODE_ID
			if(self.contract.update(db.cursor())):
                                new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
                                if(new_comment.insert(db.cursor())):
                                        db.commit()
                                        db.close()
                                        self.close()
                                else:
                                        QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                        self.contract.id_process=PROCESS_SAVE_PRECONTRACT_ID
                                        db.close()
                        else:
                                QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,',tildes)", QMessageBox.Ok)
                                self.contract.id_process=PROCESS_SAVE_PRECONTRACT_ID
                                db.close()
		else:
			QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                        db.close()
                        self.close()

	def FinishToSavePreContratoBoton(self):
		reply=QMessageBox.question(self, 'Message',"Esta Seguro de Grabar PreContrato...",QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_contract.contract_is_equal(db,self.contract)):
				self.contract.mod_date = get_time_str()
				self.contract.id_process=PROCESS_SET_WEIGHT_ID
				if(self.contract.update(db.cursor())):
                                        new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
                                        if(new_comment.insert(db.cursor())):
                                                db.commit()
                                                db.close()
                                                self.close()
                                        else:
                                                QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                                self.contract.id_process=PROCESS_SAVE_PRECONTRACT_ID
                                                db.close()
                                else:
                                        QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                        self.contract.id_process=PROCESS_SAVE_PRECONTRACT_ID
                                        db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                                db.close()
                                self.close()

class FinishProcessSetAcesss(QDialog):
	def __init__(self, contract ,parent=None):
		super(FinishProcessSetAcesss, self).__init__(parent)
		self.contract=contract
		#crear la ventana
		self.finishProcessSetAcessWindow()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(3*desktopSize.height()/4)
		left=(3*desktopSize.width()/4)
		self.resize(left, top)
		self.setWindowTitle('Finalizar Proceso')
		self.show()

	def finishProcessSetAcessWindow(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Brindar Permiso Por Estado del Hilado", self)
		self.atrasBoton = QPushButton("Atras", self)
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
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
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
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishToSetAccess)

	def FinishToSetAccess(self):
		Commentary = unicode(self.editCommentary.toPlainText())
		db=get_connection()
		if(controller_contract.contract_is_equal(db,self.contract)):
			self.contract.mod_date = get_time_str()
			self.contract.id_process=PROCESS_YAM_STATUS_ID
			self.contract.update(db.cursor())
			new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
			if(new_comment.insert(db.cursor())):
                                db.commit()
                                db.close()
                                self.close()
                        else:
                                QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                self.contract.id_process=PROCESS_SET_ACCESS_ID
                                db.close()
		else:
			QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                        db.close()
                        self.close()

class FinishProcessAcceptDates(QDialog):
	def __init__(self, contract ,parent=None):
		super(FinishProcessAcceptDates, self).__init__(parent)
		self.contract=contract
		#crear la ventana
		self.finishProcessAcceptDatesWindow()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(3*desktopSize.height()/4)
		left=(3*desktopSize.width()/4)
		self.resize(left, top)
		self.setWindowTitle('Finalizar Proceso')
		self.show()

	def finishProcessAcceptDatesWindow(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Aceptar Fechas", self)
		self.atrasBoton = QPushButton("Atras", self)
		self.aComercialBoton = QPushButton("Rechazar Fechas", self)
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
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
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
		self.aComercialBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3)
		grid.addWidget(self.aComercialBoton,8,3)
		grid.addWidget(self.crearBoton,8,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.aComercialBoton, SIGNAL("clicked()"), self.FinishToPlanificacionBoton)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishToAcceptDateBoton)

	def FinishToPlanificacionBoton(self):
		Commentary = unicode(self.editCommentary.toPlainText())
		db=get_connection()
		if(controller_contract.contract_is_equal(db,self.contract)):
			self.contract.mod_date = get_time_str()
			self.contract.id_process=PROCESS_SET_DATES_ID
			self.contract.update(db.cursor())
			new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
			if(new_comment.insert(db.cursor())):
                                db.commit()
                                db.close()
                                self.close()
                        else:
                                QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                self.contract.id_process=PROCESS_ACCEPT_DATES_ID
                                db.close()
		else:
			QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                        db.close()
                        self.close()

	def FinishToAcceptDateBoton(self):
		reply=QMessageBox.question(self, 'Message',"Esta Seguro de haber Aceptado las Fechas...",QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_contract.contract_is_equal(db,self.contract)):
				self.contract.mod_date = get_time_str()
				self.contract.id_process=PROCESS_ACTIVATE_CONTRACT_ID
				self.contract.update(db.cursor())
				new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
				if(new_comment.insert(db.cursor())):
                                        db.commit()
                                        db.close()
                                        self.close()
                                else:
                                        QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                        self.contract.id_process=PROCESS_ACCEPT_DATES_ID
                                        db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                                db.close()
                                self.close()

class FinishProcessAcceptContract(QDialog):
	def __init__(self, contract ,parent=None):
		super(FinishProcessAcceptContract, self).__init__(parent)
		self.contract=contract
		#crear la ventana
		self.finishProcessAcceptContractWindow()
		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(3*desktopSize.height()/4)
		left=(3*desktopSize.width()/4)
		self.resize(left, top)
		self.setWindowTitle('Finalizar Proceso')
		self.show()

	def finishProcessAcceptContractWindow(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Activar Contrato", self)
		self.atrasBoton = QPushButton("Atras", self)
		self.aComercialBoton = QPushButton("Cambiar Provisional a Firme", self)
		self.aReiniciarBoton = QPushButton("Reiniciar Proceso", self)
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
			self.tabla.setItem(numEventos,1, QTableWidgetItem(str(listaCometarios[numEventos].comment)))
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
		self.aComercialBoton.setFixedSize(150, 110)
		self.aReiniciarBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3)
		grid.addWidget(self.aComercialBoton,8,2)
		grid.addWidget(self.aReiniciarBoton,8,3)
		grid.addWidget(self.crearBoton,8,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.aComercialBoton, SIGNAL("clicked()"), self.FinishToCambioBoton)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishToActivateContractBoton)
		self.connect(self.aReiniciarBoton, SIGNAL("clicked()"), self.FinishToReiniciarBoton)

	def FinishToCambioBoton(self):
		if(self.contract.contract_type==CONTRACT_TYPE_PROVISIONAL):
			reply=QMessageBox.question(self, 'Message',"Esta Seguro de Cambiar el contrato a Firme...",QMessageBox.Yes,QMessageBox.No)
			if reply == QMessageBox.Yes:
				Commentary = unicode(self.editCommentary.toPlainText())
				db=get_connection()
				if(controller_contract.contract_is_equal(db,self.contract)):
					self.contract.mod_date = get_time_str()
					self.contract.contract_type = CONTRACT_TYPE_FIRME
					self.contract.update(db.cursor())
					new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
					if(new_comment.insert(db.cursor())):
                                                db.commit()
                                                db.close()
                                                self.close()
                                        else:
                                                QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                                self.contract.contract_type = CONTRACT_TYPE_PROVISIONAL
                                                db.close()
				else:
					QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                                        db.close()
                                        self.close()
		else:
			QMessageBox.warning(self, 'Error',ERROR_IS_A_FIRME_CONTRACT, QMessageBox.Ok)
	def FinishToActivateContractBoton(self):
		if(self.contract.contract_type==CONTRACT_TYPE_FIRME):
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_contract.contract_is_equal(db,self.contract)):
				self.contract.mod_date = get_time_str()
				self.contract.id_process = PROCESS_COMPLETED_ID
				self.contract.update(db.cursor())
				new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
				if(new_comment.insert(db.cursor())):
                                        db.commit()
                                        db.close()
                                        self.close()
                                else:
                                        QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                        self.contract.id_process = PROCESS_ACTIVATE_CONTRACT_ID
                                        db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                                db.close()
                                self.close()
		else:
			QMessageBox.warning(self, 'Error',ERROR_IS_A_PROVISIONAL_CONTRACT, QMessageBox.Ok)
	def FinishToReiniciarBoton(self):
		if(self.contract.contract_type==CONTRACT_TYPE_PROVISIONAL):
			reply=QMessageBox.question(self, 'Message',"Esta Seguro de Reiniciar el Proceso...",QMessageBox.Yes,QMessageBox.No)
			if reply == QMessageBox.Yes:
				Commentary = unicode(self.editCommentary.toPlainText())
				db=get_connection()
				if(controller_contract.contract_is_equal(db,self.contract)):
					self.contract.mod_date = get_time_str()
					self.contract.id_process=PROCESS_SET_PO_ID
					self.contract.iteration_number+=1
					self.contract.update(db.cursor())
					new_comment = comment.Comment([self.contract.id_contract,controller_comment.get_next_number_comment_by_id_contract(db,self.contract.id_contract),AREA_COMERCIAL_ID,Commentary])
					if(new_comment.insert(db.cursor())):
                                                db.commit()
                                                db.close()
                                                self.close()
                                        else:
                                                QMessageBox.warning(self, 'Error',"No use caracteres ASCII (e.g \xa4,'tildes)", QMessageBox.Ok)
                                                self.contract.id_process = PROCESS_ACTIVATE_CONTRACT_ID
                                                self.contract.iteration_number-=1
                                                db.close()
				else:
					QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_CONTRACT, QMessageBox.Ok)
                                        db.close()
                                        self.close()
		else:
			QMessageBox.warning(self, 'Error',ERROR_IS_A_FIRME_CONTRACT, QMessageBox.Ok)
