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


class desarrollo_window(QWidget):
  def __init__(self):
    super(desarrollo_window, self).__init__()
    #Dar tamano a la pantalla
    size=self.size()
    desktopSize=QDesktopWidget().screenGeometry()
    top=(desktopSize.height())-(size.height())
    left=(desktopSize.width())-(size.width())
    self.move(left, top)
    #abrimos la pantalla princilal para todas las areas
    self.pantallaDesarrollo()
    self.setWindowTitle('Desarrollo')
    self.show()

  def pantallaDesarrollo(self):
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
    actualizar_button = QPushButton('Actualizar', self)
    agregar_button = QPushButton('Agregar Codigo', self)
    devolver_button = QPushButton('Devolver a Comercial', self)

    #Le damos funcionalidades a cada boton
    self.connect(actualizar_button, SIGNAL("clicked()"), self.Actualizar)
    self.connect(devolver_button, SIGNAL("clicked()"), self.Devolver)
    self.connect(agregar_button, SIGNAL("clicked()"), self.agregarNumeroContrato)

    #Le damos posicion a nuestros botones
    actualizar_button.move(400,550)
    agregar_button.move(400,550)
    devolver_button.move(400,550)

    #Ahora le damos un tamano a nuestros botones
    actualizar_button.setFixedSize(150, 110)
    agregar_button.setFixedSize(150, 110)
    devolver_button.setFixedSize(150, 110)

    #le damos un espacio a nuestro grid
    grid.setHorizontalSpacing(6)
    grid.setVerticalSpacing(5)

    #Agregamos los widgets al grid
    grid.addWidget(actualizar_button,5,2)
    grid.addWidget(agregar_button,5,6)
    grid.addWidget(devolver_button,5,4)
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

  def Devolver(self):
    process = PROCESS_SET_PO_ID
    print "Se envia a Comercial", process

  def agregarNumeroContrato(self):
	ventana = ventanaContrato().exec_()

class ventanaContrato(QDialog):
  def __init__(self, parent=None):
    super(ventanaContrato, self).__init__(parent)
    #Nombre de los campos

    #Creacion de botones
    self.aceptarBoton = QPushButton("OK", self)
    self.cancelarBoton = QPushButton("Cancelar")

    #Creacion de los label
    ContractNumber = QLabel('Numero de contracto')
    Commentary = QLabel('Comentario')

    #Creacion de los campos de edicion
    self.editarContractNumber = QLineEdit()
    self.editCommentary = QTextEdit()
    #Para fecha seria asi dependiendo del tzlocal de la maquina con las liberia 'from dateutil.tz import tzlocal'
    #self.editarFecha_inicio = QDateTimeEdit(datetime.now(tzlocal()))

    #Creando el grid
    grid = QGridLayout()
    grid.addWidget(ContractNumber,1,0)
    grid.addWidget(self.editarContractNumber,1,1)

    grid.addWidget(Commentary,2,0)
    grid.addWidget(self.editCommentary,2,1)

    grid.addWidget(self.aceptarBoton,6,1)
    grid.addWidget(self.cancelarBoton,6,2)

    self.setLayout(grid)

    #Dando tamaño a la pantalla
    size=self.size()
    desktopSize=QDesktopWidget().screenGeometry()
    top=(desktopSize.height()/2)-(size.height()/2)
    left=(desktopSize.width()/2)-(size.width()/2)
    self.move(left, top)
    self.setWindowTitle('Crear Codigo de Contrato')
    self.show()

    #Funcionalidades de los botones
    self.cancelarBoton.clicked.connect(self.close)
    self.connect(self.aceptarBoton, SIGNAL("clicked()"), self.Crear_Codigo)

  def Crear_Codigo(self):
    ContractNumber = unicode(self.editarContractNumber.text())
    Commentary = unicode(self.editCommentary.toPlainText())
    #fecha_fin = datetime.strptime(str(self.editarFecha_fin.text()),'%d/%m/%y %H:%M') Para la transformacion del tiempo
    print ContractNumber, Commentary
    self.close()