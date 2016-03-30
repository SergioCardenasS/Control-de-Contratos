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
from views import comments

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
		#abrimos el creador de la pantalla
		self.pantallasCreador()
		self.setWindowTitle(TITLE_APP+CONTROL_TITLE)
		self.show()
		self.Refresh_Numbers()
		self.control_singleton=False

	def pantallasCreador(self):
		self.listaContratos=[]
		#Un temporal para saber en que boton estamos
		self.AREA_ACTUAL_ID=AREA_COMERCIAL_ID
		#Creacion de la tabla  con cada item
		self.tabla = QTableWidget()
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

		#Ahora creamos dicha filas de numeros o ids
		self.tabla.setVerticalHeaderLabels(QString(self.stringRow).split(";"))

		#Crearemos un grid ponde estaran todos nuestro widgets
		grid = QGridLayout()

		#Instaciamos botones
		self.comercial_button = QPushButton('Comercial', self)
		self.abastecimiento_button = QPushButton('Abastecimiento', self)
		self.desarrollo_button = QPushButton('Desarrollo', self)
		self.ingenieria_button = QPushButton('Ingenieria', self)
		self.planificacion_button = QPushButton('Planificacion', self)
		refresh_button = QPushButton('Actualizar', self)
		undoicon = QIcon.fromTheme("view-refresh")
		refresh_button.setIcon(undoicon)
		finish_button = QPushButton('Contratos Finalizados', self)
		undoicon = QIcon.fromTheme("folder")
		finish_button.setIcon(undoicon)
		search_button = QPushButton('Buscar Contrato', self)
		undoicon = QIcon.fromTheme("edit-find")
		search_button.setIcon(undoicon)

		#Le damos funcionalidades a cada boton
		self.connect(refresh_button, SIGNAL("clicked()"), self.Actualizar)
		self.connect(self.comercial_button, SIGNAL("clicked()"), self.tablaComercial)
		self.connect(self.abastecimiento_button, SIGNAL("clicked()"), self.tablaAbastecimiento)
		self.connect(self.desarrollo_button, SIGNAL("clicked()"), self.tablaDesarrollo)
		self.connect(self.ingenieria_button, SIGNAL("clicked()"), self.tablaIngenieria)
		self.connect(self.planificacion_button, SIGNAL("clicked()"), self.tablaPlanificacion)
		self.connect(finish_button, SIGNAL("clicked()"), self.tablaFinalizados)
		self.connect(search_button, SIGNAL("clicked()"), self.buscaCodigoLista)

		#Le damos posicion a nuestros botones
		self.comercial_button.move(50, 150)
		self.abastecimiento_button.move(50, 250)
		self.desarrollo_button.move(50, 350)
		self.ingenieria_button.move(50, 450)
		self.planificacion_button.move(50, 550)
		refresh_button.move(400,750)
		finish_button.move(400,550)
		search_button.move(400,350)

		#Ahora le damos un tamano a nuestros botones
		self.comercial_button.setFixedSize(150, 110)
		self.abastecimiento_button.setFixedSize(150, 110)
		self.desarrollo_button.setFixedSize(150, 110)
		self.ingenieria_button.setFixedSize(150, 110)
		self.planificacion_button.setFixedSize(150, 110)
		refresh_button.setFixedSize(150, 110)
		finish_button.setFixedSize(180, 110)
		search_button.setFixedSize(150, 110)

		#le damos un espacio a nuestro grid
		grid.setHorizontalSpacing(6)
		grid.setVerticalSpacing(5)

		#Agregamos los widgets al grid
		grid.addWidget(self.comercial_button,1,0)
		grid.addWidget(self.abastecimiento_button,1,2)
		grid.addWidget(self.desarrollo_button,1,4)
		grid.addWidget(self.ingenieria_button,1,6)
		grid.addWidget(self.planificacion_button,1,8)
		grid.addWidget(refresh_button,5,6)
		grid.addWidget(finish_button,5,4)
		grid.addWidget(search_button,5,2)
		grid.addWidget(self.tabla,2,0,3,9)

		#Por ultimo agregamos todo el Layout con todos nuestros widgets
		self.setLayout(grid)

	def refresh_table(self,AREA_ID):
		self.LimpiarTabla()
		#Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
		VALUE_DESC=False
		if(AREA_ID==AREA_CONTROL_ID):
			VALUE_DESC=True
		db=get_connection()
		self.listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ID),VALUE_DESC)
		db.close()
		numEventos = self.rows
		#Guardamos el nuevo tamano de items
		self.rows = len(self.listaContratos)
		self.tabla.setRowCount(self.rows)
		#Este size hara los id o filas en string
		stringRow = ''
		#Ahora nuevamente sacamos todos los elementos
		for numContratos in range(len(self.listaContratos)):
			#De esa forma actualizaremos
			self.tabla.setItem(numContratos,0, QTableWidgetItem(self.listaContratos[numContratos].purchase_order))
			self.tabla.setItem(numContratos,1, QTableWidgetItem(self.listaContratos[numContratos].contract_number))
			self.tabla.setItem(numContratos,2, QTableWidgetItem(get_str_name_from_id_process(self.listaContratos[numContratos].id_process)))
			self.tabla.setItem(numContratos,3, QTableWidgetItem(get_str_contract_type(self.listaContratos[numContratos].contract_type)))
			self.tabla.setItem(numContratos,4, QTableWidgetItem(str(self.listaContratos[numContratos].init_date)))
			self.tabla.setItem(numContratos,5, QTableWidgetItem(str(self.listaContratos[numContratos].mod_date)))
			if(self.AREA_ACTUAL_ID!=AREA_CONTROL_ID):
				if (time_pass_one_day(str(self.listaContratos[numContratos].mod_date)) == True):
					self.tabla.item(numContratos, 5).setBackground(QColor(238,0,0))	
				else:
					self.tabla.item(numContratos, 5).setBackground(QColor(0,205,0))
				self.tabla.item(numContratos, 5).setTextColor(QColor(255, 255, 255))
			self.tabla.setItem(numContratos,6, QTableWidgetItem(str(self.listaContratos[numContratos].iteration_number)))
			self.btn_sell = QPushButton('Ver Comentarios')
			self.btn_sell.clicked.connect(self.VerComentarios)
			self.tabla.setCellWidget(numContratos,7,self.btn_sell)
			stringRow = stringRow + str(numContratos+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

	def VerComentarios(self):
		button = qApp.focusWidget()
		index = self.tabla.indexAt(button.pos())
		if index.isValid():
			ventana = comments.ventanaCommentarios(id_contract=self.listaContratos[index.row()].id_contract).exec_()

	def tablaComercial(self):
		db=get_connection()
		self.comercial_button.setText("Comercial ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_COMERCIAL_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_COMERCIAL_ID
		self.refresh_table(AREA_COMERCIAL_ID)

	def tablaAbastecimiento(self):
		db=get_connection()
		self.abastecimiento_button.setText("Abastecimiento ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ABASTECIMIENTOS_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_ABASTECIMIENTOS_ID
		self.refresh_table(AREA_ABASTECIMIENTOS_ID)
    
	def tablaDesarrollo(self):
		db=get_connection()
		self.desarrollo_button.setText("Desarrollo ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_DESARROLLO_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_DESARROLLO_ID
		self.refresh_table(AREA_DESARROLLO_ID)

	def tablaIngenieria(self):
		db=get_connection()
		self.ingenieria_button.setText("Ingenieria ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_INGENIERIA_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_INGENIERIA_ID
		self.refresh_table(AREA_INGENIERIA_ID)

	def tablaPlanificacion(self):
		db=get_connection()
		self.planificacion_button.setText("Planificacion ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_PLANIFICACION_ID))))+")")
		db.close()
		self.AREA_ACTUAL_ID=AREA_PLANIFICACION_ID
		self.refresh_table(AREA_PLANIFICACION_ID)

	def tablaFinalizados(self):
		self.AREA_ACTUAL_ID=AREA_CONTROL_ID
		self.refresh_table(AREA_CONTROL_ID)

	def Actualizar(self):
		self.Refresh_Numbers()
		self.refresh_table(self.AREA_ACTUAL_ID)

	def Refresh_Numbers(self):
		db=get_connection()
		self.comercial_button.setText("Comercial ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_COMERCIAL_ID))))+")")
		self.abastecimiento_button.setText("Abastecimiento ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ABASTECIMIENTOS_ID))))+")")
		self.desarrollo_button.setText("Desarrollo ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_DESARROLLO_ID))))+")")
		self.ingenieria_button.setText("Ingenieria ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_INGENIERIA_ID))))+")")
		self.planificacion_button.setText("Planificacion ("+str(len(get_contract_by_process_list(db,get_process_by_id_area(db,AREA_PLANIFICACION_ID))))+")")
		db.close()

	def LimpiarTabla(self):
		self.tabla.clear();
		self.tabla.setRowCount(0);
		self.tabla.setColumnCount(SIZE_COLUMNS)
		self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS).split(SPLIT))

	def buscaCodigoLista(self):
		if(self.control_singleton):
			QMessageBox.warning(self, 'Error',ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
		else:
			self.control_singleton=True
			ventana = ventanaBusqueda()
			ventana.exec_()
			if(ventana.contract_number!="E"):
				self.searchCodigo(ventana.purchase_order,ventana.contract_number)
			self.control_singleton=False

	def searchCodigo(self,str_po,str_code):
		db=get_connection()
		self.listaContratos=get_contracts_by_number(db,str_po,str_code)
		db.close()
		self.LimpiarTabla()
		numEventos = self.rows
		#Guardamos el nuevo tamano de items
		self.rows = len(self.listaContratos)
		self.tabla.setRowCount(self.rows)
		#Este size hara los id o filas en string
		stringRow = ''
		#Ahora nuevamente sacamos todos los elementos
		for numContratos in range(len(self.listaContratos)):
			#De esa forma actualizaremos
			self.tabla.setItem(numContratos,0, QTableWidgetItem(self.listaContratos[numContratos].purchase_order))
			self.tabla.setItem(numContratos,1, QTableWidgetItem(self.listaContratos[numContratos].contract_number))
			self.tabla.setItem(numContratos,2, QTableWidgetItem(get_str_name_from_id_process(self.listaContratos[numContratos].id_process)))
			self.tabla.setItem(numContratos,3, QTableWidgetItem(get_str_contract_type(self.listaContratos[numContratos].contract_type)))
			self.tabla.setItem(numContratos,4, QTableWidgetItem(str(self.listaContratos[numContratos].init_date)))
			self.tabla.setItem(numContratos,5, QTableWidgetItem(str(self.listaContratos[numContratos].mod_date)))
			if (time_pass_one_day(str(self.listaContratos[numContratos].mod_date)) == True):
				self.tabla.item(numContratos, 5).setBackground(QColor(238,0,0))	
			else:
				self.tabla.item(numContratos, 5).setBackground(QColor(0,205,0))
			self.tabla.item(numContratos, 5).setTextColor(QColor(255, 255, 255))
			self.tabla.setItem(numContratos,6, QTableWidgetItem(str(self.listaContratos[numContratos].iteration_number)))
			self.btn_sell = QPushButton('Ver Comentarios')
			self.btn_sell.clicked.connect(self.VerComentarios)
			self.tabla.setCellWidget(numContratos,7,self.btn_sell)
			stringRow = stringRow + str(numContratos+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

class ventanaBusqueda(QDialog):
	def __init__(self, parent=None):
		super(ventanaBusqueda, self).__init__(parent)
		#Nombre de los campos
		#Creacion de botones
		self.aceptarBoton = QPushButton("Buscar", self)
		self.cancelarBoton = QPushButton("Cancelar")

		#Creacion de los label
		Ccontract_number = QLabel('Contrato')
		self.editcontract_number = QLineEdit()
		Purchase_Order = QLabel('PO')
		self.editpurchase_order = QLineEdit()

		#Creando el grid
		grid = QGridLayout()
		grid.addWidget(Purchase_Order,1,0)
		grid.addWidget(self.editpurchase_order,1,1)
		grid.addWidget(Ccontract_number,2,0)
		grid.addWidget(self.editcontract_number,2,1)

		grid.addWidget(self.aceptarBoton,3,1)
		grid.addWidget(self.cancelarBoton,3,2)

		self.setLayout(grid)

		#Dando tamaño a la pantalla
		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)-(size.height()/2)
		left=(desktopSize.width()/2)-(size.width()/2)
		self.move(left, top)
		self.setWindowTitle('Buscar Contrato')
		self.show()
		#Funcionalidades de los botones
		self.connect(self.cancelarBoton, SIGNAL("clicked()"), self.Sair)
		self.connect(self.aceptarBoton, SIGNAL("clicked()"), self.Crear)
		self.contract_number = ''
		self.purchase_order = ''

	def Crear(self):
		self.purchase_order = self.editpurchase_order.text()
		self.contract_number = self.editcontract_number.text()
		if(str_is_invalid(self.purchase_order)):
			QMessageBox.warning(self, 'Error',"PO No Valido", QMessageBox.Ok)
		elif(is_invalid_contract_number(self.contract_number)):
			QMessageBox.warning(self, 'Error',"Numero de Contrato no Valido", QMessageBox.Ok)
		else:
			self.close()

	def Sair(self):
		self.contract_number = 'E'
		self.purchase_order = 'E'
		self.close()
