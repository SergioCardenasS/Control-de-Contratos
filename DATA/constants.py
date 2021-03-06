#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymssql
import time
import datetime
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from BDconf import *

def get_connection():
	try:
		return pymssql.connect(DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME)
	except pymssql.Error as err:
		QMessageBox.warning(None, 'Error',"Error al Conectar con la Base De Datos", QMessageBox.Ok)
		exit()

#TIME
def get_time_str():
	return time.strftime('%Y-%m-%d %H:%M:%S')

def time_pass_one_day(str_u,days_time=0):
	mod_date=datetime.datetime.strptime(str_u,"%Y-%m-%d %H:%M:%S")
	actual_date=datetime.datetime.now()
	return (abs((actual_date-mod_date).days))>days_time

#UNICODE
def str_is_invalid(str_u):
	for char_u in unicode(str_u):
		if(ord(char_u)>=128 or char_u=="'"):
			return True
	return False

def is_invalid_contract_number(contract_number):
	if(str_is_invalid(contract_number)):
		return True
	for char_u in unicode(contract_number):
		if(ord(char_u)<48 or ord(char_u)>57):
			return True
	return False

#CONTRACTS TYPE
CONTRACT_TYPE_FIRME				= 0
CONTRACT_TYPE_PROVISIONAL		= 1
CONTRACT_TYPE_FIRME_NAME		= "Firme"
CONTRACT_TYPE_PROVISIONAL_NAME	= "Provisional"

#SIGNAL TYPE
SYGNAL_TYPE_PARCIAL				= 0
SYGNAL_TYPE_TOTAL				= 1

def get_str_contract_type(type):
	if(type==CONTRACT_TYPE_FIRME):
		return CONTRACT_TYPE_FIRME_NAME
	return CONTRACT_TYPE_PROVISIONAL_NAME

#PROCESS
PROCESS_SET_PO_ID				= 1
PROCESS_SET_PO_NAME				= "Colocar PO"
PROCESS_SET_CODE_ID				= 2
PROCESS_SET_CODE_NAME			= "Revision de PO y Tipo"
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
PROCESS_REVIEW_DATA_ID			= 11
PROCESS_REVIEW_DATA_NAME		= "Revisar Datos del Contrato"

#PROCESS AVIOS
PROCESS_AVIOS_ACTIVATE_ID		= 1
PROCESS_AVIOS_ACTIVATE_NAME		= "Activar Control"
PROCESS_AVIOS_FIN_DES_ID		= 2
PROCESS_AVIOS_FIN_DES_NAME		= "Finalizar Trabajo Desarrollo"
PROCESS_AVIOS_FIN_ING_ID		= 3
PROCESS_AVIOS_FIN_ING_NAME		= "Finalizar Trabajo Ingenieria"
PROCESS_AVIOS_FIN_LOG_ID		= 4
PROCESS_AVIOS_FIN_LOG_NAME		= "Finalizar Trabajo Logistica"
PROCESS_AVIOS_LLEGADA_ID		= 5
PROCESS_AVIOS_LLEGADA_NAME		= "Llegada de Avios"
PROCESS_AVIOS_FIN_CONTROL_ID	= 6
PROCESS_AVIOS_FIN_CONTROL_NAME	= "Finalizar Control"
PROCESS_AVIOS_COMPLETED_ID		= 7
PROCESS_AVIOS_COMPLETED_NAME	= "Completado"

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
	elif(id_process==PROCESS_REVIEW_DATA_ID):
		return PROCESS_REVIEW_DATA_NAME
	return PROCESS_COMPLETED_NAME

def get_str_name_from_id_process_avios(id_process):
	if(id_process==PROCESS_AVIOS_ACTIVATE_ID):
		return PROCESS_AVIOS_ACTIVATE_NAME
	elif(id_process==PROCESS_AVIOS_FIN_DES_ID):
		return PROCESS_AVIOS_FIN_DES_NAME
	elif(id_process==PROCESS_AVIOS_FIN_ING_ID):
		return PROCESS_AVIOS_FIN_ING_NAME
	elif(id_process==PROCESS_AVIOS_FIN_LOG_ID):
		return PROCESS_AVIOS_FIN_LOG_NAME
	elif(id_process==PROCESS_AVIOS_LLEGADA_ID):
		return PROCESS_AVIOS_LLEGADA_NAME
	elif(id_process==PROCESS_AVIOS_FIN_CONTROL_ID):
		return PROCESS_AVIOS_FIN_CONTROL_NAME
	return PROCESS_AVIOS_COMPLETED_NAME

#AREAS
AREA_CONTROL_ID				= 1
AREA_CONTROL_NAME			= "Control"
AREA_CONTROL_PASS			= "Control"
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
AREA_LOGISTICA_ID			= 7
AREA_LOGISTICA_NAME			= "Logistica"
AREA_LOGISTICA_PASS			= "Logistica"
AREA_CALIDAD_ID				= 8
AREA_CALIDAD_NAME			= "Control de Calidad"
AREA_CALIDAD_PASS			= "Calidad"

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
	elif(id_area==AREA_LOGISTICA_ID):
		return AREA_LOGISTICA_NAME
	elif(id_area==AREA_CALIDAD_ID):
		return AREA_CALIDAD_NAME
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
ERROR_A_ADMIN_OPENED					= "Ya tiene Abierta una ventana de Status General"

#TABLA
SIZE_COLUMNS			= 9
TITLE_ROWS				= "OP;Numero de Contrato;Cliente; Nombre del proceso;Tipo del Contrato;Fecha Inicial;Ultima Modificacion;Iteracion;Comentarios"
SPLIT					= ";"
SIZE_COLUMNS_COMMENT	= 3
TITLE_ROWS_COMMENT		= "Area;Fecha;Comentario"
SIZE_COLUMNS_END		= 3
TITLE_COLUMNS_END		= "Area;Fecha;Comentario"
WIDTH_COLUMN_COMMENT	= 140
TIMER_SEC				= 10
TIMER_EVENT				= TIMER_SEC*1000
ColorGRAY				= 240

#TITLE
TITLE_APP				= "Sistema de Respuestas - "
CONTROL_TITLE			= "Control"
COMERCIAL_TITLE			= "Comercial"
DESARROLLO_TITLE		= "Desarrollo"
ABASTECIMIENTOS_TITLE	= "Abastecimientos"
PLANIFICACION_TITLE		= "Planificacion"
INGENIERIA_TITLE		= "Ingenieria"
LOGISTICA_TITLE			= "Logistica"
CALIDAD_TITLE			= "Control de Calidad"




#Avios Text
AVIOS_TITLE								= "Avios - "
CONTROL_AVIOS_BUTTON					= "Control de Avios"
CONTROL_AVIOS_TITLE						= "Control de Avios"
AVIOS_TABLE_LIST						= ["PO","Contrato","Cliente","Proceso","Fecha Inicial","Fecha de Modificacion","Fecha de Llegada","Opcion"]
ERROR_A_AVIOS_OPENED					= "Avios ya se encuentra abierto"
ERROR_MODIFICATE_AVIOS					= "Alguien ya modifico este Control"

#Avios Valores
SIZE_COLUMNS_AVIOS						= 8
MORE_YEARS								= 5
