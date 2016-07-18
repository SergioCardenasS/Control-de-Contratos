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

cursor.execute("""CREATE TABLE Contract
				(
				id_contract int IDENTITY PRIMARY KEY,
				purchase_order varchar(30),
				contract_number varchar(10),
				id_process int,
				contract_type BIT,
				init_date DATETIME,
				mod_date DATETIME,
				iteration_number int,
				special_contract varchar(10)
				)""")

db.commit()
db.close()
