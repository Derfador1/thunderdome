#! /usr/bin/env python3

import random
import sys
import psycopg2
import time
import itertools

type_chart = {
	"Physical":{"Radioactive":2, "Mystical":.5},
	"Biological":{"Physical":2, "Chemical":2, "Mystical":2},
	"Radioactive":{"Biological":2, "Chemical":.5, "Technological":.5, "Mystical":2},
	"Chemical":{"Physical":.5, "Radioactive":.5, "Chemical":.5, "Technological":2, "Mystical":.5},
	"Technological":{"Biological":2, "Radioactive":.5, "Chemical":.5, "Mystical":.5},
	"Mystical":{"Radioactive":2, "Mystical":.5},
	"Mineral":{"Mineral":0}
	}

#used to store all pertanent information pertaining to fighter
class Combatant:
	def __init__(self, c_id, char_name, species_name, creature_type, base_atk, base_def, base_hp):
		self.c_id = c_id
		self.char_name = char_name
		self.species_name = species_name
		self.creature_type = creature_type
		self.base_atk = base_atk
		self.base_def = base_def
		self.base_hp = base_hp
		self.atk = []	

#used to store all pertanent information pertaining to the attack
class Attack:
	def __init__(self, attack_id, name, attack_type, min_dmg, max_dmg, attack_speed):
		self.atk_id = attack_id
		self.name = name
		self.attack_type = attack_type
		self.min_dmg = min_dmg
		self.max_dmg = max_dmg
		self.attack_speed = attack_speed

#this code was acquired from
#stackoverflow.com/question/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
#it is used to give back a time grouping based on given seconds
def ddhhmmss(seconds):
	dhms = ''
	for scale in 86400, 3600, 60:
		result, seconds = divmod(seconds, scale)
		if dhms != '' or result > 0:
			dhms += '{0:02d}:'.format(result)
	dhms += '{0:02d}'.format(seconds)
	if len(dhms) < 3:
		dhms = "00:00:" + dhms
	elif len(dhms) <= 5:
		dhms = "00:" + dhms
	return dhms

def create_combatants(cursor, fighter_list):
	num_of_combatant = 0

	try:
		cursor.execute('select * from combatant')
	except Exception as e:
		print("Failed to access database, {0}".format(e))
		exit(1)

	rows = cursor.fetchall()

	for num in rows:
		num_of_combatant += 1

	if num_of_combatant == 0:
		for char in fighter_list:
			try:
				#insert the information into the combatant table
				cursor.execute("insert into combatant (name, species_id, plus_atk, plus_dfn, plus_hp) values (%s, %s, %s, %s, %s);",\
				(char.char_name, char.c_id, 0, 0, 0))
			except Exception as e:
				print("Failed to access database, {0}".format(e))
				exit(1)

#logic and these 2 functions set up acquired with help/use of
#github user dsprimm and at
#https://github.com/dsprimm/thunderdome/blob/master/thunderdome.py

#damage calculations based on information given by Liam
def dmg(fighter, defender, attack):
	try:
		dmg = type_chart[fighter.creature_type][defender.creature_type]
	except:
		dmg = 1
	try:
		atk = type_chart[attack.attack_type][defender.creature_type]
	except:
		atk = 1
	
	if defender.base_def - fighter.base_atk < 1:
		#if this subtraction gives a 0 or negative just assume 0 because we cant do negative damage
		dmg = 0 + (atk * random.randint(attack.min_dmg, attack.max_dmg))
	else:
		dmg = (dmg * random.randint(0, defender.base_def - fighter.base_atk)) + (atk * random.randint(attack.min_dmg, attack.max_dmg))
	return dmg


def battle(fighter, defender):
	atk_hp = fighter.base_hp
	def_hp = defender.base_hp
	fighter_time = 0
	defender_time = 0
	total_time = 0

	while(atk_hp >= 0 and def_hp >= 0):
		if fighter_time == 0:
			#randomly chooses attack from list of possible attacks
			fighter_attack = random.choice(fighter.atk)
			#getting time between attacks
			fighter_time = fighter_attack.attack_speed.total_seconds()
		else:
			fighter_time -= 1
			#deal damage to defender if the attacker time is 0
			if fighter_time == 0:
				damage = dmg(fighter, defender, fighter_attack)
				def_hp -= damage

		if defender_time == 0:
			#randomly chooses attack for defender from list of possible attacks
			defender_attack = random.choice(defender.atk)
			#getting time between attacks
			defender_time = defender_attack.attack_speed.total_seconds()
		else:
			defender_time -= 1
			#deal damage to defender if the attacker time is 0
			if defender_time == 0:
				damage = dmg(defender, fighter, defender_attack)
				atk_hp -= damage
			
		total_time+= 1

	if atk_hp >= 0 and def_hp < 0:
		#victory
		return 2, total_time
	elif atk_hp < 0 and def_hp >= 0:
		#defeat
		return 1, total_time
	else:
		#draw
		return 0, total_time

			
	
def main():
	random.seed(time)

	count = 0
	
	rand_numb = 0

	name = [
		'Happy', 'Sleepy', 'Grumpy',
		'Sneezy', 'Doc', 'Bashful',
		'Dopey', 'Death Incarnate', 'Toilet',
		'Your Mailman', 'The Almighty Paradis', 'No one',
		'Person', 'Winner'
	]

	fighter_list = []
	attacks = []
	
	if(len(sys.argv) != 2):
		print("Invalid Syntax")
		print("Usage: .thunderdome.py <db-name>")
		sys.exit()	

	arg1 = sys.argv[1]

	try:
		conn = psycopg2.connect(database=arg1)
	except Exception as e:
		print("Failure to connect to database")
		exit(1)
	
	cursor = conn.cursor()

	try:
		cursor.execute('select * from fight')
	except Exception as e:
		print("Failed to access database, {0}".format(e))
		exit(1)

	rows = cursor.fetchall()

	#checking to see if there is already information in fight table
	for row in rows:
		count += 1

	if count > 0:
		print('Tournament has already taken place, please reset')
		exit(1)

	try:
		cursor.execute('select * from species')
	except Exception as e:
		print("Failed to access database, {0}".format(e))
		exit(1)

	rows = cursor.fetchall()

	#creates a list of fighters with randomly chosen names
	for row in rows:
		name_choice = random.choice(name)
		fighter_list.append(Combatant(row[0], name_choice, row[1], row[2], row[3], row[4], row[5]))
		name.remove(name_choice)

	try:
		cursor.execute('select * from attack')
	except Exception as e:
		print("Failed to access database, {0}".format(e))
		exit(1)

	rows = cursor.fetchall()

	#create attacks object with set fields based on every attack
	for atk in rows:
		attacks.append(Attack(atk[0], atk[1], atk[2], atk[3], atk[4], atk[5]))

	try:
		cursor.execute('select * from species_attack')
	except Exception as e:
		print("Failed to access database, {0}".format(e))
		exit(1)

	rows = cursor.fetchall()

	#attachs attacks to each fighter based on species
	for i in rows:
		fighter_list[i[0]-1].atk.append(attacks[i[1]-1])

	create_combatants(cursor, fighter_list)

	conn.commit()

	#use of itertools with help from dprimm to create a list of pairs to fight each other
	pairs = itertools.combinations(fighter_list, 2)
	for sset in pairs:
		final = battle(sset[0], sset[1])
	
		#create the date time group
		final_time = 0

		start_str = '2016-06-10 ' + ddhhmmss(final_time) #always starts from 00:00:00

		final_time += final[1]

		fin_str = '2016-06-10 ' + ddhhmmss(final_time)

		#based on return value we insert who won witht time stamp info
		if final[0] == 0:
			cursor.execute("insert into fight (combatant_one, combatant_two, winner, start, finish) values (%s, %s, 'Tie', TIMESTAMP \
			%s, TIMESTAMP %s)", (sset[0].c_id, sset[1].c_id, start_str, fin_str))
		elif final[0] == 1:
			cursor.execute("insert into fight (combatant_one, combatant_two, winner, start, finish) values (%s, %s, 'Two', TIMESTAMP \
			%s, TIMESTAMP %s)", (sset[0].c_id, sset[1].c_id, start_str, fin_str))
		else:
			cursor.execute("insert into fight (combatant_one, combatant_two, winner, start, finish) values (%s, %s, 'One', TIMESTAMP \
			%s, TIMESTAMP %s)", (sset[0].c_id, sset[1].c_id, start_str, fin_str))

	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
