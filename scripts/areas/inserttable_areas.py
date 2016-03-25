#Import de Librerias
import sys
from PyQt4 import QtGui
import MySQLdb

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *
from models import area

db=MySQLdb.connect(DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME)
cursor=db.cursor()

new_area=area.Area([0,AREA_CONTROL_NAME,AREA_CONTROL_PASS])
new_area.insert(cursor)
new_area=area.Area([0,AREA_COMERCIAL_NAME,AREA_COMERCIAL_PASS])
new_area.insert(cursor)
new_area=area.Area([0,AREA_ABASTECIMIENTOS_NAME,AREA_ABASTECIMIENTOS_PASS])
new_area.insert(cursor)
new_area=area.Area([0,AREA_DESARROLLO_NAME,AREA_DESARROLLO_PASS])
new_area.insert(cursor)
new_area=area.Area([0,AREA_INGENIERIA_NAME,AREA_INGENIERIA_PASS])
new_area.insert(cursor)
new_area=area.Area([0,AREA_PLANIFICACION_NAME,AREA_PLANIFICACION_PASS])
new_area.insert(cursor)

db.commit()
db.close()
