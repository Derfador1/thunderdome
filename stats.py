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
		
		#clear results all need to do is delete from table_name
"""
def shortest(cursor):
	cursor.execute("select * from fight order by finish - start desc")
	things = cursor.fetchall()
	return(things[0][0])

def longest(cursor):
	cursor.execute("select * from fight order by finish - start")
	things = cursor.fetchall()
	return(things[0][0])
	
if len(fighter_attacks > current_highest):
	current_highest = fighters_attacks
"""

def main():
	fighter_list = []
	
	if(len(sys.argv) != 2):
		print("Invalid Syntax")
		print("Usage: ./stats.py <db-name>")
		sys.exit()
	
	arg1 = sys.argv[1]

	conn = psycopg2.connect(database=arg1)
	
	cur = conn.cursor()

	while(1):

		print_menu()
		
		choice = input("Choice:")

		cur.execute("select * from fight")
		fightfacts = cur.fetchall()

		cur.execute("select * from combatant")
		combatantinfo = cur.fetchall()


		num = 0
		for item in combatantinfo:
			if int(item[0]) > num:
				num = int(item[0])
		#style and logic found with help from piracane at
		#https://github.com/pauliracane/thunderdome/blob/master/stats
		listTimeIn = [5]
		if ( choice < '3' ):
			for x in range(0, num):
				timeIn = 0
				for each in fightfacts:
					if (each[0] == x + 1) or (each[1] == x + 1):
						timeIn += (int(each[4].minute)*60+int(each[4].second)
						- int(each[3].minute)*60+int(each[3].second))
				listTimeIn.append(timeIn)

			if choice == '1':
				LongestFighter = max(listTimeIn)
				x = [i for i, j in enumerate(listTimeIn) if j == LongestFighter]

				for each in combatantinfo:
					if (each[0] == x[0]):
						print(each[1], "fought for",LongestFighter,"seconds!")

			elif choice == '2':
				print('not working')
				#need to fix this one
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
				print("The Most wins was: ",max(ListOfThings))
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
