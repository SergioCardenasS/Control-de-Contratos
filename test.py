#Import de Librerias
import sys
from PyQt4 import QtGui
import MySQLdb

#Import de Modulos
from constants import *

db=MySQLdb.connect(DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME)
cursor=db.cursor()
cursor.execute("select 'hello world'")
value=cursor.fetchone()

def main():
	app=QtGui.QApplication(sys.argv)
	w=QtGui.QWidget()
	w.resize(200,200)
	w.move(300,300)
	w.setWindowTitle(value[0])
	w.show()
	sys.exit(app.exec_())

main()

#sql="Select * From productos WHERE Nombre LIKE '%s'" %('%'+bus+'%')
#cursor.execute(sql)
#resultado=cursor.fetchall()
#prod="insert into productos values('null','%s','%s','%s','%s','%s','%s')"%(nombre,descri,version,imagen,linkexe,linkrar)
#cursor.execute(prod)
#db.commit()
