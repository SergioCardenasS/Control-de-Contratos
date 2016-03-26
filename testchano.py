#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4 import QtGui

#Import de Modulos
from constants import *
from controllers import controller_process

db=get_connection()
lista=controller_process.get_all_process(db)
id=1
for i in lista:
	id+=i.id_process
print id
db.close()
