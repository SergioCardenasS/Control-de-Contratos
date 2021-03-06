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
				comment_number int,
				id_area int,
				text_comment TEXT,
				comment_date DATETIME
				)""")

cursor.execute("""CREATE INDEX CommentIndex
				ON Comment (id_contract)
				""")

db.commit()
db.close()
