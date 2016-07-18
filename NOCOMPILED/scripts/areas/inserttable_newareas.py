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

new_area=area.Area([AREA_LOGISTICA_ID,AREA_LOGISTICA_NAME,AREA_LOGISTICA_PASS])
new_area.insert(cursor)

new_area=area.Area([AREA_CALIDAD_ID,AREA_CALIDAD_NAME,AREA_CALIDAD_PASS])
new_area.insert(cursor)

db.commit()
db.close()
