'''
@author: Marco André de Matos Pereira Gomes
@Date: 13/05/2021
'''
import Database
import Tree

def startUp():
	mydb = Database.connector("localhost", "root", "admin", "mydatabase")
	tree = Tree.Tree(0, "root")
	tables = Database.getTables(mydb)

	tables.remove(("root", ))
	tables.remove(("control", ))

	for record in Database.getRecords(mydb, "root"):
		tree.add_node(record[0], record[1])

	while len(tables) > 0:
		for table in tables:
			if tree.find_node(table[0]) != None:
				for record in Database.getRecords(mydb, table[0]):
					tree.add_node(record[0], record[1], table[0])
				tables.remove(table)
	return (tree,mydb)

def add(data):
	record = input('Record to add: ')
	table = input('Table name:')
	father = data[0].find_node(table)
	if (father != None):
		Database.addTable(data[1], table)
		if(Database.addRecord(data[1], table, record)):
			record = Database.getRecord(data[1], table, record)[0]
			data[0].add_node(record[0], record[1], table)
			return True
	return False

def delete(data):
	record = input('Record to delete: ')
	if (Database.deleteCascade(data[1],record)):
		data[0].remove_node(record)
		return True
	return False

def show(data, nome = ''):
	data[0].printTable(nome)
	#TODO
	return False

if __name__ == "__main__":
	exit = False
	data = startUp()	

	while(not(exit)):
		print("""Select a number:
1. Add record
2. Delete record
3. Show records
0. Exit
			""")
		try:
			choice = int(input('Selection: '))
		except:
			print("That's not a valid option!")
		if choice == 1:
			if(add(data)):
				print("success")
		elif choice == 2:
			if(delete(data)):
				print("success")
		elif choice == 3:
			choice = input('Table to print (dont write to print all): ')
			show(data, choice)
		elif choice == 0:
			exit = True