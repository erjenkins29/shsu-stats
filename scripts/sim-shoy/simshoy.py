import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from scipy.stats import bernoulli, poisson, norm as normal_dist

ranks = [1,6,2,5,3,4,7,12,8,11,9,10,13,18,14,17,15,16]

teams = [(x,y%6+1,z/6+1) for x,y,z in zip(ranks,range(18),range(18))]

p_winning_in_rd1 = {(1,2): .8, (1,3): .9, (2,3): .7 }

p_winning_in_rd2 = .5


def sim_SHOY(simulations, 
             p_winning     = p_winning_in_rd1,
             p_winning_rd2 = p_winning_in_rd2
            ):

    results               = []
    corner_scenarios      = []
    count_of_dd_tiebreaks = 0

    for simulation in range(simulations):

        df_teams= pd.DataFrame(teams, columns=["team","pool","initial_subrank"])
 
        df_SHOY = df_teams.set_index(["pool","initial_subrank"])

        df_SHOY["game1"] = np.nan
        df_SHOY["game1pts"] = np.nan
        df_SHOY["game1diff"] = np.nan
        df_SHOY["game2"] = np.nan
        df_SHOY["game2pts"] = np.nan
        df_SHOY["game2diff"] = np.nan
        df_SHOY["game3"] = np.nan
        df_SHOY["game3pts"] = np.nan
        df_SHOY["game3diff"] = np.nan
        df_SHOY["game4"] = np.nan
        df_SHOY["game4pts"] = np.nan
        df_SHOY["game4diff"] = np.nan


        games = []
        for i in range(6):
            tmp = p_winning.keys()
            tmp.insert(0,i+1)
            games.append(tmp)


        ### Pool Play start

        for pool in games:
            j=0
            for game in pool[1:]:
                j+=1
                winner = bernoulli.rvs(p_winning[game])
                total  = int(normal_dist.rvs(loc=14,scale=1))
                diff   = 2*(poisson.rvs(.3)+1) - total%2
                winning_pts =  (total + diff) /2
                losing_pts  = total - winning_pts

                df_SHOY.loc[(pool[0],game[0]),"game%i"%j] = winner
                df_SHOY.loc[(pool[0],game[1-winner]),"game%ipts"%j] = winning_pts
                df_SHOY.loc[(pool[0],game[1-winner]),"game%idiff"%j] = diff
                df_SHOY.loc[(pool[0],game[1]),"game%i"%j] = 1 - winner
                df_SHOY.loc[(pool[0],game[winner]),"game%ipts"%j] = losing_pts
                df_SHOY.loc[(pool[0],game[winner]),"game%idiff"%j] = -1 * diff

        ### End of pool play, reseed

        df_SHOY["subrank_after_pool_play"] = 0
        for i in range(1,7):
            ranking_kpi     = df_SHOY.xs(i,level=0)[["game1","game2","game3"]].sum(axis=1)*1000000 + df_SHOY.xs(i,level=0)[["game1diff","game2diff","game3diff"]].sum(axis=1)*10000 + df_SHOY.xs(i,level=0)[["game1pts","game2pts","game3pts"]].sum(axis=1)*10
            
            ### Check that there's no disc-toss requirement for tiebreaking
            
            ###  Take the difference of the nth and n+1'th rank, see if they are the same.  If there is a 0, there
            ###   are two reasons why there could be... a 2-way tie or a 3-way tie.

            ranking_kpi_list = ranking_kpi.tolist()
            rank_differences = [ ranking_kpi_list[0]-ranking_kpi_list[1], 
                                 ranking_kpi_list[0]-ranking_kpi_list[2], 
                                 ranking_kpi_list[1]-ranking_kpi_list[2] ]
            if 0 in rank_differences:
                
                #### Case 1: there's a 3-way tie
                if rank_differences==[0,0,0]:
                    
                    ### Add enough to each score so that there is a double disc toss
                    ranking_kpi+=[1,2,3]
                    count_of_dd_tiebreaks += 3

                #### Case 2: there's a 2-way tie
                else:
                    #print ranking_kpi
                    ranking_kpi+=[1,2,3]
                    count_of_dd_tiebreaks += 2
            
            inner_pool_rank = ranking_kpi.rank(ascending=False)
            
            for j in range(1,4):
                df_SHOY.loc[(i,j),"subrank_after_pool_play"] = inner_pool_rank[j]

        df_SHOY = df_SHOY.reset_index().set_index(["pool","subrank_after_pool_play"]).sort_index()

        ### Crossover games start

        for poolset in [(1,2),(3,4),(5,6)]:
            for poolrank in range(1,4):
                winner = bernoulli.rvs(p_winning_rd2)
                try:
                    df_SHOY.loc[(poolset[0],poolrank),"game4"] = winner
                    df_SHOY.loc[(poolset[1],poolrank),"game4"] = 1-winner
                except:
                    print df_SHOY
                    
                total  = int(normal_dist.rvs(loc=14,scale=1))
                diff   = 2*(poisson.rvs(.3)+1) - total%2
                winning_pts =  (total + diff) /2
                losing_pts  = total - winning_pts

                df_SHOY.loc[(poolset[1-winner],poolrank),"game4pts"] = winning_pts
                df_SHOY.loc[(poolset[1-winner],poolrank),"game4diff"] = diff
                df_SHOY.loc[(poolset[winner],poolrank),"game4pts"] = losing_pts
                df_SHOY.loc[(poolset[winner],poolrank),"game4diff"] = -1 * diff


        df_SHOY["day1_record"] = ["%i - %i" %(x,y) for (x,y) in zip(df_SHOY[["game1","game2","game3","game4"]].sum(axis=1), 3- df_SHOY[["game1","game2","game3","game4"]].sum(axis=1))]

        results.append(np.cumsum(df_SHOY.day1_record.value_counts().sort_index(ascending=False)))
        
        if results[-1][1]!=9:
            corner_scenarios.append((results[-1],df_SHOY))
            
 
 
#    print "Program successfully completed...\n\n%i SHOY Day 1 simulations completed"%simulations
#    print "\nWin probabilities of each team in round 1:", p_winning
#    print "Win probabilities of each team in round 2:", p_winning_rd2
#    print "Number of teams affected by disc-flip tiebreaks:\t%i"%count_of_dd_tiebreaks
#    team_count_better_than_500 = sum([x[1]==9 for x in results])
#    print "Number of times 9 teams end up 2-1:\t%i"% team_count_better_than_500
    
    
    plt.style.use("fivethirtyeight")
    plt.figure(figsize=(6,8))
    plt.hist([x[1] for x in results],range=(6,14),bins=8, histtype="stepfilled")
    plt.yticks([ x*simulations/5. for x in range(6)] , [0, .2, .4, .6, .8, 1])
    plt.xticks([6.5 + x for x in range(7)],range(6,14))
    plt.title("SHOY -- %i simulations\n\nprobability distribution:\nNumber of teams finishing\n2-1 or better"%simulations)
    plt.xlabel("\nWin probabilities of each team in round 1:\n"   + str(p_winning) +
               "\n\nWin probabilities of each team in round 2:\n" + str(p_winning_rd2) +
               "\n\nNumber of teams involved in disc-flip tiebreaks:\n"+str(count_of_dd_tiebreaks))
    plt.tight_layout()
    plt.savefig("SHOY-sim.png")        
                
    return results, [x[1] for x in corner_scenarios]