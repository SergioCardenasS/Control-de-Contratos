#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import process

def get_all_process(db):
	cursor=db.cursor()
	process_list=[]
	select_process="select * from Process"
	cursor.execute(select_process)
	for row in cursor:
		process_list.append(process.Process(row))
	return process_list

def get_process_by_id(db,id_process):
	cursor=db.cursor()
	select_process="select * from Process where id='%d'"%(id_process)
	cursor.execute(select_process)
	row=cursor.fetchone()
	if(row==None):
		return None
	return process.Process(row)

def get_process_by_id_area(db,id_area):
	cursor=db.cursor()
	process_list=[]
	select_process="select * from Process where id_area='%d'"%(id_area)
	cursor.execute(select_process)
	for row in cursor:
		process_list.append(process.Process(row))
	return process_list