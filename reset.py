#! /usr/bin/python3

import psycopg2
import sys

def main():
	if(len(sys.argv) != 2):
		print("Invalid Syntax")
		print("Usage: ./reset.py <db-name>")
		sys.exit()
	
	arg1 = sys.argv[1]
		
	try:
		conn = psycopg2.connect(database=arg1)
	except Exception as e:
		print("Failure to connect to database")
		exit(1)
		
	cursor = conn.cursor()
	try:
		cursor.execute('delete from fight *')
	except Exception as e:
		print("Failed to access database, {0}".format(e))
		exit(1)
	
	"""
	cursor.execute("drop table attack cascade;")
	cursor.execute("drop table combatant cascade;")
	cursor.execute("drop table fight cascade;")
	cursor.execute("drop table species cascade;")
	cursor.execute("drop table species_attack cascade;")
	cursor.execute("drop table type cascade;")
	"""
	
	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
