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
from datetime import date
from models import comment_avios
from controllers import controller_comment_avios,controller_contract,controller_avios

class FinishLogisticaAvios(QDialog):
	def __init__(self, s_avios ,parent=None):
		super(FinishLogisticaAvios, self).__init__(parent)
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
		label_date1 = QLabel('Fecha Estimada')
		self.d_box1 = QComboBox()
		self.m_box1 = QComboBox()
		self.y_box1 = QComboBox()
		self.create_combo_box()

		self.editCommentary = QTextEdit()
		#Tamano del boton
		self.atrasBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3,1,2)
		grid.addWidget(self.crearBoton,6,5)
		grid.addWidget(label_date1,5,2)
		grid.addWidget(self.d_box1,5,3)
		grid.addWidget(self.m_box1,5,4)
		grid.addWidget(self.y_box1,5,5)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.FinishLogisticaAviosTask)
		self.connect(self.y_box1, SIGNAL("currentIndexChanged(QString)"), self.day_combo_box1)
		self.connect(self.m_box1, SIGNAL("currentIndexChanged(QString)"), self.day_combo_box1)

	def create_combo_box(self):
		actual_date=datetime.datetime.now()
		year_list=range(actual_date.year - MORE_YEARS,actual_date.year + MORE_YEARS)
		year_list.reverse()
		for year in year_list:
			self.y_box1.addItem(str(year))
		self.y_box1.setCurrentIndex(MORE_YEARS-1)
		for month in range(1,13):
			str_month=str(month)
			if(month<10):
				str_month="0"+str_month
			self.m_box1.addItem(str_month)
		self.m_box1.setCurrentIndex(actual_date.month - 1)
		self.max_day1=0
		if(actual_date.month==2):
			self.max_day1=int(actual_date.year%4==0)+28
		elif(actual_date.month==1 or actual_date.month==3 or actual_date.month==5 or actual_date.month==7 or actual_date.month==8 or actual_date.month==10 or actual_date.month==12):
			self.max_day1=31
		else:
			self.max_day1=30
		for day in range(1,self.max_day1+1):
			str_day=str(day)
			if(day<10):
				str_day="0"+str_day
			self.d_box1.addItem(str_day)
		self.d_box1.setCurrentIndex(actual_date.day - 1)

	def day_combo_box1(self):
		current_day = int(self.d_box1.currentText())
		current_month = int(self.m_box1.currentText())
		current_year = int(self.y_box1.currentText())
		new_day=0
		if(current_month==2):
			new_day=int(current_year%4==0)+28
		elif(current_month==1 or current_month==3 or current_month==5 or current_month==7 or current_month==8 or current_month==10 or current_month==12):
			new_day=31
		else:
			new_day=30
		if(self.max_day1!=new_day):
			self.max_day1=new_day
			self.d_box1.clear()
			for day in range(1,self.max_day1+1):
				str_day=str(day)
				if(day<10):
					str_day="0"+str_day
				self.d_box1.addItem(str_day)
			if(current_day<=self.max_day1):
				self.d_box1.setCurrentIndex(current_day - 1)
			else:
				self.d_box1.setCurrentIndex(0)

	def FinishLogisticaAviosTask(self):
		reply=QMessageBox.question(self,
		'Message',"Enviar a Logistica el Control de Avios del contrato: "+str(self.contract.contract_number),
		QMessageBox.Yes,QMessageBox.No)
		day1=int(self.d_box1.currentText())
		month1=int(self.m_box1.currentText())
		year1=int(self.y_box1.currentText())
		datestr1=str(date(year1,month1,day1))
		if reply == QMessageBox.Yes:
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_avios.avios_is_equal(db,self.avios)):
				self.avios.mod_date = get_time_str()
				self.avios.id_process=PROCESS_AVIOS_LLEGADA_ID
				self.avios.llegada_date=datestr1
				if(self.avios.update(db.cursor())):
					new_comment = comment_avios.CommentAvios([self.avios.id_avios,controller_comment_avios.get_next_number_comment_by_id_avios(db,self.avios.id_avios),AREA_LOGISTICA_ID,Commentary,self.avios.mod_date])
					if(new_comment.insert(db.cursor())):
						db.commit()
						db.close()
						self.close()
					else:
						QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
						self.avios.id_process=PROCESS_AVIOS_FIN_LOG_ID
						self.avios.llegada_date=""
						db.close()
				else:
					QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
					self.avios.id_process=PROCESS_AVIOS_FIN_LOG_ID
					self.avios.llegada_date=""
					db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_AVIOS, QMessageBox.Ok)
				db.close()
				self.close()

class AviosLLegadas(QDialog):
	def __init__(self, s_avios ,parent=None):
		super(AviosLLegadas, self).__init__(parent)
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
		self.setWindowTitle('Enviar LLegada de Avios')
		self.show()

	def pantalla(self):
		#Nombre de los campos
		#Creacion de botones
		self.crearBoton = QPushButton("Enviar a Control de Calidad", self)
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
		self.label_llegada = QLabel('Tipo')
		self.llegada = QComboBox()
		self.llegada.addItem("Llegada Parcial")
		self.llegada.addItem("Llegada Total")
		self.llegada.setCurrentIndex(0)

		self.editCommentary = QTextEdit()
		#Tamano del boton
		self.atrasBoton.setFixedSize(150, 110)
		self.crearBoton.setFixedSize(150, 110)

		#Agregamos los widgets al grid
		grid.addWidget(self.atrasBoton,0,1)
		grid.addWidget(self.tabla,0,2,4,5)
		grid.addWidget(self.label_llegada,5,2)
		grid.addWidget(self.llegada,5,3)
		grid.addWidget(self.commentary,6,2)
		grid.addWidget(self.editCommentary,6,3)
		grid.addWidget(self.crearBoton,6,4)
		self.setLayout(grid)
		#Funcionalidades de los botones
		self.atrasBoton.clicked.connect(self.close)
		self.connect(self.crearBoton, SIGNAL("clicked()"), self.SendAviosTask)

	def SendAviosTask(self):
		reply=QMessageBox.question(self,
		'Message',"Comunicar a Control de Calidad la Llegada del Avio del contrato: "+str(self.contract.contract_number),
		QMessageBox.Yes,QMessageBox.No)
		if reply == QMessageBox.Yes:
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			if(controller_avios.avios_is_equal(db,self.avios)):
				self.avios.mod_date = get_time_str()
				if(self.llegada.currentIndex()==SYGNAL_TYPE_TOTAL):
					self.avios.id_process=PROCESS_AVIOS_FIN_CONTROL_ID
					Commentary="Llegada Total: \n"+Commentary
				else:
					Commentary="Llegada Parcial: \n"+Commentary
				if(self.avios.update(db.cursor())):
					new_comment = comment_avios.CommentAvios([self.avios.id_avios,controller_comment_avios.get_next_number_comment_by_id_avios(db,self.avios.id_avios),AREA_LOGISTICA_ID,Commentary,self.avios.mod_date])
					if(new_comment.insert(db.cursor())):
						db.commit()
						db.close()
						self.close()
					else:
						QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
						self.avios.id_process=PROCESS_AVIOS_LLEGADA_ID
						db.close()
				else:
					QMessageBox.warning(self, 'Error',INVALID_STR, QMessageBox.Ok)
					self.avios.id_process=PROCESS_AVIOS_LLEGADA_ID
					db.close()
			else:
				QMessageBox.warning(self, 'Error',ERROR_MODIFICATE_AVIOS, QMessageBox.Ok)
				db.close()
				self.close()

