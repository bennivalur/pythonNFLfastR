import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

def getImage(path): 
    return OffsetImage(plt.imread(path), zoom=.5)

teams = ['BREI','FH','FJO','FYL','GRO','HK','IA','KA','KR','STJA','VAL','VIKR']

BREI = ['BREI',9,14,1.88,1.35]
FH = ['FH',8,14,1.13,1.18]
FJO = ['FJO',9,3,1.27,1.58]
FYL = ['FYL',9,15,1.31,1.77]
GRO = ['GRO',9,5,0.9,1.64]
HK = ['HK',9,8,1.14,1.52]
IA = ['IA',9,10,1.34,1.73]
KA = ['KA',8,8,0.95,1.36]
KR = ['KR',8,17,1.53,0.94]
STJA = ['STJA',6,14,1.6,1.59]
VAL = ['VAL',9,19,2.01,1.25]
VIKR = ['VIKR',9,13,1.55,1.16]

data = [BREI,FH,FJO,FYL,GRO,HK,IA,KA,KR,STJA,VAL]

for i in data:
    xGD = i[3] - i[4]
    i.append(xGD)
    avgPts = float(i[2]) / float(i[1])
    i.append(avgPts)

df = pd.DataFrame(data,columns=['club','games','points','xg','xga','xgd','avgPts'])

logos = os.listdir(os.getcwd() + '/pepsi_max_logos')

logo_paths = []

for i in logos:
    logo_paths.append(os.getcwd() + '/pepsi_max_logos/' + str(i))

x = df['xgd']
y = df['avgPts']

fig, ax = plt.subplots(figsize=(10,10))

#Make a scatter plot first to get the points to place logos
ax.scatter(x, y, s=.001)

#Adding logos to the chart
for x0, y0, path in zip(x, y, logo_paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False, fontsize=4)
    ax.add_artist(ab)

#Adding labels and text
ax.set_ylabel('Points Per Game', fontsize=16)
ax.set_xlabel('Expected Goals Difference', fontsize=16)

#Add a grid
ax.grid(zorder=0,alpha=.4)
ax.set_axisbelow(True)

#ax.invert_xaxis()

ax.set_title('PEPSI MAX Performance Vs. Results', fontsize=20)
plt.figtext(.81, .07, 'Data: footystats.org | graph: @bennivaluR_', fontsize=12)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 
        color='darkorange', linestyle='--')

#Create directory if it does not exist
try: 
    os.makedirs('pepsi_graphs')
except OSError:
    if not os.path.isdir('pepsi_graphs'):
        raise

#Save the figure as a png
plt.savefig('pepsi_graphs/pepsiXGvsXGA.png', dpi=400)
