'''
@author: Marco André de Matos Pereira Gomes
@Date: 13/05/2021
'''
BOMBA = False
CLEANSE = False
import mysql.connector

def connector(hostname, username, passw, dataname = ''):
	mydb = mysql.connector.connect(
  	host=hostname,
  	user=username,
  	password=passw
	)

	mycursor = mydb.cursor()

	if not(checkDatabase(mydb, dataname)):
		#create database
		mycursor.execute("CREATE DATABASE {name}".format(name = dataname, ))
		
		mydb  = mysql.connector.connect(
	  		host=hostname,
	  		user=username,
	  		password=passw,
	  		database=dataname
		)

		mycursor = mydb.cursor()

		if not(checkTableExists(mydb,"root")):
			#create table root
			mycursor.execute("CREATE TABLE root (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE KEY)")
		
		if not(checkTableExists(mydb,"control")):
			#create table root
			mycursor.execute("CREATE TABLE control (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE KEY)")

	else:
		mydb  = mysql.connector.connect(
	  		host=hostname,
	  		user=username,
	  		password=passw,
	  		database=dataname
		)
	return mydb

def checkDatabase(dbcon, databaseName):
	found_flag = False
	mycursor = dbcon.cursor()

	mycursor.execute("SHOW DATABASES")

	for x in mycursor:
		if databaseName == x[0]:
			found_flag = True

	mycursor.close()
	return found_flag

def checkTableExists(dbcon, tablename):
	tablename = ''.join(e for e in tablename if e.isalnum())
	mycursor = dbcon.cursor()
	val = (tablename, )
	sql = """SELECT * FROM information_schema.tables WHERE table_name = %s;"""
	mycursor.execute(sql, val)
	if mycursor.fetchone() != None:
		mycursor.close()
		return True
	
	mycursor.close()
	return False

def checkRecordExistsTable(dbcon, tablename, name):
	tablename = ''.join(e for e in tablename if e.isalnum())
	name = ''.join(e for e in name if e.isalnum())
	mycursor = dbcon.cursor()
	val = (name, )
	sql ="""
        SELECT *
        FROM {table}
        WHERE name = %s;
        """.format(table = tablename, )
	mycursor.execute(sql, val)
	if mycursor.fetchone() != None:
		mycursor.close()
		return True

	mycursor.close()
	return False

def getTables(dbcon):
	mycursor = dbcon.cursor()
	sql = ("SHOW TABLES;")
	mycursor.execute(sql)
	return mycursor.fetchall()

def getRecords(dbcon, tablename):
	tablename = ''.join(e for e in tablename if e.isalnum())
	mycursor = dbcon.cursor()
	if not(checkTableExists(dbcon, tablename)):
		return False
	sql = "SELECT * FROM {table}".format(table = tablename)
	mycursor.execute(sql)
	return mycursor.fetchall()

def getRecord(dbcon, tablename, name):
	tablename = ''.join(e for e in tablename if e.isalnum())
	mycursor = dbcon.cursor()
	if not(checkTableExists(dbcon, tablename)):
		return False
	val = (name, )
	sql ="""
        SELECT *
        FROM {table}
        WHERE name = %s;
        """.format(table = tablename, )
	mycursor.execute(sql, val)
	return mycursor.fetchall()

def addTable(dbcon, tablename):
	tablename = ''.join(e for e in tablename if e.isalnum())
	mycursor = dbcon.cursor()
	if not (checkRecordExistsTable(dbcon, "control", tablename)):
		return False
	if checkTableExists(dbcon, tablename):
		return False
	sql = ("CREATE TABLE {value} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE KEY)").format(value = tablename)
	mycursor.execute(sql)

	dbcon.commit()

	print(mycursor.rowcount, "record inserted.")

	return True

def addRecord(dbcon, tablename, name):
	tablename = ''.join(e for e in tablename if e.isalnum())
	name = ''.join(e for e in name if e.isalnum())
	mycursor = dbcon.cursor()
	if checkRecordExistsTable(dbcon, "control", name):
		return False
	if not(checkTableExists(dbcon, tablename)):
		return False
	if checkRecordExistsTable(dbcon, tablename, name):
		return False
	val = (name, )
	sql = "INSERT INTO {table} (name) VALUES (%s)".format(table = tablename, value = val)
	mycursor.execute(sql, val)

	sql = "INSERT INTO {table} (name) VALUES (%s)".format(table = "control", value = val)
	mycursor.execute(sql, val)

	dbcon.commit()

	print(mycursor.rowcount, "record inserted.")

	return True

def deleteAll(dbcon, tablename):
	tablename = ''.join(e for e in tablename if e.isalnum())
	mycursor = dbcon.cursor()
	if not(checkTableExists(dbcon, tablename)):
		return False
	sql = "DROP TABLE {table}".format(table = tablename)
	mycursor.execute(sql)

	dbcon.commit()

	print(mycursor.rowcount, "record deleted.")

	return True

def deleteRecord(dbcon, tablename, name):
	tablename = ''.join(e for e in tablename if e.isalnum())
	name = ''.join(e for e in name if e.isalnum())
	mycursor = dbcon.cursor()
	if not(checkRecordExistsTable(dbcon, "control", name)):
		return False
	if not(checkRecordExistsTable(dbcon, tablename, name)):
		return False

	val = (name, )
	sql = "DELETE FROM {table} WHERE name = %s".format(table = tablename)
	mycursor.execute(sql, val)

	dbcon.commit()

	print(mycursor.rowcount, "record of {value} deleted.".format(value = name))

	return True

def deleteCascade(dbcon, tablename):
	tablename = ''.join(e for e in tablename if e.isalnum())
	mycursor = dbcon.cursor()
	if checkTableExists(dbcon, tablename):
		sql = "SELECT * FROM {table}".format(table = tablename)
		mycursor.execute(sql)

		for child in mycursor:
			result = deleteCascade(dbcon, child[1])
			if result:
				deleteAll(dbcon, tablename)


	val = (tablename, )
	records = ["root"]

	for tablename in records:
		if checkTableExists(dbcon, tablename):
			sql ="""
				SELECT *
				FROM {table}
				WHERE name = %s;
				""".format(table = tablename, )
			mycursor.execute(sql, val)
			if mycursor.fetchone() != None:
				deleteRecord(dbcon, tablename, val[0])
				deleteRecord(dbcon, "control", val[0])
				mycursor.close()
				return True
			else:
				sql ="""
				SELECT *
				FROM {table};
				""".format(table = tablename, )
				mycursor.execute(sql)
				support = mycursor.fetchall()
				for name in support:
					records.extend([name[1]])


	mycursor.close()
	return False

def printTable(dbcon, tablename):
	tablename = ''.join(e for e in tablename if e.isalnum())
	mycursor = dbcon.cursor()
	if not(checkTableExists(dbcon, tablename)):
		return False
	sql = "SELECT * FROM {table}".format(table = tablename)
	mycursor.execute(sql)
	print(tablename)
	for x in mycursor:
  		print(x)

	return True

def SeLfDeStRuCtSeQuEnCe(dbcon):
	mycursor = dbcon.cursor()

	sql = "DROP DATABASE mydatabase".format(table = tablename)
	mycursor.execute(sql)

	mycursor.close
	return True


if __name__ == "__main__":

	mydb = connector("localhost", "root", "admin", "mydatabase")

	for i in range(5):
		if i==0:
			tablename = "root"
		else:
			tablename = "cat{num}".format(num = i)
		for j in range(5):
			name = "cat{num}".format(num = i*100+j+1)
			if not(addTable(mydb, tablename)):
				print("Didnt create table %s", (tablename))
			if not(addRecord(mydb, tablename, name)):
				print("Didnt add %s to %s", (name, tablename))

	#show tables
	#mycursor.execute("SHOW TABLES")
	for i in range(5):
		if i==0:
			tablename = "root"
		else:
			tablename = "cat{num}".format(num = i)
		printTable(mydb, tablename)

	addRecord(mydb, "cat1", "cat900")
	addTable(mydb, "cat900")
	addRecord(mydb, "cat900", "cat901")
	addTable(mydb, "cat901")
	addRecord(mydb, "cat901", "cat902")
	printTable(mydb, "cat900")
	printTable(mydb, "cat901")
	deleteCascade(mydb,"cat901")
	printTable(mydb, "cat900")
	printTable(mydb, "cat901")
	printTable(mydb, "cat902")
	tabelas = getTables(mydb)
	for tabela in tabelas:
		getRecords(mydb, tabela)
	if CLEANSE: 
		deleteAll(mydb, tablename)

	#printTable(mydb, tablename)
	if BOMBA:
		SeLfDeStRuCtSeQuEnCe(mydb)