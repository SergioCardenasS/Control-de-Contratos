#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='..'
sys.path.insert(0,BASE_DIR)
from constants import *

class Comment():
	id_contract 	= 0
	comment_number 	= 0
	id_area 		= 0
	comment 		= ""
	comment_date	= ""
	def __init__(self, row_comment):
		self.id_contract 	= row_comment[0]
		self.comment_number = row_comment[1]
		self.id_area 		= row_comment[2]
		self.comment 		= row_comment[3]
		self.comment_date	= str(row_comment[4])
	def insert(self,cursor_db):
		if(str_is_invalid(self.comment)):
			return False
		insert_code_comment="""INSERT INTO Comment values('%d','%d','%d',"%s",'%s')"""%(self.id_contract,self.comment_number,self.id_area,self.comment,self.comment_date)
		cursor_db.execute(insert_code_comment)
		return True
