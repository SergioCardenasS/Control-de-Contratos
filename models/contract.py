#Import de Librerias
import sys
import datetime

#Import de Modulos
BASE_DIR='..'
sys.path.insert(0,BASE_DIR)
from constants import *

#Clase Contract:
#Contiene su PO, Numero de Conrato, el estado en el
#que se encuentra y su fecha de inicio y ultima
#modificacio, incluyendo el numero de iteracion en
#la que se encuentra.
class Contract:
	#Indice del Contrato
	id_contract			= 0
	#Orden de Compra del Contrato
	purchase_order		= ""
	#Numero del Contrato
	contract_number		= 0
	#Indice del Proceso (Estado)
	id_process			= 0
	#Tipo del Contrato
	contract_type		= CONTRACT_TYPE_PROVISIONAL
	#Fecha Inicial (creacion del Control del Contrato)
	init_date			= datetime.datetime(1,1,1,0,0,0)
	#Fecha de Ultima Modificacion (Ultima modificacion del Control del Contrato)
	mod_date			= datetime.datetime(1,1,1,0,0,0)
	#Numero de Iteracion del Control del Contrato
	iteration_number	= 0
	#Constructor de la clase Contrato, recive una fila de la tabla de la bases de datos, como una lista.
	def __init__(self, row_contract):
		self.id_contract		= row_contract[0]
		self.purchase_order		= row_contract[1]
		self.contract_number	= row_contract[2]
		self.id_process			= row_contract[3]
		self.contract_type		= row_contract[4]
		self.init_date			= row_contract[5]
		self.mod_date			= row_contract[6]
		self.iteration_number	= row_contract[7]