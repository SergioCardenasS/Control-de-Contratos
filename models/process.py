#Clase Process:
#Contiene su propio nombre y el id del area
#que esta acargo de este proceso.
class Process:
	#Indice del proceso
	id_process	= 0
	#Nombre del Proceso
	name		= ""
	#Id del area que trabaja este proceso
	id_area		= 0
	#Constructor de la clase Process que recive una fila de la tabla de la bases de datos, como una lista.
	def __init__(self,row_process):
		self.id_process	= row_process[0]
		self.name		= row_process[1]
		self.id_area	= row_process[2]