# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:21:22 2018

@author: ywanggp
"""

import sys
sys.path.append("Functions")
from obtainScore import *
from jumpDays import *
from givePath import *
from submitFormat import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

#trainPredFile = "C:/Users/ywanggp/Downloads/ForecastDataforTraining_201712.csv"
#trainTrueFile = "C:/Users/ywanggp/Downloads/In_situMeasurementforTraining_201712.csv"
#testPredFile = "C:/Users/ywanggp/Downloads/ForecastDataforTesting_201712.csv"
#cityLocFile = "C:/Users/ywanggp/Downloads/CityData.csv"

trainPredFile = "C:\Users\lzhaoai\Desktop\predict_weather\ForecastDataforTraining_201712.csv"
trainTrueFile = "C:\Users\lzhaoai\Desktop\predict_weather\In_situMeasurementforTraining_201712.csv"
testPredFile = "C:\Users\lzhaoai\Desktop\predict_weather\ForecastDataforTesting_201712.csv"
cityLocFile = "C:\Users\lzhaoai\Desktop\predict_weather\CityData.csv"
testTrueFile = "C:\Users\lzhaoai\Desktop\predict_weather\predict_model_3.csv"
submitPath = "C:\Users\lzhaoai\Desktop\predict_weather\submitResult.csv"

cityLoc = pd.read_csv(cityLocFile)
xCity = cityLoc['xid']
yCity = cityLoc['yid']
file = testTrueFile

xsize = 548
ysize = 421

maxDay = 5
maxCity = 10

chunksize = xsize * ysize
df = pd.read_csv(file, chunksize = chunksize)
df1 = pd.read_csv(file, chunksize = chunksize)

block = []
fullScore = []
for dayNum in [1]: #range(1, maxDay + 1):
    for cityNum in [2,9]: #range(1, maxCity + 1):
        df = pd.read_csv(file, chunksize = chunksize)
        df = jumpDays(df, dayNum, chunksize)

        (pathList, windGra) = givePath(df, np.asarray([xCity[0], yCity[0]]),
                                   np.asarray([xCity[cityNum], yCity[cityNum]]),
                                   xsize, ysize, xCity, yCity)
        score = obtainScore(pathList, windGra)
        fullScore += [score]
        (string, des_n_day) = submitFormat(dayNum+5, cityNum, pathList)
        block += list(np.concatenate((des_n_day, string, pathList), axis = 1))
        
block = np.asarray(block)

#df1_block = df1.get_chunk(chunksize)
#windGra = df1_block["wind"].values.reshape(xsize,ysize)
#x = np.linspace(1, xsize, xsize)
#y = np.linspace(1, ysize, ysize)
#X,Y = np.meshgrid(y, x)
#CS = plt.contour(X, Y, windGra,levels = [15],
#                 colors=('k',),linestyles=('-',),linewidths=(1,))
#CSF = plt.contourf(X, Y, windGra, 8, alpha=.95, cmap=plt.cm.cool)
#plt.clabel(CS, fmt = '%2.1d', colors = 'k', fontsize=14) #contour line labels
#plt.colorbar(CSF, shrink=0.8, extend='both')
#plt.scatter(yCity[1:11], xCity[1:11], marker='x', s=50, c = 'gold', zorder=10)
#plt.scatter(pathList[:,1], pathList[:, 0], marker='x', s=5, c = 'gold', zorder=10)
#plt.scatter(yCity[0], xCity[0], marker='*', s=50, c = 'gold', zorder=10)
#plt.show()

#%%
#df_b = pd.DataFrame(block)
#df_b.to_csv(submitPath, header=None,index = False)
print fullScore
print sum(fullScore)