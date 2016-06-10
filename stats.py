#! /usr/bin/env python3

import random
import sys
import psycopg2

def print_menu():
	menu = [
		'1. Longest fight?',
		'2. Shortest fight?', '3. Won most fights?',
		'4. Lost most fights', '5. Most possible attacks',
		'6. Win/Loss/Draw table', '7. Exit'
		]

	for item in menu:
		print(item)	
		
		#clear results all need to do is delete from table_name

def shortest(cursor):
	cursor.execute("select name from fight order by finish - start desc")
	return(rows[0][0])

def longest(cursor):
	cursor.execute("select name from fight order by finish - start")
	return(rows[0][0])

#def most_fights():

#def least_fights():

#def possible_attacks():

"""
if len(fighter_attacks > current_highest):
	current_highest = fighters_attacks
"""

def main():
	fighter_list = []
	
	arg1 = sys.argv[1]

	conn = psycopg2.connect(database=arg1)
	
	cursor = conn.cursor()

	print_menu()

	while(1):
		user_input = input('Choice: ')

		if(user_input == '1'):
			print("here")
			longest_fight = longest(cursor)
			print(longest_fight)
		elif(user_input == '2'):
			shrotest_fight = shortest(cursor)
			print(shortest_fight)
		else:
			break

	conn.close()

if __name__ == "__main__":
	main()
