# La clase comentario guardara los comentarios del contrado que cada area colocara 
# en cada uno de los procesos
class Comment():
	# id del contrato no sera auto-incrementable ya que para cada contrato habran muchos comentarios
	id_contract 	= 0
	# el id del comentario tampoco sera auto-incrementable ya que cada contrato tendra su propio orden de comentarios
	comment_number 	= 0
	# el id del area sera una Foreigh Key
	id_area 		= 0
	# El comentario o texto
	comment 		= ""
	def __init__(self, id_contract, comment_number, id_area, comment):
		self.id_contract 	= id_contract
		self.comment_number = comment_number
		self.id_area 		= id_area
		self.comment 		= comment
