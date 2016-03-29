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
		comment_list.append(comment.Comment(row))
	return comment_list

def get_all_comments_by_id_contract(db,id_contract):
	cursor=db.cursor()
	comment_list=[]
	select_comment="select * from Comment where id_contract='%d' order by comment_number DESC"%(id_contract)
	cursor.execute(select_comment)
	for row in cursor:
		comment_list.append(comment.Comment(row))
	return comment_list

def get_next_number_comment_by_id_contract(db,id_contract):
	cursor=db.cursor()
	select_comment="select MAX(comment_number) from Comment where id_contract='%d'"%(id_contract)
	cursor.execute(select_comment)
	val=0
	for row in cursor:
		val=row[0]
	return val+1
