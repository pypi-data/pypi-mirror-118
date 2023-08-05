import click
import os
import sqlite3
from sqlite3 import Error

def create_connection():
	primary_dir = "C:/restore"
	secondary_dir = "database/"
	path = os.path.join(primary_dir,secondary_dir)
	if not os.path.exists(path):
		os.makedirs(path)

	# connection and creation of database
	db = "sqlite.db"
	try:
		global conn
		conn = sqlite3.connect(path+db)
		global csr
		csr = conn.cursor()
		csr.execute('''CREATE TABLE IF NOT EXISTS users
					(service text, email text, password text)''')
	
	except Error as e:
		print(e)

def storePassword(service, email, password):
	create_connection()
	sql = "INSERT INTO users VALUES ('{}','{}','{}')".format(f"{service}",f"{email}",f"{password}")
	try:
		csr.execute(sql)
		conn.commit()
	except Error as e:
		click.echo(e)

def findDataByService(service):
	create_connection()
	sql = "SELECT * FROM users WHERE service = ('{}')".format(f"{service}")
	try:	
		csr.execute(sql)
		data = csr.fetchall()
		for row in data:
			click.echo(row)
	
	except Error as e:
		click.echo(e)