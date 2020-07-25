import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from getData import getD

def getImage(path): 
    return OffsetImage(plt.imread(path), zoom=.5)

teams = ['BREI','FH','FJO','FYL','GRO','HK','IA','KA','KR','STJA','VAL','VIKR']

BREI = ['BREI',1.62,1.3]
FH = ['FH',1.25,1.18]
FJO = ['FJO',1.29,1.43]
FYL = ['FYL',1.11,1.69]
GRO = ['GRO',0.86,1.51]
HK = ['HK',0.94,1.34]
IA = ['IA',1.06,1.51]
KA = ['KA',1.27,1.44]
KR = ['KR',1.53,0.94]
STJA = ['STJA',1.47,1.38]
VAL = ['VAL',1.89,1.23]
VIKR = ['VIKR',1.39,1.18]

data = [BREI,FH,FJO,FYL,GRO,HK,IA,KA,KR,STJA,VAL]

df = pd.DataFrame(data,columns=['club','xg','xga'])

logos = os.listdir(os.getcwd() + '/pepsi_max_logos')

logo_paths = []

for i in logos:
    logo_paths.append(os.getcwd() + '/pepsi_max_logos/' + str(i))

x = df['xga']
y = df['xg']

fig, ax = plt.subplots(figsize=(10,10))

#Fixed size of graph, good for making animations
#ax.set_ylim([-0.35,0.40])
#ax.set_xlim([-0.37,0.47])

#Make a scatter plot first to get the points to place logos
ax.scatter(x, y, s=.001)

#Adding logos to the chart
for x0, y0, path in zip(x, y, logo_paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False, fontsize=4)
    ax.add_artist(ab)

#Adding labels and text
ax.set_ylabel('Expected Goals', fontsize=16)
ax.set_xlabel('Expected Goals Against', fontsize=16)

#Add a grid
ax.grid(zorder=0,alpha=.4)
ax.set_axisbelow(True)

ax.invert_xaxis()

ax.set_title('PEPSI MAX expected goals vs expected goals against', fontsize=20)
plt.figtext(.81, .07, 'Data: footystats.org', fontsize=12)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), 
        color='darkorange', linestyle='--')

#Save the figure as a png
plt.savefig('pepsi_graphs/pepsiXGvsXGA.png', dpi=400)
