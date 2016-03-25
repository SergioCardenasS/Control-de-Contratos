#Import de Librerias
import sys
from PyQt4 import QtGui
import MySQLdb

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *

db=MySQLdb.connect(DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME)
cursor=db.cursor()

cursor.execute("DROP TABLE Contract")

db.commit()
db.close()
