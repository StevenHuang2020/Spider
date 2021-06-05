#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#Description: statistic of world vaccinations
#Date: 2021/06/05
#Author: Steven Huang, Auckland, NZ
import os
import matplotlib.pyplot as plt
from plotCoronavirous import readCsv, gSaveBasePath
from plotCoronavirous import createPath

SMALL_SIZE = 10
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

#plt.rc('figure.dpi', 300)
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
#plt.rc('font', family='Times New Roman')
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=SMALL_SIZE)  # fontsize of the figure title

def plotData(df, title, kind='line', y='', fName='', logy=False):
    #fontsize = 4
    ax = df.plot(kind=kind, title=title, y=y, logy=logy)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    #plt.setp(ax.get_yticklabels()) #fontsize=fontsize
    #plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=0.14, right=0.96, top=0.92, wspace=None, hspace=None)
    plt.savefig(gSaveBasePath + 'World_' + fName+'.png')
    plt.show()
    
def plotWorldVaccinations(df): 
    df = df[df['location'] == 'World' ]
    df = df.drop(columns=['location','continent','iso_code'])
    df = df.dropna(subset=['total_vaccinations'])
    
    print('columns=', df.columns)
    #columns= Index(['date', 'total_vaccinations', 'people_vaccinated',
    #    'people_fully_vaccinated', 'new_vaccinations',
    #    'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
    #    'people_fully_vaccinated_per_hundred'],
    #   dtype='object')
    df.set_index(["date"], inplace=True)  
    print(df.head())
    
    kinds = ['line','bar','barh','hist','box','kde','density','area']  
    
    title = 'World people vaccinated'
    y=['people_vaccinated', 'people_fully_vaccinated']
    plotData(df, title=title, kind='line', y=y, fName='vaccinated')
    
    title = 'World vaccinated per hundred'
    y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred']
    plotData(df, title=title, kind='line', y=y, fName='vaccinatedPerHundred')
    
    title = 'World new vaccinated'
    y=['new_vaccinations']
    plotData(df, title=title, kind='bar', y=y, fName='vaccinatedNew')   
   
    title = 'World total vaccinated'
    y=['total_vaccinations']
    plotData(df, title=title, kind='bar', y=y, fName='vaccinatedTotal')   
    
def plotContinentVaccinations(df): 
    pass

def saveCountryVaccData(df, path=r'./OurWrold/vaccineCountry'):
    df = df[df['location'] != 'World' ]
    countries = list(df.location.unique())
    
    print('countries=', countries)
    createPath(path)
    for c in countries:
        dfCountry = df[df['location'] == c ]
        dfCountry.set_index(["date"], inplace=True)  
        #print(dfCountry.head())
        dfCountry.to_csv(os.path.join(path, 'vaccination_'+c+'.csv'), index=True)
        #break
        
def plotConuntryVaccinations(): 
    vaccCountryPath=r'./OurWrold/vaccineCountry'
    pass

def main():
    file = r'./OurWrold/vaccinations.csv'
    df = readCsv(file)
    
    saveCountryVaccData(df)
    plotWorldVaccinations(df)
    plotConuntryVaccinations()
    #plotContinentVaccinations(df)
    
if __name__=="__main__":
    main()
