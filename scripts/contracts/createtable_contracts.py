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

cursor.execute("""CREATE TABLE Contract
				(
				id_contract int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
				purchase_order varchar(30),
				contract_number varchar(10),
				id_process int UNSIGNED,
				contract_type boolean,
				init_date DATETIME,
				mod_date DATETIME,
				iteration_number int UNSIGNED
				)""")

db.commit()
db.close()
