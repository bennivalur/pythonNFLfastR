import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from getData import getD

#Hot vs cold passing
def makegraph(year_from, year_to,_directory, temp):
    data = pd.read_csv(_directory + '/play_by_play_1999_to_2019.csv.gz', compression='gzip', low_memory=False)

    min_attempts = 30
    title = 'Mean QB EPA by QB When the temperature is exactly 66°F (minimum '+ str(min_attempts) +' passing attempts and over one(1) rushing attempt) - ' + str(year_from) + '-' + str(year_to)
    x_label = 'QB EPA on running plays'
    y_label = 'QB EPA on passing plays'
    file_name = 'trubisky_.png'
    plot_credits = 'Data: nflfastR | plot by: @bennivaluR_'

    run_epa = data.loc[(data['temp'] == temp) & (data['play_type'] == 'run') ].groupby(['name']).agg({'qb_epa':'mean','play_type':'count'})
    pass_epa = data.loc[(data['temp'] == temp) & (data['play_type'] == 'pass') ].groupby(['name']).agg({'qb_epa':'mean','play_type':'count'})

    team_epa = pd.merge(run_epa,pass_epa,on='name',how='inner')
    
    team_epa.rename(columns={'qb_epa_x': 'qb_epa_run','qb_epa_y': 'qb_epa_pass','play_type_x': 'run_count','play_type_y': 'pass_count'}, inplace=True)

    team_epa = team_epa.loc[(team_epa['pass_count'] > min_attempts)]
    team_epa = team_epa.loc[(team_epa['run_count'] > 1)]

    team_epa.reset_index(inplace=True) 


    with open(_directory + '/main_table.txt', 'w') as file:
        file.write(team_epa.to_string())

    
    #Define x and y
    x = team_epa.qb_epa_run
    y = team_epa.qb_epa_pass

    #Create a figure with size 15x15
    fig, ax = plt.subplots(figsize=(15,15))

    #Make a scatter plot first to get the points to place logos
    ax.scatter(x, y, s=25.000)

    #adding names to plot
    for i, txt in enumerate(team_epa.name):
        ax.annotate(txt, (team_epa['qb_epa_run'].iloc[i], team_epa['qb_epa_pass'].iloc[i]),(team_epa['qb_epa_run'].iloc[i]+0.005, team_epa['qb_epa_pass'].iloc[i]+0.005))


    #Adding labels and text
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_label, fontsize=16)


    #Add a grid
    ax.grid(zorder=0,alpha=.4)
    ax.set_axisbelow(True)

    ax.set_title(title, fontsize=15)
    plt.figtext(.81, .07, plot_credits, fontsize=10)

    #Plot trendline
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 
            color='darkorange', linestyle='--')

    #Save the figure as a png
    plt.savefig(_directory + '/' + file_name , dpi=400)


#Set up the datafile if it does not exist
_columns = ['game_id','play_type','epa','temp','rusher','receiver','passer','name','qb_epa']
_directory  = "trubisky"

year_from = 1999
year_to = 2019
temp = 66

#Create datafile if it does not exist
#Run getD intependently if you want a new datafile with other columns
if(not os.path.exists(_directory + '/play_by_play_'+ str(year_from) +'_to_'+ str(year_to) +'.csv.gz')):
    getD(year_from, year_to, _columns,_directory) 


makegraph(year_from,year_to,_directory,temp)