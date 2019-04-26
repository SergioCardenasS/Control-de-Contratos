#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import area

def get_all_areas(db):
	cursor=db.cursor()
	area_list=[]
	select_area="select * from Area"
	cursor.execute(select_area)
	for row in cursor:
		area_list.append(area.Area(row))
	return area_list

def get_area_by_id(db,id_area):
	cursor=db.cursor()
	select_area="select * from Area where id='%d'"%(id_area)
	cursor.execute(select_area)
	row=cursor.fetchone()
	if(row==None):
		return None
	return area.Area(row)

def get_area_by_name(db,name_area):
	cursor=db.cursor()
	select_area="select * from Area where name='%s'"%(name_area)
	cursor.execute(select_area)
	row=cursor.fetchone()
	if(row==None):
		return None
	return area.Area(row)