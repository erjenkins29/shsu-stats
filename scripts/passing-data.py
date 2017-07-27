import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

def single_game_single_reciever(player, receiver, df):
    #df should be passed in
    data = {'Drops': len(df[df['Receiver error?'] == 1]),
            'Catches': len(df[df['Turnover?'] == 0]),
            'Throwaways': len(df[df['Thrower error?'] == 1]),
            'Goals': len(df[df['Assist?'] == 1])}
    return pd.Series(data)

def single_game_passing_data(thrower, game):
    df = pd.read_csv('WY-Wolves/Passes vs. ' + game)
    df = df[df['Thrower'] == thrower]
    data = pd.DataFrame(columns=['Drops', 'Catches', 'Throwaways', 'Goals'], index=['Player'])
    for receiver, frame in df.groupby('Receiver'):
        data.loc[receiver] = single_game_single_reciever(thrower, receiver, frame)

    return data

def ulti_passing_data(thrower):
    ulti_df = pd.read_csv('WY-Wolves/1617SUISWolves-stats.csv')
    ulti_df = ulti_df[ulti_df['Passer'] == thrower]
    data = pd.DataFrame(columns=['Drops', 'Catches', 'Throwaways', 'Goals'], index=['Player'])
    for reciever, frame in ulti_df.groupby('Receiver'):
        data.loc[reciever] = pd.Series({'Drops': len(frame[frame['Action'] == 'Drop']),
                                    'Catches': len(frame[frame['Action'] == 'Catch']),
                                    'Throwaways': len(frame[frame['Action'] == 'Throwaway']),
                                    'Goals': len(frame[frame['Action'] == 'Goal'])})
    return data

mypath = '../WY-Wolves/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
games = []
for f in onlyfiles:
	if('vs.' in f):
		idx = f.index('vs.')
		games.append(f[idx + 4:])

games = list(set(games))

thrower = '#22 Paul Simpson'

data = single_game_passing_data(thrower, games[0])
for game in games[1:]:
	print(game)
	data = data.add(single_game_passing_data(thrower, game), fill_value=0)
print(data.sort_values('Catches',ascending=False))
