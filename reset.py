#! /usr/bin/python3

import psycopg2

def main():
	conn = psycopg.connect("dbname='sparadis'")
	cursor = conn.cursor()
	cursor.execute("delete from fight")

if __name__ == "__main__":
	main()
