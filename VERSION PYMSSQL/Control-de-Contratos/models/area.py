#!/usr/bin/env python
# -*- coding: utf-8 -*-

# La clase area almacenara todas las areas dentro de la empresa
class Area():
	# id del area sera la Primary Key y auto-incrementable habran pocas pero podremos agregar mas si se desea
	id_area 	= 0
	# nombre del area dentro de la empresa que tambien servira como su id para autentificarse
	name 		= ""
	# el password o contraseña sera para poder logearse en cada unas de las areas
	password 	= ""
	def  __init__(self, row_area):
		self.id_area 	= row_area[0]
		self.name 		= row_area[1]
		self.password 	= row_area[2]
	def insert(self,cursor_db):
		insert_code_area="""INSERT INTO Area values('%d','%s','%s')"""%(self.id_area,self.name,self.password)
		cursor_db.execute(insert_code_area)