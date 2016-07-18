#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
import datetime

#Import de Modulos
BASE_DIR='..'
sys.path.insert(0,BASE_DIR)
from constants import *

class Avios:
	id_avios			= 0
	id_contract			= 0
	id_process			= 0
	init_date			= ""
	mod_date			= ""
	llegada_data		= ""
	def __init__(self, row_avios):
		self.id_avios			= row_avios[0]
		self.id_contract		= row_avios[1]
		self.id_process			= row_avios[2]
		self.init_date			= str(row_avios[3])
		self.mod_date			= str(row_avios[4])
		self.llegada_date		= row_avios[5]

	def insert(self,cursor_db):
		insert_code_avios="""INSERT INTO Avios
								(id_contract,id_process,init_date,mod_date,llegada_date)
								values('%d','%d','%s','%s','%s'
								)"""%(self.id_contract,
										self.id_process,
										self.init_date,
										self.mod_date,
										self.llegada_date)
		cursor_db.execute(insert_code_avios)
		cursor_db.execute("select MAX(id_avios) from Avios")
		for row in cursor_db:
			self.id_avios=row[0]
		return True

	def update(self,cursor_db):
		update_code="""UPDATE Avios SET id_process='%d', mod_date='%s', llegada_date='%s'
							WHERE id_avios='%d'"""%(
									self.id_process,
									self.mod_date,
									self.llegada_date,
									self.id_avios)
		cursor_db.execute(update_code)
		return True
