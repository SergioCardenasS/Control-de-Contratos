#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4 import QtGui

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import process_avios

db=get_connection()
cursor=db.cursor()


new_process=process_avios.ProcessAvios([PROCESS_AVIOS_ACTIVATE_ID,PROCESS_AVIOS_ACTIVATE_NAME,AREA_DESARROLLO_ID])
new_process.insert(cursor)

new_process=process_avios.ProcessAvios([PROCESS_AVIOS_FIN_DES_ID,PROCESS_AVIOS_FIN_DES_NAME,AREA_DESARROLLO_ID])
new_process.insert(cursor)

new_process=process_avios.ProcessAvios([PROCESS_AVIOS_FIN_ING_ID,PROCESS_AVIOS_FIN_ING_NAME,AREA_INGENIERIA_ID])
new_process.insert(cursor)

new_process=process_avios.ProcessAvios([PROCESS_AVIOS_FIN_LOG_ID,PROCESS_AVIOS_FIN_LOG_NAME,AREA_LOGISTICA_ID])
new_process.insert(cursor)

new_process=process_avios.ProcessAvios([PROCESS_AVIOS_LLEGADA_ID,PROCESS_AVIOS_LLEGADA_NAME,AREA_LOGISTICA_ID])
new_process.insert(cursor)

new_process=process_avios.ProcessAvios([PROCESS_AVIOS_FIN_CONTROL_ID,PROCESS_AVIOS_FIN_CONTROL_NAME,AREA_CALIDAD_ID])
new_process.insert(cursor)

new_process=process_avios.ProcessAvios([PROCESS_AVIOS_COMPLETED_ID,PROCESS_AVIOS_COMPLETED_NAME,AREA_CONTROL_ID])
new_process.insert(cursor)



db.commit()
db.close()
