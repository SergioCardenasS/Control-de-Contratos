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


new_process=process_avios.ProcessAvios([PROCESS_AVIOS_CREATE_ID,PROCESS_AVIOS_CREATE_NAME,AREA_DESARROLLO_ID])
new_process.insert(cursor)


db.commit()
db.close()
