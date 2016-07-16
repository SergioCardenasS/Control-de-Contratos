#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import avios_control

def get_all_avios(db):
	cursor=db.cursor()
	avios_list=[]
	select="select * from Avios"
	cursor.execute(select)
	for row in cursor:
		avios_list.append(avios_control.Avios(row))
	return avios_list

def get_avios_by_id(db,id_avios):
	cursor=db.cursor()
	select="select * from Avios where id_avios='%d'"%(id_avios)
	cursor.execute(select)
	row=cursor.fetchone()
	if(row==None):
		return None
	return avios_control.Avios(row)

def get_avios_by_process_list(db,process_list,asc_desc=False):
	cursor=db.cursor()
	avios_list=[]
	select="select * from Avios where id_process IN ('%d'"%(process_list[0].id_process)
	for index in range(1,len(process_list)):
		select+=",'%d'"%(process_list[index].id_process)
	select+=") ORDER BY mod_date"
	if(asc_desc):
		select+=" DESC"
	cursor.execute(select)
	for row in cursor:
		avios_list.append(avios_control.Avios(row))
	return avios_list
