#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import contract, comment
from controllers.controller_contract import *
from controllers.controller_process import *

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
		#abrimos la pantalla princilal para todas las areas
		self.pantallaComercial()
		self.setWindowTitle('Comercial')
		self.show()

	def pantallaComercial(self):
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
		self.refresh_table(AREA_COMERCIAL_ID)

	def Actualizar(self):
		self.refresh_table(AREA_COMERCIAL_ID)

	def LimpiarTabla(self):
		self.tabla.clear();
		self.tabla.setRowCount(0);
		self.tabla.setColumnCount(SIZE_COLUMNS)
		self.tabla.setHorizontalHeaderLabels(QString(TITLE_ROWS).split(SPLIT))

	def refresh_table(self,AREA_ID):
		self.LimpiarTabla()
		#Primero lo que hara esta funcion es actualizar los items nuevos para eso necesitamos el ultimo tamano de items
		db=get_connection()
		self.listaContratos = get_contract_by_process_list(db,get_process_by_id_area(db,AREA_ID))
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
			self.tabla.setItem(numContratos,6, QTableWidgetItem(str(self.listaContratos[numContratos].iteration_number)))
			self.btn_sell = QPushButton('Finalizar')
			self.btn_sell.clicked.connect(self.Finalizar)
			self.tabla.setCellWidget(numContratos,7,self.btn_sell)
			stringRow = stringRow + str(numContratos+1) + SPLIT
		self.tabla.setVerticalHeaderLabels(QString(stringRow).split(SPLIT))

	def crearContrato(self):
		ventana = ventanaContrato().exec_()
	def Finalizar(self):
		button = qApp.focusWidget()
		index = self.tabla.indexAt(button.pos())
		if index.isValid():
			print index.row()

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
	def Crear(self):
		PO = self.editPO.text()
		if(PO == ''):
			QMessageBox.warning(self, 'Error',CREATE_CONTRACT_ERROR_NO_PO_TYPED, QMessageBox.Ok)
		else:
			init_date = get_time_str()
			mod_date = init_date
			Is_Provisional = chr(self.editIs_Provisional.isChecked())
			Commentary = unicode(self.editCommentary.toPlainText())
			db=get_connection()
			new_contract = contract.Contract([0,PO,'-',PROCESS_SET_CODE_ID,Is_Provisional,init_date,mod_date,1])
			new_contract.insert(db.cursor())
			new_comment = comment.Comment([new_contract.id_contract,1,AREA_COMERCIAL_ID,Commentary])
			new_comment.insert(db.cursor())
			db.commit()
			db.close()
			self.close()
