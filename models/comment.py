#!C:\Python27\python

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
	def __init__(self, row_comment):
		self.id_contract 	= row_comment[0]
		self.comment_number = row_comment[1]
		self.id_area 		= row_comment[2]
		self.comment 		= row_comment[3]
