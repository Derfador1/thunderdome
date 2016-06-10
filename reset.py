#! /usr/bin/python3

import psycopg2
import sys

def main():
	arg1 = sys.argv[1]
		
	conn = psycopg2.connect(database=arg1)
	cursor = conn.cursor()
	cursor.execute('delete from fight *')
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
