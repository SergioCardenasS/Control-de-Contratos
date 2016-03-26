#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4 import QtGui

#Import de Modulos
from constants import *
from controllers import controller_contract

db=get_connection()
lista=controller_contract.get_all_contracts(db)
for i in lista:
	print i.name
db.close()
