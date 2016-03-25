#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

#DATABASE Configuration
DATABASE_HOST		= "127.0.0.1"
DATABASE_USER		= "root"
DATABASE_PASSWORD	= ""
DATABASE_NAME 		= "BASE_SEGUIMIENTO"

def get_connection():
	return MySQLdb.connect(DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME)

#CONTRACTS TYPE
CONTRACT_TYPE_FIRME			= 0
CONTRACT_TYPE_PROVISIONAL	= 1

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
