import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# use player stats to build lines for each point
# divide points into O points and D points
# O Efficiency is +1 for score on O, -1 for opponent score
# D Efficiency is +1 for score on D, -1 for opponent score

# Player Stats vs has points played for each player
# Points vs has O or D and scored or not
opponent = 'CI-Vapour 2017-03-29_16-30.csv'

player_stats_df = pd.read_csv('Player Stats vs. ' + opponent)
points_df = pd.read_csv('Points vs. ' + opponent)

o_points = points_df[points_df['Started on offense?'] == 1]
d_points = points_df[points_df['Started on offense?'] == 0]

players = player_stats_df.loc[:, ['Player', 'Points played']]

o_points_played = {}

points = o_points.loc[:,['Point']].values
if points.size > 0:
	for point in np.nditer(points):
		point = int(point)
		for row in players.iterrows():
			player_points = row[1][1].split(',')
			if str(point) in player_points:
				if row[1][0] in o_points_played.keys():
					o_points_played[row[1][0]] += 1
				else:
					o_points_played[row[1][0]] = 1



o_points_won = o_points[o_points['Scored?'] == 1]
points = o_points_won.loc[:,['Point']].values

o_lines_plus = {}

if points.size > 0:
	for point in np.nditer(points):
		point = int(point)
		for row in players.iterrows():
			player_points = row[1][1].split(',')
			if str(point) in player_points:
				if point in o_lines_plus.keys():
					o_lines_plus[point].append(row[1][0])
				else:
					o_lines_plus[point] = [row[1][0]]



o_points_lost = o_points[o_points['Scored?'] == 0]
points = o_points_lost.loc[:,['Point']].values

o_lines_minus = {}

if points.size > 0:
	for point in np.nditer(points):
		point = int(point)
		for row in players.iterrows():
			player_points = row[1][1].split(',')
			if str(point) in player_points:
				if point in o_lines_minus.keys():
					o_lines_minus[point].append(row[1][0])
				else:
					o_lines_minus[point] = [row[1][0]]


o_eff_data = {}

for point, line in o_lines_plus.items():
	for player in line:
		if player in o_eff_data.keys():
			o_eff_data[player] += 1
		else:
			o_eff_data[player] = 1

for point, line in o_lines_minus.items():
	for player in line:
		if player in o_eff_data.keys():
			o_eff_data[player] -= 1
		else:
			o_eff_data[player] = -1

for player, eff in o_eff_data.items():
	o_eff_data[player] = eff/o_points_played[player]

for player, eff in o_eff_data.items():
	print(player, ':\t', eff)