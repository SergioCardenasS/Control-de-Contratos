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

cursor.execute("""CREATE TABLE CommentAvios
				(
				id_avios int,
				comment_number int,
				id_area int,
				text_comment TEXT,
				comment_date DATETIME
				)""")

cursor.execute("""CREATE INDEX CommentAviosIndex
				ON CommentAvios (id_avios)
				""")

db.commit()
db.close()
