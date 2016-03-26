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
from controllers.controller_contract import *
from controllers.controller_process import *


class control_window(QWidget):
  def __init__(self):
    super(control_window, self).__init__()
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
    self.pantallasAreas()
    self.setWindowTitle('Administrador')
    self.show()

  def pantallasAreas(self):
    #Un tipo para saber en que boton estamos
    self.Type = None
    #Creacion de la tabla  con cada item
    self.tabla = QTableWidget()
    tablaItem = QTableWidgetItem()
    self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #Numero de items o filas
    self.rows = 0
    self.stringRow = ''
    #Creamos las columnas
    self.tabla.setColumnCount(SIZE_COLUMNS)
    self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS).split(SPLIT))
    #Por ahora solo creamos el numero de filas o items
    self.tabla.setRowCount(self.rows)

    #Estas variables son para darle un tamano dependiendo del texto pero solo para las columnas
    header = self.tabla.horizontalHeader()
    header.setResizeMode(QHeaderView.Stretch)

    #Esta lista de elementos tendra la query en lista
    #listaEventos = [['1','2','3'],['1','2','3'],['1','2','3']]
    #for numEventos in range(len(listaEventos)):
    #self.tabla.setItem(numEventos,0, QTableWidgetItem(listaEventos[numEventos].nombre))
    #self.tabla.setItem(numEventos,1, QTableWidgetItem(listaEventos[numEventos].importancia))
    #self.tabla.setItem(numEventos,2, QTableWidgetItem(listaEventos[numEventos].alerta))
    # Asi se sacarain los elementos si fueran datos de una base de datos
      #self.tabla.setItem(numEventos,0, QTableWidgetItem(listaEventos[numEventos][0]))
      #self.tabla.setItem(numEventos,1, QTableWidgetItem(listaEventos[numEventos][1]))
      #self.tabla.setItem(numEventos,2, QTableWidgetItem(listaEventos[numEventos][2]))
    # Ahora necesitamos un orden en las filas, podriamos hacerlo con el id o si con el mismo iterador de esta variable numEventos
      #self.stringRow = self.stringRow + str(numEventos+1) + ";"

    #Ahora creamos dicha filas de numeros o ids
    self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))

    #Crearemos un grid ponde estaran todos nuestro widgets
    grid = QGridLayout()

    #Instaciamos botones
    comercial_button = QPushButton('Comercial', self)
    abastecimiento_button = QPushButton('Abastecimiento', self)
    desarrollo_button = QPushButton('Desarrollo', self)
    ingenieria_button = QPushButton('Ingenieria', self)
    planificacion_button = QPushButton('Planificacion', self)
    refresh_button = QPushButton('Refresh', self)

    #Le damos funcionalidades a cada boton
    #self.connect(refresh_button, SIGNAL("clicked()"), self.Actualizar)
    self.connect(comercial_button, SIGNAL("clicked()"), self.tablaComercial)
    self.connect(abastecimiento_button, SIGNAL("clicked()"), self.tablaAbastecimiento)
    self.connect(desarrollo_button, SIGNAL("clicked()"), self.tablaDesarrollo)
    self.connect(ingenieria_button, SIGNAL("clicked()"), self.tablaIngenieria)
    self.connect(planificacion_button, SIGNAL("clicked()"), self.tablaPlanificacion)

    #Le damos posicion a nuestros botones
    comercial_button.move(50, 150)
    abastecimiento_button.move(50, 250)
    desarrollo_button.move(50, 350)
    ingenieria_button.move(50, 450)
    planificacion_button.move(50, 550)
    refresh_button.move(400,550)

    #Ahora le damos un tamano a nuestros botones
    comercial_button.setFixedSize(150, 110)
    abastecimiento_button.setFixedSize(150, 110)
    desarrollo_button.setFixedSize(150, 110)
    ingenieria_button.setFixedSize(150, 110)
    planificacion_button.setFixedSize(150, 110)
    refresh_button.setFixedSize(150, 110)

    #le damos un espacio a nuestro grid
    grid.setHorizontalSpacing(6)
    grid.setVerticalSpacing(5)

    #Agregamos los widgets al grid
    grid.addWidget(comercial_button,1,0)
    grid.addWidget(abastecimiento_button,1,2)
    grid.addWidget(desarrollo_button,1,4)
    grid.addWidget(ingenieria_button,1,6)
    grid.addWidget(planificacion_button,1,8)
    grid.addWidget(refresh_button,5,4)
    grid.addWidget(self.tabla,2,0,3,9)

    #Por ultimo agregamos todo el Layout con todos nuestros widgets
    self.setLayout(grid)

  def close_db(self):
    if(self.db_connected):
      self.db_connected=False
      self.db.close()

  def tablaComercial(self):
    self.LimpiarTabla()
    #Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
    db = get_connection()
    listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_COMERCIAL_ID))
    numEventos = self.rows
    #Guardamos el nuevo tamano de items
    self.rows = len(listaContratos)
    self.tabla.setRowCount(self.rows)
    #Este size hara los id o filas en string
    stringRow = ''
    #Ahora nuevamente sacamos todos los elementos
    for numContratos in range(len(listaContratos)):
      #self.tabla.setItem(size,0, QTableWidgetItem(listaEventos[size].nombre))
      #De esa forma actualizaremos
      self.tabla.setItem(numContratos,0, QTableWidgetItem(listaEventos[numContratos][0]))
      self.tabla.setItem(numContratos,1, QTableWidgetItem(listaEventos[numContratos][1]))
      self.tabla.setItem(numContratos,2, QTableWidgetItem(listaEventos[numContratos][2]))
      self.tabla.setItem(numContratos,3, QTableWidgetItem(listaEventos[numContratos][3]))
      self.tabla.setItem(numContratos,4, QTableWidgetItem(listaEventos[numContratos][4]))
      self.tabla.setItem(numContratos,5, QTableWidgetItem(listaEventos[numContratos][5]))
      self.tabla.setItem(numContratos,6, QTableWidgetItem(listaEventos[numContratos][6]))
      self.btn_sell = QPushButton('Comentarios')
      self.btn_sell.clicked.connect(self.handleButtonClicked)
      self.table.setCellWidget(numContratos,7,self.btn_sell)
      stringRow = stringRow + str(numContratos+1) + SPLIT
    #Ahorta solo la seteamos
    self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

  def tablaAbastecimiento(self):
    self.LimpiarTabla()
    #Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
    db = get_connection()
    listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ABASTECIMIENTOS_ID))
    numEventos = self.rows
    #Guardamos el nuevo tamano de items
    self.rows = len(listaContratos)
    self.tabla.setRowCount(self.rows)
    #Este size hara los id o filas en string
    stringRow = ''
    #Ahora nuevamente sacamos todos los elementos
    for numContratos in range(len(listaContratos)):
      #self.tabla.setItem(size,0, QTableWidgetItem(listaEventos[size].nombre))
      #De esa forma actualizaremos
      self.tabla.setItem(numContratos,0, QTableWidgetItem(listaEventos[numContratos][0]))
      self.tabla.setItem(numContratos,1, QTableWidgetItem(listaEventos[numContratos][1]))
      self.tabla.setItem(numContratos,2, QTableWidgetItem(listaEventos[numContratos][2]))
      self.tabla.setItem(numContratos,3, QTableWidgetItem(listaEventos[numContratos][3]))
      self.tabla.setItem(numContratos,4, QTableWidgetItem(listaEventos[numContratos][4]))
      self.tabla.setItem(numContratos,5, QTableWidgetItem(listaEventos[numContratos][5]))
      self.tabla.setItem(numContratos,6, QTableWidgetItem(listaEventos[numContratos][6]))
      self.btn_sell = QPushButton('Comentarios')
      self.btn_sell.clicked.connect(self.handleButtonClicked)
      self.table.setCellWidget(numContratos,7,self.btn_sell)
      stringRow = stringRow + str(numContratos+1) + SPLIT
    #Ahorta solo la seteamos
    self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))
    
  def tablaDesarrollo(self):
    self.LimpiarTabla()
    #Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
    db = get_connection()
    listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_DESARROLLO_ID))
    numEventos = self.rows
    #Guardamos el nuevo tamano de items
    self.rows = len(listaContratos)
    self.tabla.setRowCount(self.rows)
    #Este size hara los id o filas en string
    stringRow = ''
    #Ahora nuevamente sacamos todos los elementos
    for numContratos in range(len(listaContratos)):
      #self.tabla.setItem(size,0, QTableWidgetItem(listaEventos[size].nombre))
      #De esa forma actualizaremos
      self.tabla.setItem(numContratos,0, QTableWidgetItem(listaEventos[numContratos][0]))
      self.tabla.setItem(numContratos,1, QTableWidgetItem(listaEventos[numContratos][1]))
      self.tabla.setItem(numContratos,2, QTableWidgetItem(listaEventos[numContratos][2]))
      self.tabla.setItem(numContratos,3, QTableWidgetItem(listaEventos[numContratos][3]))
      self.tabla.setItem(numContratos,4, QTableWidgetItem(listaEventos[numContratos][4]))
      self.tabla.setItem(numContratos,5, QTableWidgetItem(listaEventos[numContratos][5]))
      self.tabla.setItem(numContratos,6, QTableWidgetItem(listaEventos[numContratos][6]))
      self.btn_sell = QPushButton('Comentarios')
      self.btn_sell.clicked.connect(self.handleButtonClicked)
      self.table.setCellWidget(numContratos,7,self.btn_sell)
      stringRow = stringRow + str(numContratos+1) + SPLIT
    #Ahorta solo la seteamos
    self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

  def tablaIngenieria(self):
    self.LimpiarTabla()
    #Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
    db = get_connection()
    listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_INGENIERIA_ID))
    numEventos = self.rows
    #Guardamos el nuevo tamano de items
    self.rows = len(listaContratos)
    self.tabla.setRowCount(self.rows)
    #Este size hara los id o filas en string
    stringRow = ''
    #Ahora nuevamente sacamos todos los elementos
    for numContratos in range(len(listaContratos)):
      #self.tabla.setItem(size,0, QTableWidgetItem(listaEventos[size].nombre))
      #De esa forma actualizaremos
      self.tabla.setItem(numContratos,0, QTableWidgetItem(listaEventos[numContratos][0]))
      self.tabla.setItem(numContratos,1, QTableWidgetItem(listaEventos[numContratos][1]))
      self.tabla.setItem(numContratos,2, QTableWidgetItem(listaEventos[numContratos][2]))
      self.tabla.setItem(numContratos,3, QTableWidgetItem(listaEventos[numContratos][3]))
      self.tabla.setItem(numContratos,4, QTableWidgetItem(listaEventos[numContratos][4]))
      self.tabla.setItem(numContratos,5, QTableWidgetItem(listaEventos[numContratos][5]))
      self.tabla.setItem(numContratos,6, QTableWidgetItem(listaEventos[numContratos][6]))
      self.btn_sell = QPushButton('Comentarios')
      self.btn_sell.clicked.connect(self.handleButtonClicked)
      self.table.setCellWidget(numContratos,7,self.btn_sell)
      stringRow = stringRow + str(numContratos+1) + SPLIT
    #Ahorta solo la seteamos
    self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))
  
  def tablaPlanificacion(self):
    self.LimpiarTabla()
    #Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
    db = get_connection()
    listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_PLANIFICACION_ID))
    numEventos = self.rows
    #Guardamos el nuevo tamano de items
    self.rows = len(listaContratos)
    self.tabla.setRowCount(self.rows)
    #Este size hara los id o filas en string
    stringRow = ''
    #Ahora nuevamente sacamos todos los elementos
    for numContratos in range(len(listaContratos)):
      #self.tabla.setItem(size,0, QTableWidgetItem(listaEventos[size].nombre))
      #De esa forma actualizaremos
      self.tabla.setItem(numContratos,0, QTableWidgetItem(listaEventos[numContratos][0]))
      self.tabla.setItem(numContratos,1, QTableWidgetItem(listaEventos[numContratos][1]))
      self.tabla.setItem(numContratos,2, QTableWidgetItem(listaEventos[numContratos][2]))
      self.tabla.setItem(numContratos,3, QTableWidgetItem(listaEventos[numContratos][3]))
      self.tabla.setItem(numContratos,4, QTableWidgetItem(listaEventos[numContratos][4]))
      self.tabla.setItem(numContratos,5, QTableWidgetItem(listaEventos[numContratos][5]))
      self.tabla.setItem(numContratos,6, QTableWidgetItem(listaEventos[numContratos][6]))
      self.btn_sell = QPushButton('Comentarios')
      self.btn_sell.clicked.connect(self.handleButtonClicked)
      self.table.setCellWidget(numContratos,7,self.btn_sell)
      stringRow = stringRow + str(numContratos+1) + SPLIT
    #Ahorta solo la seteamos
    self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

  def LimpiarTabla(self):
    self.tabla.clear();
    self.tabla.setRowCount(0);
    self.tabla.setColumnCount(SIZE_COLUMNS)
    self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS).split(SPLIT))
