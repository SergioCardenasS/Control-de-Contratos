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

cursor.execute("""CREATE TABLE Area
				(
				id_area int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
				name varchar(30),
				password varchar(30)
				)""")

db.commit()
db.close()
