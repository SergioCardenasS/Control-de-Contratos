#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime
import time

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import contract, comment

class comercial_window(QWidget):
	def __init__(self):
		super(comercial_window, self).__init__()
		#Dar tamano a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height())-(size.height())
		left=(desktopSize.width())-(size.width())
		self.move(left, top)
		#Creacion de conexion a BD
		self.db=get_connection()
		self.db_connected=True
		#abrimos la pantalla princilal para todas las areas
		self.pantallaComercial()
		self.setWindowTitle('Comercial')
		self.show()

	def pantallaComercial(self):
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
		tablaItem = QTableWidgetItem()
		#Numero de items o filas
		self.rows = 3
		self.stringRow = ''
		#Creamos las columnas
		self.tabla.setColumnCount(4)
		self.tabla.setHorizontalHeaderLabels(QString("Nombre;Proceso;Posicion;Estado").split(";"))
		#Por ahora solo creamos el numero de filas o items
		self.tabla.setRowCount(self.rows)

		#Estas variables son para darle un tamano dependiendo del texto pero solo para las columnas
		header = self.tabla.horizontalHeader()
		header.setResizeMode(QHeaderView.Stretch)
		#Esta lista de elementos tendra la query en lista
		listaEventos = [['1','2','3'],['1','2','3'],['1','2','3']]
		for numEventos in range(len(listaEventos)):
			#self.tabla.setItem(numEventos,0, QTableWidgetItem(listaEventos[numEventos].nombre))
			#self.tabla.setItem(numEventos,1, QTableWidgetItem(listaEventos[numEventos].importancia))
			#self.tabla.setItem(numEventos,2, QTableWidgetItem(listaEventos[numEventos].alerta))
			# Asi se sacarain los elementos si fueran datos de una base de datos

			self.tabla.setItem(numEventos,0, QTableWidgetItem(listaEventos[numEventos][0]))
			self.tabla.setItem(numEventos,1, QTableWidgetItem(listaEventos[numEventos][1]))
			self.tabla.setItem(numEventos,2, QTableWidgetItem(listaEventos[numEventos][2]))
			# Ahora necesitamos un orden en las filas, podriamos hacerlo con el id o si con el mismo iterador de esta variable numEventos
			self.stringRow = self.stringRow + str(numEventos+1) + ";"
		#Ahora creamos dicha filas de numeros o ids
		self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))

		#Crearemos un grid ponde estaran todos nuestro widgets
		grid = QGridLayout()

		#Instaciamos botones
		aceptar_button = QPushButton('Actualizar', self)
		aceptar1_button = QPushButton('Crear Control de Contrato', self)

		#Le damos funcionalidades a cada boton
		self.connect(aceptar_button, SIGNAL("clicked()"), self.Actualizar)
		self.connect(aceptar1_button, SIGNAL("clicked()"), self.crearContrato)

		#Le damos posicion a nuestros botones
		aceptar_button.move(400,550)
		aceptar1_button.move(400,550)

		#Ahora le damos un tamano a nuestros botones
		aceptar_button.setFixedSize(150, 110)
		aceptar1_button.setFixedSize(150, 110)

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(6)
		grid.setVerticalSpacing(5)

		#Agregamos los widgets al grid
		grid.addWidget(aceptar_button,5,3)
		grid.addWidget(aceptar1_button,5,5)
		grid.addWidget(self.tabla,1,0,3,9)

		#Por ultimo agregamos todo el Layout con todos nuestros widgets
		self.setLayout(grid)

	def Actualizar(self):
		#Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
		numEventos = self.rows
		#Guardamos el nuevo tamano de items
		self.rows = 4
		self.tabla.setRowCount(self.rows)
		#Este size hara los id o filas en string
		size = numEventos
		#Con este while creamos esa fila para actualizar la que teniamos mas antes
		while(numEventos<self.rows):
		  numEventos += 1
		  self.stringRow = self.stringRow + str(numEventos) + ";"

		#Ahorta solo la seteamos
		self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))

		#Ahora nuevamente sacamos todos los elementos
		listaEventos = [['1','2','3'],['1','2','3'],['1','2','3'],['1','2','3']]
		while(size<len(listaEventos)):
			#self.tabla.setItem(size,0, QTableWidgetItem(listaEventos[size].nombre))
			#De esa forma actualizaremos
			self.tabla.setItem(size,0, QTableWidgetItem(listaEventos[size][0]))
			self.tabla.setItem(size,1, QTableWidgetItem(listaEventos[size][1]))
			self.tabla.setItem(size,2, QTableWidgetItem(listaEventos[size][2]))
			size +=1
	def crearContrato(self):
		ventana = ventanaContrato().exec_()
	def close_db(self):
		if(self.db_connected):
			self.db_connected=False
			self.db.close()

class ventanaContrato(QDialog):
	def __init__(self, parent=None):
		super(ventanaContrato, self).__init__(parent)
		#Nombre de los campos
		#Creacion de botones
		self.aceptarBoton = QPushButton("OK", self)
		self.cancelarBoton = QPushButton("Cancelar")

		#Creacion de los label
		PO = QLabel('Purchase Orden')
		Commentary = QLabel('Comentario')
		Is_Provisional = QLabel('Provisional')

		#Creacion de los campos de edicion
		self.editPO = QLineEdit()
		self.editIs_Provisional = QRadioButton()
		self.editCommentary = QTextEdit()
		#Para fecha seria asi dependiendo de
		#Para fecha seria asi dependiendo del tzlocal de la maquina con las liberia ''
		#self.editarFecha_inicio = QDateTimeEdit(datetime.now(tzlocal()))

		#Creando el grid
		grid = QGridLayout()
		grid.addWidget(PO,1,0)
		grid.addWidget(self.editPO,1,1)

		grid.addWidget(Is_Provisional,2,0)
		grid.addWidget(self.editIs_Provisional,2,1)

		grid.addWidget(Commentary,3,0)
		grid.addWidget(self.editCommentary,3,1)

		grid.addWidget(self.aceptarBoton,7,1)
		grid.addWidget(self.cancelarBoton,7,2)

		self.setLayout(grid)

		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)-(size.height()/2)
		left=(desktopSize.width()/2)-(size.width()/2)
		self.move(left, top)
		self.setWindowTitle('Crear Control de Contrato')
		self.show()
		#Funcionalidades de los botones
		self.cancelarBoton.clicked.connect(self.close)
		self.connect(self.aceptarBoton, SIGNAL("clicked()"), self.Crear)
		#DB conexion
	def Crear(self):
		PO = self.editPO.text()
		if(PO == ''):
			QMessageBox.warning(self, 'Error',CREATE_CONTRACT_ERROR_NO_PO_TYPED, QMessageBox.Ok)
		else:
			db=get_connection()
			init_date = time.strftime('%Y-%m-%d %H:%m')
			mod_date = init_date
			Is_Provisional = int(self.editIs_Provisional.isChecked())
			Commentary = unicode(self.editCommentary.toPlainText())
			new_contract = contract.Contract([0,PO,'-',PROCESS_SET_CODE_ID,Is_Provisional,init_date,mod_date,1])
			new_contract.insert(db.cursor())
			new_comment = comment.Comment([new_contract.id_contract,1,AREA_COMERCIAL_ID,Commentary])
			new_comment.insert(db.cursor())
			db.commit()
			db.close()
			self.close()