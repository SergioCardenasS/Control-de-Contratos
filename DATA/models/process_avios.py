#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ProcessAvios:
	id_process	= 0
	name		= ""
	id_area		= 0
	def __init__(self,row_process):
		self.id_process	= row_process[0]
		self.name		= row_process[1]
		self.id_area	= row_process[2]
	def insert(self,cursor_db):
		insert_code_process="""INSERT INTO ProcessAvios values('%d','%s','%d')"""%(self.id_process,self.name,self.id_area)
		cursor_db.execute(insert_code_process)