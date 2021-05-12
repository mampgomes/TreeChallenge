BOMBA = False
CLEANSE = False
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin"
)

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
    mycursor = dbcon.cursor()
    mycursor.execute("""
        SELECT *
        FROM information_schema.tables
        WHERE table_name = '{value}'
        """.format(value = tablename.replace('\'', '\'\'')))
    if mycursor.fetchone() != None:
    		mycursor.close()
    		return True
	
    mycursor.close()
    return False

def checkRecordExists(dbcon, tablename, name):
    mycursor = dbcon.cursor()
    mycursor.execute("""
        SELECT *
        FROM {table}
        WHERE name = '{value}'
        """.format(table = tablename, value = name))
    if mycursor.fetchone() != None:
    		mycursor.close()
    		return True

    mycursor.close()
    return False

def addTable(dbcon, tablename):
	mycursor = dbcon.cursor()
	if checkTableExists(dbcon, tablename):
		return False
	sql = ("CREATE TABLE {value} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE KEY)").format(value = tablename)
	mycursor.execute(sql)

	dbcon.commit()

	print(mycursor.rowcount, "record inserted.")

	return True

def addRecord(dbcon, tablename, name):
	mycursor = dbcon.cursor()
	if not(checkTableExists(dbcon, tablename)):
		return False
	if checkRecordExists(dbcon, tablename, name):
		return False
	val = "'{value}'".format(value = name)
	sql = "INSERT INTO {table} (name) VALUES ({value})".format(table = tablename, value = val)
	mycursor.execute(sql)

	dbcon.commit()

	print(mycursor.rowcount, "record inserted.")

	return True

def deleteAll(dbcon, tablename):
	mycursor = dbcon.cursor()
	if not(checkTableExists(dbcon, tablename)):
		return False
	sql = "DELETE FROM {table}".format(table = tablename)
	mycursor.execute(sql)

	dbcon.commit()

	print(mycursor.rowcount, "record deleted.")

	return True

def deleteRecord(dbcon, tablename, name):
	mycursor = dbcon.cursor()
	if not(checkRecordExists(dbcon, tablename, name)):
		return False
	sql = "DELETE FROM {table} WHERE name = '{value}'".format(table = tablename, value = name)
	mycursor.execute(sql)

	dbcon.commit()

	print(mycursor.rowcount, "record of {value} deleted.".format(value = name))

	return True

def printTable(dbcon, tablename):
	mycursor = dbcon.cursor()
	if not(checkTableExists(dbcon, tablename)):
		return False
	sql = "SELECT * FROM {table}".format(table = tablename)
	mycursor.execute(sql)

	for x in mycursor:
  		print(x)

	return True

def SeLfDeStRuCtSeQuEnCe(dbcon):
	mycursor = dbcon.cursor()

	sql = "DROP DATABASE mydatabase".format(table = tablename)
	mycursor.execute(sql)

	mycursor.close
	return True

mycursor = mydb.cursor()

if not(checkDatabase(mydb, "mydatabase")):
	#create database
	mycursor.execute("CREATE DATABASE mydatabase")
	mydb.database="mydatabase"

	if not(checkTableExists(mydb,"root")):
		#create table root
		mycursor.execute("CREATE TABLE root (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) UNIQUE KEY)")
else:
	mydb  = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin",
  database="mydatabase"
)


for i in range(5):
	if i==0:
		tablename = "root"
	else:
		tablename = "cat{num}".format(num = i)
	tablename = "cat{num}".format(num = i)
	for j in range(5):
		name = "cat{num}".format(num = j+1)
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


if CLEANSE: 
	deleteAll(mydb, tablename)

printTable(mydb, tablename)
if BOMBA:
	SeLfDeStRuCtSeQuEnCe(mydb)
else:
	mycursor.close