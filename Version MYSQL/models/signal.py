#!/usr/bin/env python
# -*- coding: utf-8 -*-

class SignalAvios:
	id_signal		= 0
	id_avios		= 0
	type			= 0
	comment			= ""
	def __init__(self, row_signal):
		self.id_signal		= row_signal[0]
		self.id_avios		= row_signal[1]
		self.type			= row_signal[2]
		self.comment		= row_signal[3]

	def insert(self,cursor_db):
		insert_code_signal="""INSERT INTO SignalAvios
								(id_avios,type,comment)
								values('%d','%d','%s'
								)"""%(self.id_avios,
										self.type,
										self.comment)
		cursor_db.execute(insert_code_signal)
		cursor_db.execute("select MAX(id_signal) from SignalAvios")
		for row in cursor_db:
			self.id_signal=row[0]
		return True
