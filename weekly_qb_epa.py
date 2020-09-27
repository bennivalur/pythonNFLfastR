import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from getData import getD

def makegraph(_directory,team,week):
    data = pd.read_csv(_directory + '/play_by_play_2020_to_2020.csv.gz', compression='gzip', low_memory=False)
    



    data = data.loc[(data['posteam'] == team) & (data['week'] == week)& (data['qb_dropback'] == 1) ]

    last_row = data.iloc[-1]
    
    if(last_row['home_team'] == team):
        _at = ' vs '
        opponent = last_row['away_team']
        t_score = last_row['total_home_score']
        o_score = last_row['total_away_score']
    else:
        _at = ' @ '
        opponent = last_row['home_team']
        o_score = last_row['total_home_score']
        t_score = last_row['total_away_score']





    ##game_data = data.iloc[0]
    ##print(game_data['away_team'])

    #_title = 'Week 1 - Chicago @ Detroit: 27 - 23'
    _title = 'Week '+ str(week) +' - ' + team + _at + opponent + ': ' + str(t_score) + ' - ' + str(o_score) 
    plot_credits = 'Data: nflfastR | plot by: @bennivaluR_'
    _file_name = _directory + '/' + team + '/' + team +'_week' + str(week)


    data['sumQBEPA'] = data['qb_epa'].cumsum()
    data['sumEPA'] = data['epa'].cumsum()
    


    x = data.game_seconds_remaining
    y = data.sumQBEPA
    y2 = data['posteam_score']

    fig, ax = plt.subplots(figsize=(10,10))
    
    plt.plot(x,y2,label = 'Points')
    plt.plot(x,y,label='QB EPA')
    
    plt.legend(loc="upper left")

    ax = plt.gca()
    ax.invert_xaxis()

    plt.figtext(.5,.92,_title,fontsize=15,ha='center')
    plt.figtext(.5,.90,team+' Actual Points vs Accumulated QB EPA on QB dropbacks',fontsize=10,ha='center')
    
    plt.figtext(.71, .05, plot_credits, fontsize=10)
    plt.ylabel('Points')
    plt.xlabel('Time Remaining')
    

    

    #Save the figure as a png
    plt.savefig( _file_name, dpi=400)

def makeScatter(_directory):
    print("ahh")

def setup(_directory,teams):
    for i in teams:
        try: 
            os.makedirs(_directory + '/' + i)
        except OSError:
            if not os.path.isdir(_directory):
                raise

def doAllTeams(_directory,week,teams):
    for t in teams:
        print("Making " + t)
        makegraph(_directory,t,week)

#Set up the datafile if it does not exist
_columns = ['game_id','home_team','away_team','total_home_score','total_away_score','posteam','week','game_seconds_remaining','posteam_score','play_type','epa','temp','receiver','passer','name','qb_epa','qb_scramble','qb_dropback']
_directory  = "qb_epa_weekly"

year_from = 2020
year_to = 2020

teams = ['ARI','ATL','BAL','BUF','CAR','CHI','CIN','CLE','DAL','DEN','DET','GB','HOU','IND','JAX','KC','LA','LAC','LV','MIA','NE','NO','NYG','NYJ','PHI','PIT','SEA','SF','TB','TEN','WAS']

#Uncomment to get data
getD(year_from, year_to, _columns,_directory) 

#setup(_directory,teams)

week = 2
team = 'CHI'

#Make one graph for one team
makegraph(_directory,team,week)

#Uncomment to do for all teams
#doAllTeams(_directory,week,teams)

