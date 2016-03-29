#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4 import QtGui

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import process

db=get_connection()
cursor=db.cursor()


new_process=process.Process([PROCESS_SET_PO_ID,PROCESS_SET_PO_NAME,AREA_COMERCIAL_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_SET_CODE_ID,PROCESS_SET_CODE_NAME,AREA_DESARROLLO_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_SAVE_PRECONTRACT_ID,PROCESS_SAVE_PRECONTRACT_NAME,AREA_COMERCIAL_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_SET_WEIGHT_ID,PROCESS_SET_WEIGHT_NAME,AREA_INGENIERIA_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_YAM_STATUS_ID,PROCESS_YAM_STATUS_NAME,AREA_ABASTECIMIENTOS_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_SET_ACCESS_ID,PROCESS_SET_ACCESS_NAME,AREA_COMERCIAL_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_SET_DATES_ID,PROCESS_SET_DATES_NAME,AREA_PLANIFICACION_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_ACCEPT_DATES_ID,PROCESS_ACCEPT_DATES_NAME,AREA_COMERCIAL_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_ACTIVATE_CONTRACT_ID,PROCESS_ACTIVATE_CONTRACT_NAME,AREA_COMERCIAL_ID])
new_process.insert(cursor)

new_process=process.Process([PROCESS_COMPLETED_ID,PROCESS_COMPLETED_NAME,AREA_CONTROL_ID])
new_process.insert(cursor)

db.commit()
db.close()
