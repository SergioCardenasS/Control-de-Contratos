#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
import datetime

#Import de Modulos
BASE_DIR='..'
sys.path.insert(0,BASE_DIR)
from constants import *

#Clase Contract:
#Contiene su PO, Numero de Conrato, el estado en el
#que se encuentra y su fecha de inicio y ultima
#modificacio, incluyendo el numero de iteracion en
#la que se encuentra.
class Contract:
	#Indice del Contrato
	id_contract			= 0
	#Orden de Compra del Contrato
	purchase_order		= ""
	#Numero del Contrato
	contract_number		= ""
	#Indice del Proceso (Estado)
	id_process			= 0
	#Tipo del Contrato
	contract_type		= CONTRACT_TYPE_PROVISIONAL
	#Fecha Inicial (creacion del Control del Contrato)
	init_date			= ""
	#Fecha de Ultima Modificacion (Ultima modificacion del Control del Contrato)
	mod_date			= ""
	#Numero de Iteracion del Control del Contrato
	iteration_number	= 0
	#Constructor de la clase Contrato, recive una fila de la tabla de la bases de datos, como una lista.
	def __init__(self, row_contract):
		self.id_contract		= int(row_contract[0])
		self.purchase_order		= row_contract[1]
		self.contract_number	= row_contract[2]
		self.id_process			= row_contract[3]
		self.contract_type		= ord(chr(row_contract[4]))
		self.init_date			= str(row_contract[5])
		self.mod_date			= str(row_contract[6])
		self.iteration_number	= row_contract[7]
	def insert(self,cursor_db):
		if(str_is_invalid(self.purchase_order) or str_is_invalid(self.contract_number)):
			return False
		insert_code_contract="""INSERT INTO Contract
								(purchase_order,contract_number,id_process,contract_type,init_date,mod_date,iteration_number)
								values('%s','%s','%d',CONVERT(bit,'%d'),'%s','%s','%d'
								)"""%(self.purchase_order,
										self.contract_number,
										self.id_process,
										self.contract_type,
										self.init_date,
										self.mod_date,
										self.iteration_number)
		cursor_db.execute(insert_code_contract)
		cursor_db.execute("select MAX(id_contract) from Contract")
		for row in cursor_db:
			self.id_contract=row[0]
		return True
	def update(self,cursor_db):
		if(str_is_invalid(self.purchase_order) or str_is_invalid(self.contract_number)):
			return False
		update_code_contract="""UPDATE Contract SET purchase_order='%s', contract_number='%s', id_process='%d', contract_type=CONVERT(bit,'%d'), mod_date='%s', iteration_number='%d'
							WHERE id_contract='%d'"""%(
									self.purchase_order,
									self.contract_number,
									self.id_process,
									self.contract_type,
									self.mod_date,
									self.iteration_number,
									self.id_contract)
		cursor_db.execute(update_code_contract)
		return True
