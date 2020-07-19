import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from getData import getD

def getImage(path): 
    return OffsetImage(plt.imread(path), zoom=.5)

#Hot vs cold passing
def makegraphs(year_from, year_to,descr, cold,hot):

    data = pd.read_csv(descr + '/play_by_play_1999_to_2019.csv.gz', compression='gzip', low_memory=False)

    logos = os.listdir(os.getcwd() + '/logos')

    logo_paths = []

    for i in logos:
        logo_paths.append(os.getcwd() + '/logos/' + str(i))

    cold_limit = cold
    heat_limit = hot
    min_attempts = 150

    #Filter to pass plays,temp and season range and groupby offensive team
    team_epa = data.loc[(data['temp']  <= cold_limit) & (data['play_type']== 'pass') ].groupby(['passer']).agg({'qb_epa':'mean','game_id':'count'})

    #Do the same but for games in heat
    team_epa['not_cold'] = data.loc[(data['play_type'] == 'pass') & ((data['roof'] == 'dome')  | (data['roof'] == 'open') | (data['roof'] == 'closed') | (data['temp']  > cold_limit))].groupby('passer')[['qb_epa']].mean()
    team_epa = team_epa.loc[(team_epa['game_id']) > min_attempts]
    
    #Text files containing the data
    coldtx = data.loc[(data['temp']  <= cold_limit) & (data['play_type']== 'pass') ].groupby(['passer']).agg({'qb_epa':'mean','temp':'mean','game_id':'count'})
    hottx = data.loc[(data['play_type'] == 'pass') & ((data['roof'] == 'dome')  | (data['roof'] == 'open') | (data['roof'] == 'closed') | (data['temp']  > cold_limit))].groupby(['passer'])[['qb_epa']].mean()
    #hottx = data.loc[(data['play_type'] == 'pass')].groupby(['roof'])[['qb_epa']].mean()
    coldtx = coldtx.loc[(coldtx['game_id'] > min_attempts)]
    
    with open(descr + '/hot.txt', 'w') as file:
        file.write(hottx.to_string())

    with open(descr + '/cold.txt', 'w') as file:
        file.write(coldtx.to_string())

    with open(descr + '/main_table.txt', 'w') as file:
        file.write(team_epa.to_string())

    #Define x and y
    x = team_epa.not_cold
    y = team_epa['qb_epa']

    #Create a figure with size 12x12
    fig, ax = plt.subplots(figsize=(18,18))

    #Fixed size of graph, good for making animations
    ax.set_xlim([-0.1,0.4])
    #ax.set_ylim([-0.37,0.47])

    #Make a scatter plot first to get the points to place logos
    ax.scatter(x, y, s=25.000)

    #Adds a line
    #Above line = better in cold
    #Bellow line = worse in cold
    plt.plot([-0.1, 0.3], [-0.1, 0.3], color='black', linestyle='-', linewidth=1)

    #adding names to plot
    for i, txt in enumerate(team_epa.index):
        ax.annotate(txt, (team_epa['not_cold'].iloc[i], team_epa['qb_epa'].iloc[i]),(team_epa['not_cold'].iloc[i]+0.001, team_epa['qb_epa'].iloc[i]+0.001))


    #Adding labels and text
    ax.set_xlabel('QB EPA on passing plays in normal conditions (Indoor or temp > ' + str(cold_limit) + '°F)', fontsize=16)
    ax.set_ylabel('QB EPA on passing plays in cold conditions (<= ' + str(cold_limit) + '°F)', fontsize=16)


    #Add a grid
    ax.grid(zorder=0,alpha=.4)
    ax.set_axisbelow(True)
        
    
    year_from = str(year_from)
    year_to = str(year_to)

    ax.set_title('Mean QB EPA by QB & Conditions (minimum '+ str(min_attempts) +' attempts) - ' + year_from + '-' + year_to, fontsize=20)
    plt.figtext(.81, .07, 'Data: nflfastR', fontsize=12)
    #plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 
    #        color='darkorange', linestyle='--')



    #Save the figure as a png
    plt.savefig(descr + '/sub30_passing_cold_epas_' + year_from + '_' + year_to + '.png', dpi=400)


#Set up the datafile if it does not exist
columns = ['game_id','posteam','play_type','epa','roof','temp','season','passer','qb_epa']
descr  = "passing_cold_v2"

#creates datafile
#getD(1999, 2019, columns,descr)

year_from = 1999
year_to = 2019

#years = range(1999,2020)
#for i in years:
#    print(i)
#    if(i <= (year_to -9)):
#        makegraphs(i,i+9,descr,40,80)
makegraphs(1999,2019,descr,32,80)