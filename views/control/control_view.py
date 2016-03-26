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

class control_window(QWidget):
  	def __init__(self):
  		super(control_window, self).__init__()
  		#Dar tamano a la pantalla
  		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height())-(size.height())
		left=(desktopSize.width())-(size.width())
		self.move(left, top)
		#abrimos la pantalla princilal para todas las areas
		self.pantallasAreas()
  		self.setWindowTitle('control_window')
  		self.show()

  	def pantallasAreas(self):
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
  		actualizar_horario = QPushButton('Actualizar', self)
  		salir = QPushButton('Salir', self)
  		#Le damos funcionalidades a cada boton
  		salir.clicked.connect(QCoreApplication.instance().quit)
  		self.connect(actualizar_horario, SIGNAL("clicked()"), self.Actualizar)
  		
  		#Le damos posicion a nuestros botones
  		actualizar_horario.move(50, 150)
  		salir.move(50, 250)

  		#Ahora le damos un tamano a nuestros botones
		actualizar_horario.setFixedSize(150, 110)
		salir.setFixedSize(150, 110)

  		#le damos un espacio a nuestro grid
  		grid.setSpacing(25)

  		#Agregamos los widgets al grid
  		grid.addWidget(actualizar_horario,1,0)
  		grid.addWidget(salir,2,0)
  		grid.addWidget(self.tabla,1,2,5,2)

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