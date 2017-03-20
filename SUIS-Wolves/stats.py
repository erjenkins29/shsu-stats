import csv
from os import listdir
from os.path import isfile, join
import time
import io


mypath = 'C:\\Users\\aligh_000\\shsu-stats\\SUIS-Wolves'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def single_game_scoring(passing_file):
	# assumes a forehad force
	scoring = {'upline': 0, 'crossfield': 0}
	with open(passing_file, newline='') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			assist = int(row[9])
			start_x = float(row[19])
			end_x = float(row[21])

			if assist:
				if end_x > start_x:
					scoring['upline'] += 1
				else:
					scoring['crossfield'] += 1
	return scoring

def multi_game_scoring(passing_files):
	# look through passing files to see if score is
	# upline or cross field
	scoring = {'upline': 0, 'crossfield': 0}
	for passing_file in passing_files:
		game_scoring = single_game_scoring(passing_file)
		for score_type in scoring.keys():
			scoring[score_type] += game_scoring[score_type]
	return scoring

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

def process_defensive_blocks(row):
	# Created
	# Point
	# Player
	# In own endzone? -- can't know
	# In opponent's endzone? -- can't know
	# Stall out? -- can't know
	# Callahan?
	# Location X (0 -> 1 = left sideline -> right sideline) -- can't know
	# Location Y (0 -> 1 = back of opponent endzone -> back of own endzone) -- can't know
	defensive_blocks_fieldnames = ['Created', 'Point', 'Player', 'In own endzone?', "In opponent's endzone?", 
								   'Stall out?', 'Callahan?', 'Location X (0 -> 1 = left sideline -> right sideline)',
								   'Location Y (0 -> 1 = back of opponent endzone -> back of own endzone)']

	if row[8] == 'D' or row[8] == 'Callahan':
		stats = []
		game_start = int(row[0][10:13]) * 3600 + int(row[0][14:16]) * 60
		elapsed_time = int(row[41])
		event_time = game_start + elapsed_time

		created = row[0][:10] + ' ' + str(event_time // 3600) + ':' + str(event_time % 3600 // 60)
		point = str(int(row[5]) + int(row[6]))
		player = row[11]
		callahan = 1 if row[8] == 'Callahan' else 0
		stats = [created, point, player, '', '', '', callahan, '', '']
		return {k: v for k, v in zip(defensive_blocks_fieldnames, stats)}
	else:
		return None

def ultianalytics_to_statto(ultianalytics_file):
	# statto file nameing convention
	# focus vs. opponent date_id.csv
	defensive_blocks_prefix = 'Defensive Blocks vs. '
	passes_prefix = 'Passes vs. '
	player_stats_prefix = 'Player Stats vs. '
	points_prefix = 'Points vs. '
	possessions_prefix = 'Possessions vs. '
	stall_outs_prefix = 'Stall Outs Against vs. '

	defensive_blocks_fieldnames = ['Created', 'Point', 'Player', 'In own endzone?', "In opponent's endzone?", 'Stall out?', 'Callahan?', 'Location X (0 -> 1 = left sideline -> right sideline)', 'Location Y (0 -> 1 = back of opponent endzone -> back of own endzone)']
	passes_fieldnames = ['Created', 'Point', 'Possession', 'Thrower', 'Receiver', 'Turnover?', 'Thrower error?', 'Receiver error?', 'Throw to endzone?', 'Assist?', 'Secondary assist?', 'Huck? (> 40m)', 'Swing?', 'Dump?', 'From sideline?', 'To sideline?', 'Distance (m)', 'Forward distance (m)', 'Left-to-right distance (m)', 'Start X (0 -> 1 = left sideline -> right sideline)', 'Start Y (0 -> 1 = back of opponent endzone -> back of own endzone)', 'End X (0 -> 1 = left sideline -> right sideline)', 'End Y (0 -> 1 = back of opponent endzone -> back of own endzone)']
	player_stats_fieldnames = ['Player', 'Points played total', 'Points played', 'Touches', 'Points played with touches', 'Throws', 'Catches', 'Possessions initiated', 'Assists', 'Secondary Assists', 'Goals', 'Turnovers', 'Thrower errors', 'Receiver errors', 'Defensive blocks', 'Stall outs for', 'Stall outs against', 'Average completed throw distance (m)', 'Average completed throw gain (m)', 'Average incomplete throw distance (m)', 'Average incomplete throw gain(m)', 'Average caught pass distance (m)', 'Average caught pass gain (m)']
	points_fieldnames = ['Created', 'Point', 'Our score at pull', "Opponent's score at pull", 'Started on offense?', 'Scored?', 'Possessions', 'Passes', 'Turnovers', 'Thrower errors', 'Receiver errors', 'Defensive blocks', 'Opposition errors', 'Secondary assist', 'Assist', 'Goal']
	possessions_fieldnames = ['Created', 'Point', 'Possession', 'Started point on offense?', 'Scored?', 'Start X (0 -> 1 = left sideline -> right sideline', 'Start Y (0 -> 1 = back of opponent endzone -> back of own endzone)', 'Initiator', 'Passes', 'Secondary assist', 'Assist', 'Goal', 'Thrower error', 'Receiver error', 'Stalled out']
	stall_outs_fieldnames = ['Created', 'Point', 'Possession', 'Player', 'Location X (0 -> 1 = left sideline -> right sideline)', 'Location Y (0 -> 1 = back of opponent endzone -> back of own endzone)']

	games = []
	with open(ultianalytics_file, newline='') as ultianalytics_file:
		ultianalytics_reader = csv.reader(ultianalytics_file)
		next(ultianalytics_reader, None)
		row = next(ultianalytics_reader)
		date = row[0][:10]
		time = row[0][11:13] + '-' + row[0][14:16]
		opponent = row[2]

		game_suffix = opponent + ' ' + date + '_' + time + '.csv'

		defensive_blocks = mypath + '\\' + defensive_blocks_prefix + game_suffix
		passes = mypath + '\\' + passes_prefix + game_suffix
		player_stats = mypath + '\\' + player_stats_prefix + game_suffix
		points = mypath + '\\' + points_prefix + game_suffix
		possessions = mypath + '\\' + possessions_prefix + game_suffix
		stall_outs = mypath + '\\' + stall_outs_prefix + game_suffix

		game_files = [defensive_blocks, passes, player_stats, points, possessions, stall_outs]

		for row in ultianalytics_reader:
			# get the game suffix information
			date = row[0][:10]
			time = row[0][11:13] + '-' + row[0][14:16]
			opponent = row[2]

			game_suffix = opponent + ' ' + date + '_' + time + '.csv'

			if (game_suffix) not in games:
				games.append(game_suffix)

			# read the row and determine which statto files need to be written to.
				# Date/Time
				# Tournament
				# Opponent
				# Point Elapsed Seconds
				# Line (O or D)
				# Our Score - End of Point
				# Their Score - End of Point
				# Event Type
				# Action
				# Passer
				# Receiver
				# Defender
				# Hang Time (secs)
				# Player 0
				# Player 1
				# Player 2
				# Player 3
				# Player 4
				# Player 5
				# Player 6
				# ...
				# Player 27
				# Elapsed Time (secs)
				# Begin Area
				# Begin X
				# Begin Y
				# End Area
				# End X
				# End Y
				# Distance Unit of Measure
				# Absolute Distance
				# Lateral Distance
				# Toward Our Goal Distance

			# when opening the statto files read the first row to see if the headers are there.
			# Defensive Blocks

			# correctly writes the header line

			with open(defensive_blocks, 'w+', newline='') as f:
				statto_reader = csv.reader(f)
				statto_writer = csv.DictWriter(f, fieldnames=defensive_blocks_fieldnames)
				try:
					new_row = next(statto_reader)
					break
				except StopIteration:
					statto_writer.writeheader()

			stats = process_defensive_blocks(row)			
			if stats:
				with open(defensive_blocks, 'a', newline='\n') as f:
					statto_writer = csv.DictWriter(f, fieldnames=defensive_blocks_fieldnames)
					statto_writer.writerow(stats)
					
	return games

#------------------------------------------------
# test scoring for crossfield vs upline scoring

passing_files = [f for f in onlyfiles if ('Passes' in f)]
scoring_summary = multi_game_scoring(passing_files)
for score_type, amount in scoring_summary.items():
	print(score_type, ': ', amount)

#------------------------------------------------
# test for passing data

# passing_files = [f for f in onlyfiles if ('Passes' in f)]
# #print(passing_files)

# passing = multi_game_passing(passing_files)
# # passing = single_game_passing(passing_files[0])

# for thrower, receivers in passing.items():
# 	print(thrower)
# 	for receiver, count in receivers.items():
# 		print('\n\t' + receiver + ': ' + str(count))
# 	print()


#------------------------------------------------
# test for conversion script

# games = ultianalytics_to_statto(mypath + '\\' + 'test.csv')

# for game in games:
# 	print(game)
