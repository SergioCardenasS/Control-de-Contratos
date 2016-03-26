#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import comment

def get_all_comments(db):
	cursor=db.cursor()
	comment_list=[]
	select_comment="select * from Comment"
	cursor.execute(select_comment)
	for row in cursor:
		process_list.append(comment.Comment(row))
	return comment_list
