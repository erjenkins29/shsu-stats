import csv
from os import listdir
from os.path import isfile, join
import time


mypath = 'C:\\Users\\aligh_000\\shsu-stats\\SUIS Wolves'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def single_game_passing(passing_file):
	# search all rows of a single game passing file
	# create a dictionary with keys = thrower name, values = dictionary of receivers
	# the dictionary of receivers has keys = receiver name, values = dictionary of reception types
	# the dictionary of reception types has keys = type name, value = number of times occurred

	passing = {}
	with open(passing_file, newline = '') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader, None)
		for row in csvreader:
			# loop through each row in the record
			# look for the thrower, reciever and the result of the throw

			# thrower and receiver are names
			# throw_error, rec_error, assist are 0, 1 values
			# throw_error, rec_error are not mutually exclusive
			thrower = row[3]
			receiver = row[4]
			throw_error = int(row[6])
			rec_error = int(row[7])
			assist = int(row[9])

			if thrower in passing.keys():
				if receiver in passing[thrower].keys():
					if throw_error:
						if 'throwaways' in passing[thrower][receiver].keys():
							passing[thrower][receiver]['throwaways'] += 1
						else:
							passing[thrower][receiver]['throwaways'] = 1
					if rec_error:
						if 'drops' in passing[thrower][receiver].keys():
							passing[thrower][receiver]['drops'] += 1
						else:
							passing[thrower][receiver]['drops'] = 1
					if assist:
						if 'goals' in passing[thrower][receiver].keys():
							passing[thrower][receiver]['goals'] += 1
						else:
							passing[thrower][receiver]['goals'] = 1
					if not throw_error and not rec_error:
						if 'catches' in passing[thrower][receiver].keys():
							passing[thrower][receiver]['catches'] += 1
						else:
							passing[thrower][receiver]['catches'] = 1
				else:
					passing[thrower][receiver] = {}
					if throw_error:
						passing[thrower][receiver]['throwaways'] = 1
					if rec_error:
						passing[thrower][receiver]['drops'] = 1
					if assist:
						passing[thrower][receiver]['goals'] = 1
					if not throw_error and not rec_error:
						passing[thrower][receiver]['catches'] = 1
			else:
				passing[thrower] = {receiver: {}}
				if throw_error:
					passing[thrower][receiver]['throwaways'] = 1
				if rec_error:
					passing[thrower][receiver]['drops'] = 1
				if assist:
					passing[thrower][receiver]['goals'] = 1
				if not throw_error and not rec_error:
					passing[thrower][receiver]['catches'] = 1

	# for thrower, receivers in passing.items():
	# 	total = 0
	# 	for rec_counts in receivers.values():
	# 		for att_count in rec_counts.values():
	# 			total += att_count
	# 	passing[thrower]['total'] = total
	return passing

def multi_game_passing(passing_files):
	passing = {}
	for passing_file in passing_files:
		game_passing = single_game_passing(passing_file)
		for thrower, receivers in game_passing.items():
			# receivers is a dictionary key = receiver, value = dicitionary
			if thrower in passing.keys():
				for receiver, attempts in receivers.items():
					# attempts is a dictionary with key = att_type, value = frequency
					if receiver in passing[thrower].keys():
						for attempt in attempts.keys():
							if attempt in passing[thrower][receiver].keys():
								passing[thrower][receiver][attempt] += game_passing[thrower][receiver][attempt]
							else:
								passing[thrower][receiver][attempt] = game_passing[thrower][receiver][attempt]
					else:
						passing[thrower][receiver] = game_passing[thrower][receiver]
			else:
				passing[thrower] = game_passing[thrower]
	return passing

passing_files = [f for f in onlyfiles if ('Passes' in f)]
#print(passing_files)

passing = multi_game_passing(passing_files)
# passing = single_game_passing(passing_files[0])

for thrower, receivers in passing.items():
	print(thrower)
	for receiver, count in receivers.items():
		print('\n\t' + receiver + ': ' + str(count))
	print()


# import matplotlib.pyplot as plt
# from numpy.random import rand
 
# fig, ax = plt.subplots()
# scale = 1000
# ax.scatter(0, 0, c='red', s=scale)
# ax.scatter(1, 0, c='red', s=scale)

# plt.show()