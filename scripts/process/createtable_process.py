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

cursor.execute("""CREATE TABLE Process
				(
				id_process int UNSIGNED PRIMARY KEY,
				name varchar(50),
				id_area int UNSIGNED,
				FOREIGN KEY (id_area) REFERENCES Area(id_area)
				)""")

db.commit()
db.close()
