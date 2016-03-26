#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import contract

def get_all_contracts(db):
	cursor=db.cursor()
	contract_list=[]
	select_contract="select * from Contract"
	cursor.execute(select_contract)
	for row in cursor:
		process_list.append(contract.Contract(row))
	return contract_list

def get_contracts_by_id(db,id_contract):
	cursor=db.cursor()
	select_contract="select * from Contract where id='%d'"%(id_contract)
	cursor.execute(select_contract)
	row=cursor.fetchone()
	if(row==None):
		return None
	return contract.Contract(row)

def get_contract_by_process_list(db,process_list):
	cursor=db.cursor()
	contract_list=[]
	select_contract="select * from Contract where id_process IN ('%d'"%(process_list[0].id_process)
	for index in range(1,process_list):
		select_contract+=",'%d'"%(process_list[index].id_process)
	select_contract+=")"
	cursor.execute(select_contract)
	for row in cursor:
		process_list.append(contract.Contract(row))
	return contract_list