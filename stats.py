#! /usr/bin/env python3

import random
import sys
import psycopg2

def print_menu():
	menu = [
		'1. Longest fight?',
		'2. Shortest fight?', '3. Most possible attacks?',
		'4. Won most fights?','5. Lost most fights?',
		'6. Draws?', '7. Exit'
		]

	for item in menu:
		print(item)	

def main():
	fighter_list = []
	
	if(len(sys.argv) != 2):
		print("Invalid Syntax")
		print("Usage: ./stats.py <db-name>")
		sys.exit()
	
	arg1 = sys.argv[1]

	try:
		conn = psycopg2.connect(database=arg1)
	except Exception as e:
		print("Failure to connect to database")
		exit(1)
	
	cur = conn.cursor()

	while(1):

		print_menu()
		
		choice = input("Choice:")

		try:
			cur.execute("select * from fight")
		except Exception as e:
			print("Failed to access database, {0}".format(e))
			exit(1)
			
		fightfacts = cur.fetchall()

		try:
			cur.execute("select * from combatant")
		except Exception as e:
			print("Failed to access database, {0}".format(e))
			exit(1)	
					
		combatantinfo = cur.fetchall()


		num = 0
		for item in combatantinfo:
			if int(item[0]) > num:
				num = int(item[0])
		#style and logic found with help from piracane at
		#https://github.com/pauliracane/thunderdome/blob/master/stats
		listTimeIn = [5]
		if ( choice < '3' ):
			#this query and setup style was found through the help of
			#https://github.com/JMcLaurin/thunderdome/blob/master/stats.py
			sql_query = "SELECT id, name, SUM(finish-start)"
			sql_query += "FROM combatant JOIN fight ON id=combatant_one OR"
			sql_query += " id=combatant_two GROUP BY id ORDER BY sum DESC;"

			cur.execute(sql_query) 
			time = cur.fetchall()			

			if choice == '1':
				print(time[0][1], "fought for", time[0][2])
			elif choice == '2':
				print(time[-1][1], "fought for", time[-1][2])
		elif ( choice == '3' ):
			highestnumskills = [0, 0]
			for each in combatantinfo:
				cur.execute("select * from species_attack where species_id = " + str(each[0]))
				skilllist = cur.fetchall()
				if (len(skilllist) > highestnumskills[0]):
					highestnumskills[0] = each[0]
					highestnumskills[1] = len(skilllist)

			for each in combatantinfo:
				if each[0] == highestnumskills[0]:
					print(each[1], "has the most skills available at",
					highestnumskills[1])

		if(choice >= '4') and (choice <= '6'):
			ListOfThings = [2]
			for each in combatantinfo:
				ListOfThings.append(0)

			if (choice == '4'):
				for x in range(1, len(combatantinfo)):
					for thing in fightfacts:
						if ((int(thing[0]) == x) and (thing[2] == "One") or
						(int(thing[1]) == x) and (thing[2] == "Two")):
							ListOfThings[x]+=1
				print("The most wins was: ",max(ListOfThings))
			elif (choice == '5'):
				for x in range(1, len(combatantinfo)):
					for thing in fightfacts:
						if ((int(thing[1]) == x) and (thing[2] == "One")
						or (int(thing[0]) == x) and (thing[2] == "Two")):
							ListOfThings[x]+=1
				print("The most Losses was: ",max(ListOfThings))
			elif (choice == '6'):
				for x in range(1, len(combatantinfo)):
					for thing in fightfacts:
						if ((int(thing[0]) == x) and (thing[2] == "Tie")
						or (int(thing[1]) == x) and (thing[2] == "Tie")):
							ListOfThings[x]+=1
				print("The most ties was: ",max(ListOfThings))
		if(choice == '7'):
			print('quitting..')
			sys.exit()

	"""
	while(1):
		user_input = input('Choice: ')

		if(user_input == '1'):
			print("here")
			longest_fight = longest(cursor)
			print(longest_fight)
		elif(user_input == '2'):
			print('here 2')
			shortest_fight = shortest(cursor)
			print(shortest_fight)
		else:
			break
	"""
	conn.close()

if __name__ == "__main__":
	main()
