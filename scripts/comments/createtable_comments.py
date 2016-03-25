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

cursor.execute("""CREATE TABLE Comment
				(
				id_contract int,
				FOREIGN KEY (id_contract) REFERENCES Contract(id_contract),
				comment_number int,
				id_area int,
				FOREIGN KEY (id_area) REFERENCES Area(id_area),
				text_comment TEXT
				)""")

db.commit()
db.close()
