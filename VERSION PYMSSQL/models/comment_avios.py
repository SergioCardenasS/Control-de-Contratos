#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='..'
sys.path.insert(0,BASE_DIR)
from constants import *

class CommentAvios():
	id_avios 		= 0
	comment_number 	= 0
	id_area 		= 0
	comment 		= ""
	comment_date	= ""
	def __init__(self, row_comment_avio):
		self.id_avios	 	= row_comment_avio[0]
		self.comment_number = row_comment_avio[1]
		self.id_area 		= row_comment_avio[2]
		self.comment 		= row_comment_avio[3]
		self.comment_date	= str(row_comment_avio[4])
	def insert(self,cursor_db):
		if(str_is_invalid(self.comment)):
			return False
		insert_code_comment_avio="""INSERT INTO CommentAvios values('%d','%d','%d','%s','%s')"""%(self.id_avios,self.comment_number,self.id_area,self.comment,self.comment_date)
		cursor_db.execute(insert_code_comment_avio)
		return True
