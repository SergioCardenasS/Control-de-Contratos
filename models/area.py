# La clase area almacenara todas las areas dentro de la empresa
class Area():
	# id del area sera la Primary Key y auto-incrementable habran pocas pero podremos agregar mas si se desea
	id_area 	= 0
	# nombre del area dentro de la empresa que tambien servira como su id para autentificarse
	name 		= ""
	# el password o contraseña sera para poder logearse en cada unas de las areas
	password 	= ""
	def  __init__(self, name, password):
		self.name 		= name
		self.password 	= password