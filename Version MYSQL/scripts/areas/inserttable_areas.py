#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4 import QtGui

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import area

db=get_connection()
cursor=db.cursor()

new_area=area.Area([AREA_CONTROL_ID,AREA_CONTROL_NAME,AREA_CONTROL_PASS])
new_area.insert(cursor)

new_area=area.Area([AREA_COMERCIAL_ID,AREA_COMERCIAL_NAME,AREA_COMERCIAL_PASS])
new_area.insert(cursor)

new_area=area.Area([AREA_ABASTECIMIENTOS_ID,AREA_ABASTECIMIENTOS_NAME,AREA_ABASTECIMIENTOS_PASS])
new_area.insert(cursor)

new_area=area.Area([AREA_DESARROLLO_ID,AREA_DESARROLLO_NAME,AREA_DESARROLLO_PASS])
new_area.insert(cursor)

new_area=area.Area([AREA_INGENIERIA_ID,AREA_INGENIERIA_NAME,AREA_INGENIERIA_PASS])
new_area.insert(cursor)

new_area=area.Area([AREA_PLANIFICACION_ID,AREA_PLANIFICACION_NAME,AREA_PLANIFICACION_PASS])
new_area.insert(cursor)

db.commit()
db.close()
