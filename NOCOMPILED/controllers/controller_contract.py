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
	select_contract="select * from Contract where id_contract='%d'"%(id_contract)
	cursor.execute(select_contract)
	row=cursor.fetchone()
	if(row==None):
		return None
	return contract.Contract(row)

def contract_is_equal(db,last_contract):
	cursor=db.cursor()
	select_contract="select * from Contract where id_contract='%d'"%(last_contract.id_contract)
	cursor.execute(select_contract)
	row=cursor.fetchone()
	if(row==None):
		return False
	new=contract.Contract(row)
	return (last_contract.id_process==new.id_process)

def get_contract_by_process_list(db,process_list,asc_desc=False):
	cursor=db.cursor()
	contract_list=[]
	select_contract="select * from Contract where id_process IN ('%d'"%(process_list[0].id_process)
	for index in range(1,len(process_list)):
		select_contract+=",'%d'"%(process_list[index].id_process)
	select_contract+=") ORDER BY mod_date"
	if(asc_desc):
                select_contract+=" DESC"
	cursor.execute(select_contract)
	for row in cursor:
		contract_list.append(contract.Contract(row))
	return contract_list

def get_contracts_by_number(db,contract_number):
	cursor=db.cursor()
	contract_list=[]
	select_contract="select * from Contract where contract_number LIKE '%s'"%(contract_number+"%")
	cursor.execute(select_contract)
	for row in cursor:
		contract_list.append(contract.Contract(row))
	return contract_list

def get_contracts_by_po(db,purchase_order):
	cursor=db.cursor()
	contract_list=[]
	select_contract="select * from Contract where purchase_order LIKE '%s'"%("%"+purchase_order+"%")
	cursor.execute(select_contract)
	for row in cursor:
		contract_list.append(contract.Contract(row))
	return contract_list

def get_contracts_by_client(db,special_contract):
	cursor=db.cursor()
	contract_list=[]
	select_contract="select * from Contract where special_contract LIKE '%s'"%("%"+special_contract+"%")
	cursor.execute(select_contract)
	for row in cursor:
		contract_list.append(contract.Contract(row))
	return contract_list
