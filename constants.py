#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time

#DATABASE Configuration
DATABASE_HOST		= "127.0.0.1"
DATABASE_USER		= "root"
DATABASE_PASSWORD	= ""
DATABASE_NAME 		= "BASE_SEGUIMIENTO"

def get_connection():
	return MySQLdb.connect(DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME)

#TIME
def get_time_str():
	return time.strftime('%Y-%m-%d %H:%M:%S')

#UNICODE
def str_is_invalid(str_u):
	for char_u in unicode(str_u):
		if(ord(char_u)>=128 or char_u=="'"):
			return True
	return False

def is_invalid_contract_number(contract_number):
	if(str_is_invalid(contract_number)):
		return True
	for char_u in str(contract_number):
		if(ord(char_u)<48 or ord(char_u)>57):
			return True
	return False

#CONTRACTS TYPE
CONTRACT_TYPE_FIRME				= 0
CONTRACT_TYPE_PROVISIONAL		= 1
CONTRACT_TYPE_FIRME_NAME		= "Firme"
CONTRACT_TYPE_PROVISIONAL_NAME	= "Provisional"

def get_str_contract_type(type):
	if(type==CONTRACT_TYPE_FIRME):
		return CONTRACT_TYPE_FIRME_NAME
	return CONTRACT_TYPE_PROVISIONAL_NAME

#PROCESS
PROCESS_SET_PO_ID				= 1
PROCESS_SET_PO_NAME				= "Colocar PO"
PROCESS_SET_CODE_ID				= 2
PROCESS_SET_CODE_NAME			= "Creacion de Codigos"
PROCESS_SAVE_PRECONTRACT_ID		= 3
PROCESS_SAVE_PRECONTRACT_NAME	= "Grabar Precontrato"
PROCESS_SET_WEIGHT_ID			= 4
PROCESS_SET_WEIGHT_NAME			= "Colocar Pesos"
PROCESS_YAM_STATUS_ID			= 5
PROCESS_YAM_STATUS_NAME			= "Estado del Hilado"
PROCESS_SET_ACCESS_ID			= 6
PROCESS_SET_ACCESS_NAME			= "Brindar Permiso para el Hilado"
PROCESS_SET_DATES_ID			= 7
PROCESS_SET_DATES_NAME			= "Brindar Fechas"
PROCESS_ACCEPT_DATES_ID			= 8
PROCESS_ACCEPT_DATES_NAME		= "Aceptar Fechas"
PROCESS_ACTIVATE_CONTRACT_ID	= 9
PROCESS_ACTIVATE_CONTRACT_NAME	= "Activar Contrato"
PROCESS_COMPLETED_ID			= 10
PROCESS_COMPLETED_NAME			= "Completado"

def get_str_name_from_id_process(id_process):
	if(id_process==PROCESS_SET_PO_ID):
		return PROCESS_SET_PO_NAME
	elif(id_process==PROCESS_SET_CODE_ID):
		return PROCESS_SET_CODE_NAME
	elif(id_process==PROCESS_SAVE_PRECONTRACT_ID):
		return PROCESS_SAVE_PRECONTRACT_NAME
	elif(id_process==PROCESS_SET_WEIGHT_ID):
		return PROCESS_SET_WEIGHT_NAME
	elif(id_process==PROCESS_YAM_STATUS_ID):
		return PROCESS_YAM_STATUS_NAME
	elif(id_process==PROCESS_SET_ACCESS_ID):
		return PROCESS_SET_ACCESS_NAME
	elif(id_process==PROCESS_SET_DATES_ID):
		return PROCESS_SET_DATES_NAME
	elif(id_process==PROCESS_ACCEPT_DATES_ID):
		return PROCESS_ACCEPT_DATES_NAME
	elif(id_process==PROCESS_ACTIVATE_CONTRACT_ID):
		return PROCESS_ACTIVATE_CONTRACT_NAME
	return PROCESS_COMPLETED_NAME

#AREAS
AREA_CONTROL_ID				= 1
AREA_CONTROL_NAME			= "Administrador"
AREA_CONTROL_PASS			= "Administrador"
AREA_COMERCIAL_ID			= 2
AREA_COMERCIAL_NAME			= "Comercial"
AREA_COMERCIAL_PASS			= "Comercial"
AREA_ABASTECIMIENTOS_ID		= 3
AREA_ABASTECIMIENTOS_NAME	= "Abastecimientos"
AREA_ABASTECIMIENTOS_PASS	= "Abastecimientos"
AREA_DESARROLLO_ID			= 4
AREA_DESARROLLO_NAME		= "Desarrollo"
AREA_DESARROLLO_PASS		= "Desarrollo"
AREA_INGENIERIA_ID			= 5
AREA_INGENIERIA_NAME		= "Ingenieria"
AREA_INGENIERIA_PASS		= "Ingenieria"
AREA_PLANIFICACION_ID		= 6
AREA_PLANIFICACION_NAME		= "Planificacion"
AREA_PLANIFICACION_PASS		= "Planificacion"

def get_str_name_by_id_area(id_area):
	if(id_area==AREA_CONTROL_ID):
		return AREA_CONTROL_NAME
	elif(id_area==AREA_COMERCIAL_ID):
		return AREA_COMERCIAL_NAME
	elif(id_area==AREA_ABASTECIMIENTOS_ID):
		return AREA_ABASTECIMIENTOS_NAME
	elif(id_area==AREA_DESARROLLO_ID):
		return AREA_DESARROLLO_NAME
	elif(id_area==AREA_INGENIERIA_ID):
		return AREA_INGENIERIA_NAME
	elif(id_area==AREA_PLANIFICACION_ID):
		return AREA_PLANIFICACION_NAME
	return ""

#LOGIN_ERRORS
LOGIN_ERROR_NO_PASS_TYPED	= "No ha escrito ninguna contrasenha"
LOGIN_ERROR_BAD_PASS		= "Contrasenha Incorrecta"

#CREATE CONTRACT ERRORS
CREATE_CONTRACT_ERROR_NO_PO_TYPED	= "No ha escrito el PO"
INVALID_STR							= "Existe texto no valido"

#PROCESS ERRORS
ERROR_SET_CODE_CONTRACT_ERROR_NO_TYPED	= "No ha escrito Codigo del contrato"
ERROR_IS_A_FIRME_CONTRACT				= "El Contrato es Firme"
ERROR_IS_A_PROVISIONAL_CONTRACT			= "El Contrato es Provisional"
ERROR_MODIFICATE_CONTRACT				= "El Control ya ha sido Modificado"
ERROR_A_PROCESS_OPENED					= "Ya tiene Abierta una Opcion"

#TABLA
SIZE_COLUMNS			= 8
TITLE_ROWS				= "OP;Numero de Contrato; Nombre del proceso;Tipo del Contrato;Fecha Inicial;Ultima Modificacion;Iteracion;Comentarios"
SPLIT					= ";"
SIZE_COLUMNS_COMMENT	= 2
TITLE_ROWS_COMMENT		= "Area;Comentario"
SIZE_COLUMNS_END		= 2
TITLE_COLUMNS_END		= "Area;Comentario"
WIDTH_COLUMN_COMMENT	= 140