import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def getImage(path): 
    return OffsetImage(plt.imread(path), zoom=.5)

def getD(year_from, year_to, columns, file_descr):

    YEARS = range(year_from, year_to+1)
    year_to = str(year_to)
    year_from = str(year_from)
    data = pd.DataFrame()

    for i in YEARS:  
        print(i)
        i_data = pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/master/data/' \
                            'play_by_play_' + str(i) + '.csv.gz?raw=True',
                            compression='gzip', low_memory=False)
        print("drop", i)
        i_data.drop(['passer_player_name', 'passer_player_id',
            'rusher_player_name', 'rusher_player_id',
            'receiver_player_name', 'receiver_player_id'],
            axis=1, inplace=True)
        print("reg", i)
        i_data = i_data.loc[i_data.season_type=='REG']
        print("run pass no",i)
        i_data = i_data.loc[(i_data.play_type.isin(['no_play','pass','run'])) & (i_data.epa.isna()==False)]
        i_data.play_type.loc[i_data['pass']==1] = 'pass'
        i_data.play_type.loc[i_data.rush==1] = 'run'
        print("index reset",i)
        i_data.reset_index(drop=True, inplace=True)
        print('remove columns')
        i_data = i_data[columns]

        data = data.append(i_data, sort=True)

    print("reset index")
    data.reset_index(drop=True, inplace=True)

    print("save to csv")
    data.to_csv(file_descr + '_play_by_play_'+ year_from +'_to_'+ year_to +'.csv.gz', compression='gzip')



year_low = 1998
year_high = 2010

columns = ['game_id','posteam','play_type','epa','temp','season']
file_descr  = "temp"

#creates datafile
getD(1999, 2019, columns,file_descr)


