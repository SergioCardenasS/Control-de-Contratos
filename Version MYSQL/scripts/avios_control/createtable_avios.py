#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4 import QtGui

#Import de Modulos
BASE_DIR='../..'
sys.path.insert(0,BASE_DIR)
from constants import *

db=get_connection()
cursor=db.cursor()

cursor.execute("""CREATE TABLE Avios
				(
				id_avios int AUTO_INCREMENT PRIMARY KEY,
				id_contract int,
				id_process int,
				init_date DATETIME,
				mod_date DATETIME,
				llegada_date varchar(10)
				)""")

db.commit()
db.close()
