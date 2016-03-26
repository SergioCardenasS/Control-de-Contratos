#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Import de Librerias
import sys
from PyQt4 import QtGui

#Import de Modulos
from constants import *
from controllers import controller_process, controller_contract

db=get_connection()
for i in controller_contract.get_contract_by_process_list(db,controller_process.get_process_by_id_area(db,AREA_DESARROLLO_ID)):
	print i.purchase_order