import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from getData import getD

def getImage(path): 
    return OffsetImage(plt.imread(path), zoom=.5)


def makegraphs(year_from, year_to,descr, cold,hot):

    data = pd.read_csv(descr + '/play_by_play_1999_to_2019.csv.gz', compression='gzip', low_memory=False)

    logos = os.listdir(os.getcwd() + '/logos')

    logo_paths = []

    for i in logos:
        logo_paths.append(os.getcwd() + '/logos/' + str(i))

    cold_limit = cold
    heat_limit = hot

    #Filter to pass plays,temp and season range and groupby offensive team
    team_epa = data.loc[(data['temp']  <= cold_limit) & (data['play_type']== 'pass') & (data['season'] >= year_from ) & (data['season'] <= year_to )].groupby(['posteam'])[['epa']].mean()

    #Do the same but for games in heat
    team_epa['hot'] = data.loc[(data['temp']  >= heat_limit) & (data['play_type'] == 'pass') & (data['season'] >= year_from ) & (data['season'] <= year_to )].groupby('posteam')[['epa']].mean()

    #Text files containing the data
    coldtx = data.loc[(data['temp']  <= cold_limit) & (data['play_type']== 'pass') & (data['season'] >= year_from ) & (data['season'] <= year_to )].groupby(['posteam','game_id']).agg({'epa':'mean','temp':'mean'})
    hottx = data.loc[(data['temp']  >= heat_limit) & (data['play_type'] == 'pass') & (data['season'] >= year_from ) & (data['season'] <= year_to )].groupby(['posteam','game_id']).agg({'epa':'mean','temp':'mean'})
    
    with open(descr + '/hot.txt', 'w') as file:
        file.write(hottx.to_string())

    with open(descr + '/cold.txt', 'w') as file:
        file.write(coldtx.to_string())

    #Define x and y
    x = team_epa['epa']
    y = team_epa.hot

    #Create a figure with size 12x12
    fig, ax = plt.subplots(figsize=(15,15))

    #Fixed size of graph, good for making animations
    #ax.set_xlim([-0.45,0.45])
    #ax.set_ylim([-0.45,0.47])

    #Make a scatter plot first to get the points to place logos
    ax.scatter(x, y, s=.001)

    #Adding logos to the chart
    for x0, y0, path in zip(x, y, logo_paths):
        ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False, fontsize=4)
        ax.add_artist(ab)


    #Adding labels and text
    ax.set_xlabel('Passing EPA in cold (<= ' + str(cold_limit) + '°F)', fontsize=16)
    ax.set_ylabel('Passing EPA in heat (>= ' + str(heat_limit) + '°F)', fontsize=16)

    #Add a grid
    ax.grid(zorder=0,alpha=.4)
    ax.set_axisbelow(True)
        
    
    year_from = str(year_from)
    year_to = str(year_to)

    ax.set_title('Mean Passing EPA by Team & Temperature - ' + year_from + '-' + year_to, fontsize=20)
    plt.figtext(.81, .07, 'Data: nflfastR', fontsize=12)
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 
            color='darkorange', linestyle='--')

    #Save the figure as a png
    plt.savefig(descr + '/passing_heat_epas_' + year_from + '_' + year_to + '.png', dpi=400)


#Set up the datafile if it does not exist
columns = ['game_id','posteam','play_type','epa','temp','season']
descr  = "temp"

#creates datafile
getD(1999, 2019, columns,descr)

year_from = 1999
year_to = 2019

years = range(1999,2020)
#for i in years:
#    print(i)
#    if(i <= (year_to -9)):
#        makegraphs(i,i+9,descr)
makegraphs(1999,2010,descr,35,80)