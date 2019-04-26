#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import comment_avios

def get_all_comments(db):
	cursor=db.cursor()
	comment_list=[]
	select_comment="select * from CommentAvios"
	cursor.execute(select_comment)
	for row in cursor:
		comment_list.append(comment_avios.CommentAvios(row))
	return comment_list

def get_all_comments_by_id_avios(db,id_avios):
	cursor=db.cursor()
	comment_list=[]
	select_comment="select * from CommentAvios where id_avios='%d' order by comment_number DESC"%(id_avios)
	cursor.execute(select_comment)
	for row in cursor:
		comment_list.append(comment_avios.CommentAvios(row))
	return comment_list

def get_next_number_comment_by_id_avios(db,id_avios):
	cursor=db.cursor()
	select_comment="select MAX(comment_number) from CommentAvios where id_avios='%d'"%(id_avios)
	cursor.execute(select_comment)
	val=0
	for row in cursor:
		val=row[0]
	if(val!=None):
		return val+1
	return 1
