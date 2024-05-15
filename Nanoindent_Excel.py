# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 04:40:12 2024

@author: joktavia
"""

#Nanoindentation Reviewed Dmaxmin Dfmaxfmin#

#import Libraries
import pandas as pd 
import numpy as np 
import os
import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import find_peaks, argrelextrema
from openpyxl import Workbook 
from openpyxl.utils.dataframe import dataframe_to_rows



#DataPrep read the Load function in column wise with these information
nano = pd.read_csv("v3.txt", sep = ',') 
index = nano.columns
df = nano[[
    'SegmentTime', 'BeginTime', 'EndTime', 
    'BeginLoad','EndLoad', 
    'NumofSeqPoints', 'Aquisition_rate']]

#express data as float

df = df.astype('float64')

print(df[['BeginLoad','EndLoad']])

#add start and end column (datapoint)
for i in range(len(df)):
    if i > 0:
        val = df.iloc[:i,5].sum() + 1
        y = df.iloc[:i+1,5].sum()
        #print(val)
        #print(y)
        df.loc[i,'Start'] = val
        df.loc[i,'End'] = y
    else:
        val=0
        y = df.iloc[i,5].sum()
        #print(val)
        #print(y)
        df.loc[i,'Start'] = val
        df.loc[i,'End'] = y
        
#print(df)

#define hold segment
loca = np.where(np.logical_and(df['BeginLoad'] == df['EndLoad'], df['BeginLoad'] == 400) , df.index, 0 )    
loca = np.trim_zeros(loca)
loca = [l for l in loca if l != 0]
print(loca)
#retain important position to find HS 
start=[]
end=[]  
HS_dict = {}
for idx_,value in enumerate(loca):
    data1 = df.loc[value,'Start'].astype('int64')
    data2 = df.loc[value,'End'].astype('int64')
    start.append(data1)
    end.append(data2)

#upload load and depth data
flname = os.listdir('FL_3')
for i in range (len(flname)):
    #os.mkdir('RESULTS/FL_3_' + str(i))
    LF = pd.read_csv('FL_3/' + flname[i],engine='python',encoding = "cp1252",skiprows=[0,1,2,3,4],sep='\t')   
    idx = LF.columns
    df1 = LF[['Depth (nm)', 'Load (µN)', 'Time (s)']]
    

#plot HS
     
    for idx_,value in enumerate(start):
        df_HS = df1.loc[value:end[idx_]]
        if idx_ == 0:
            HS_start= df_HS[df_HS['Time (s)'].gt(4)].index[0]
        else:
            HS_start= df_HS[df_HS['Time (s)'].gt(375)].index[0]
        
        plotHS = df1.iloc[HS_start:end[idx_],:]
        fig2 = plotHS.plot(kind = 'scatter', x ='Time (s)'  ,y = 'Load (µN)'
                            , ylabel = 'Load (µN)'  , xlabel = 'Time (s)')
        fig2.figure.savefig(f'RESULTS/FL_3_{i}/Plot/HS_cut_{idx_}.png')
        plt.show()
        
        #regression with numpy
        reg = np.polyfit( plotHS['Time (s)'], plotHS['Load (µN)'], deg= 1 )
        HS_idx = (f'{i}/{idx_}')
        HS_dict[HS_idx] = reg
        
    
#add time in dataframe
a=0
b=1
steigung ={}
HS_df = pd.DataFrame(data=HS_dict, index= ['m','c'])
HS_df = (HS_df.T)
len(HS_df)/2
for i in range(16):
    HS_df.loc[f'{i}/{a}','Time(s)'] = 4
    HS_df.loc[f'{i}/{b}','Time(s)'] = 375
    HS_plot = HS_df.loc[f'{i}/{a}':f'{i}/{b}',:]
   
    fig3 = HS_plot.plot(kind = 'line', x = 'Time(s)',y = ['m']
                        , xlabel = 'Time(s)'  , ylabel = 'Steigung')
    fig3.figure.savefig(f'RESULTS/FL_3_{i}/Dmaxplot/HS_{i}.png')
    reg2 = np.polyfit( HS_plot['Time(s)'], HS_plot['m'], deg= 1 )
    exper= (f'{i}')
    steigung[exper] = reg2
            
#print(HS_df)
HS_df.to_excel('RESULTS/Driftrate.xlsx')
print(steigung)





