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

def main():
	list1 = []
	
	conn = psycopg2.connect("dbname='sparadis'")
	
	cursor = conn.cursor()
	
	cursor.execute('select * from combatant')
	
	rows = cursor.fetchall()

	for row in rows:
		print(row)
	
	#print_menu()
	#trying to do stuff!!!!!
	
	conn.close()

if __name__ == "__main__":
	main()
