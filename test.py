#!C:\Python27\python
import MySQLdb
from constants import DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME

db=MySQLdb.connect(DATABASE_HOST,DATABASE_USER,DATABASE_PASSWORD,DATABASE_NAME)
cursor=db.cursor()
cursor.execute("select 'hello world'")
value=cursor.fetchone()
print value