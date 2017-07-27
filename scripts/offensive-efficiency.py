import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
# Offensive/Deffensive Officiency

# single player single game

def get_game_data(game):
	# returns a dataframe for the points csv and the points played for each player
	def points_played_to_array(row):
		data = row['Points played'].split(',')
		return pd.Series({'Player': row['Player'], 'Points played': np.array([int(point) for point in data])})\

	player_stats_df = pd.read_csv(mypath + 'Player Stats vs. ' + game)
	points_played_df = player_stats_df.apply(points_played_to_array, axis=1)

	return pd.read_csv(mypath + 'Points vs. ' + game), points_played_df

def o_eff(player, game):
	# return raw player offensive score, total o points played
	points_df, points_played_df = get_game_data(game)
	
	plus = 0
	minus = 0

	if player in points_played_df['Player'].unique():
		plus = len(np.intersect1d(points_played_df[points_played_df['Player'] == player]['Points played'].values[0],
								  points_df[(points_df['Started on offense?'] == 1) & (points_df['Scored?'] == 1)]['Point']))

		minus = len(np.intersect1d(points_played_df[points_played_df['Player'] == player]['Points played'].values[0],
								   points_df[(points_df['Started on offense?'] == 1) & (points_df['Scored?'] == 0)]['Point']))
	return plus - minus, plus + minus

def total_o_eff(player, games):
	# return the total offensive efficiency for a player over a list of games
	ulti_df = pd.read_csv('../WY-Wolves/1617SUISWolves-stats.csv')
	o_scored = len(ulti_df[(ulti_df['Line'] == 'O') & (ulti_df['Action'] == 'Goal') & (ulti_df['Event Type'] == 'Offense') &
            ((ulti_df['Player 0'] == player) |
             (ulti_df['Player 1'] == player) |
             (ulti_df['Player 2'] == player) |
             (ulti_df['Player 3'] == player) |
             (ulti_df['Player 4'] == player) |
             (ulti_df['Player 5'] == player) |
             (ulti_df['Player 6'] == player))])
	o_lost = len(ulti_df[(ulti_df['Line'] == 'O') & (ulti_df['Action'] == 'Goal') & (ulti_df['Event Type'] == 'Defense') &
            ((ulti_df['Player 0'] == player) |
             (ulti_df['Player 1'] == player) |
             (ulti_df['Player 2'] == player) |
             (ulti_df['Player 3'] == player) |
             (ulti_df['Player 4'] == player) |
             (ulti_df['Player 5'] == player) |
             (ulti_df['Player 6'] == player))])
	o_plus_minus = o_scored - o_lost
	o_points_played = o_scored + o_lost
	for game in games:
		new_plus_minus, new_points_played = o_eff(player, game)
		o_plus_minus += new_plus_minus
		o_points_played += new_points_played

	if o_points_played == 0:
		return None
	else:
		return o_plus_minus/o_points_played

def d_eff(player, game):
	# return raw player defensive score, total d points played
	points_df, points_played_df = get_game_data(game)

	plus = 0
	minus = 0

	if player in points_played_df['Player'].unique():
		plus = len(np.intersect1d(points_played_df[points_played_df['Player'] == player]['Points played'].values[0],
								  points_df[(points_df['Started on offense?'] == 0) & (points_df['Scored?'] == 1)]['Point']))

		minus = len(np.intersect1d(points_played_df[points_played_df['Player'] == player]['Points played'].values[0],
								   points_df[(points_df['Started on offense?'] == 0) & (points_df['Scored?'] == 0)]['Point']))
	return plus - minus, plus + minus

def total_d_eff(player, games):
	# return the total offensive efficiency for a player over a list of games
	ulti_df = pd.read_csv('../WY-Wolves/1617SUISWolves-stats.csv')
	d_scored = len(ulti_df[(ulti_df['Line'] == 'D') & (ulti_df['Action'] == 'Goal') & (ulti_df['Event Type'] == 'Defense') &
            ((ulti_df['Player 0'] == player) |
             (ulti_df['Player 1'] == player) |
             (ulti_df['Player 2'] == player) |
             (ulti_df['Player 3'] == player) |
             (ulti_df['Player 4'] == player) |
             (ulti_df['Player 5'] == player) |
             (ulti_df['Player 6'] == player))])
	d_lost = len(ulti_df[(ulti_df['Line'] == 'D') & (ulti_df['Action'] == 'Goal') & (ulti_df['Event Type'] == 'Offense') &
            ((ulti_df['Player 0'] == player) |
             (ulti_df['Player 1'] == player) |
             (ulti_df['Player 2'] == player) |
             (ulti_df['Player 3'] == player) |
             (ulti_df['Player 4'] == player) |
             (ulti_df['Player 5'] == player) |
             (ulti_df['Player 6'] == player))])
	d_plus_minus = d_scored - d_lost
	d_points_played = d_scored + d_lost
	for game in games:
		new_plus_minus, new_points_played = d_eff(player, game)
		d_plus_minus += new_plus_minus
		d_points_played += new_points_played
	if d_points_played == 0:
		return None
	else:
		return d_plus_minus/d_points_played

mypath = '../WY-Wolves/'

players_df = pd.read_csv(mypath + '1617 SUIS Wolves Players.csv')
players = list(players_df['Player'])
# players = ['#27 Daniel Zhang',
# 		   '#69 Justin Chen',
# 		   '#66 Jerry Chen',
# 		   'Oscar Yao',
# 		   '#76 Jack Xia',
# 		   '#19 Ben Wang',
# 		   '#41 Billy Ni',
# 		   '#25 Alex Chen',
# 		   '#30 Jimmy Peng',
# 		   '#1 Joyce Wang',
# 		   '#14 Cecilia Wu',
# 		   '#28 Tina Zhu',
# 		   'Melody Zheng',
# 		   '#0 Julie Luo',
# 		   '#52 Emily Zhang',
# 		   'Theresa Zhang']

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
games = []
for f in onlyfiles:
	if('vs.' in f):
		idx = f.index('vs.')
		games.append(f[idx + 4:])

games = list(set(games))
rows = []

for player in players:
	row = {'Player': player, 'O eff': total_o_eff(player, games), 'D eff': total_d_eff(player, games)}
	rows.append(row)

eff = pd.DataFrame(rows)
eff = eff.set_index('Player')
print(eff.sort_values('O eff', ascending=False))
print()
print(eff.sort_values('D eff', ascending=False))

