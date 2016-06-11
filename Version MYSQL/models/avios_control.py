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
	def __init__(self, row_avios):
		self.id_avios			= row_avios[0]
		self.id_contract		= row_avios[1]
		self.id_process			= row_avios[2]
		self.init_date			= str(row_avios[3])
		self.mod_date			= str(row_avios[4])

	def insert(self,cursor_db):
		insert_code_avios="""INSERT INTO Avios
								(id_contract,id_process,init_date,mod_date)
								values('%d','%d','%s','%s'
								)"""%(self.id_contract,
										self.id_process,
										self.init_date,
										self.mod_date)
		cursor_db.execute(insert_code_avios)
		cursor_db.execute("select MAX(id_avios) from Avios")
		for row in cursor_db:
			self.id_avios=row[0]
		return True
