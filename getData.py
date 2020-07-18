import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def getImage(path): 
    return OffsetImage(plt.imread(path), zoom=.5)


#Creates the datacollection needed while removing unneeded columns
#year_from: number (1999-2019)
#year_to: number (1999-2019)
#columns: array -> what columns to keep example = ['game_id','posteam','play_type','epa','temp','season']
#file_descr: string -> will create a folder with that name and save the datafile there
def getD(year_from, year_to, columns, file_descr):

    print("Getting data and fields needed")

    YEARS = range(year_from, year_to+1)
    year_to = str(year_to)
    year_from = str(year_from)
    data = pd.DataFrame()

    for i in YEARS:  
        print(i)
        i_data = pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/master/data/' \
                            'play_by_play_' + str(i) + '.csv.gz?raw=True',
                            compression='gzip', low_memory=False)
        print("Drop unneeded columns", i)
        i_data.drop(['passer_player_name', 'passer_player_id',
            'rusher_player_name', 'rusher_player_id',
            'receiver_player_name', 'receiver_player_id'],
            axis=1, inplace=True)

        print("Select only regular season", i)
        i_data = i_data.loc[i_data.season_type=='REG']

        print("Select only run, pass and no plays",i)
        i_data = i_data.loc[(i_data.play_type.isin(['no_play','pass','run'])) & (i_data.epa.isna()==False)]
        i_data.play_type.loc[i_data['pass']==1] = 'pass'
        i_data.play_type.loc[i_data.rush==1] = 'run'

        print('Remove columns we don\'t need')
        i_data = i_data[columns]

        data = data.append(i_data, sort=True)

    print("Reset Index")
    data.reset_index(drop=True, inplace=True)

    print("Save to csv")
    data.to_csv(file_descr + '/play_by_play_'+ year_from +'_to_'+ year_to +'.csv.gz', compression='gzip')



year_low = 1998
year_high = 2010

columns = ['game_id','posteam','play_type','epa','temp','season']
file_descr  = "temp"

#creates datafile
#getD(1999, 2019, columns,file_descr)


