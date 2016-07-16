#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import process_avios

def get_all_process_avios(db):
	cursor=db.cursor()
	process_list=[]
	select_process="select * from ProcessAvios"
	cursor.execute(select_process)
	for row in cursor:
		process_list.append(process_avios.ProcessAvios(row))
	return process_list

def get_process_avios_by_id(db,id_process):
	cursor=db.cursor()
	select_process="select * from ProcessAvios where id_process='%d'"%(id_process)
	cursor.execute(select_process)
	row=cursor.fetchone()
	if(row==None):
		return None
	return process_avios.ProcessAvios(row)

def get_process_avios_by_id_area(db,id_area):
	cursor=db.cursor()
	process_list=[]
	select_process="select * from ProcessAvios where id_area='%d'"%(id_area)
	cursor.execute(select_process)
	for row in cursor:
		process_list.append(process_avios.ProcessAvios(row))
	return process_list