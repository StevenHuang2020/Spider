#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#Description: statistic of world vaccinations
#Date: 2021/06/05
#Author: Steven Huang, Auckland, NZ
import os
import datetime
from numpy.core.numeric import NaN
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from plotCoronavirous import readCsv, gSaveBasePath,binaryDf
from predictStatistics import plotDataAx
from commonPath import createPath,getFileName,pathsFiles

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

#matplotlib.rcParams['figure.dpi'] = 150 #high resolution 100~300

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
#plt.rc('font', family='Times New Roman')
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=SMALL_SIZE)   # fontsize of the figure title

def getDataStr():
    now = datetime.datetime.now()
    return str(' Date:') + str(now.strftime("%Y-%m-%d %H:%M:%S"))

def plotData(df, title, kind='line', y='', fName='', logy=False, save=True, bottom=0.14):
    #fontsize = 4
    ax = df.plot(kind=kind, title=title, y=y, logy=logy)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    #plt.setp(ax.get_yticklabels()) #fontsize=fontsize
    #plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=bottom, right=0.96, top=0.92, wspace=None, hspace=None)
    if save:
        plt.savefig(fName)
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
    
    title = 'World people vaccinated,' + getDataStr()
    y=['people_vaccinated', 'people_fully_vaccinated']
    fileName = gSaveBasePath + 'World_vaccinated.png'
    plotData(df, title=title, kind='line', y=y, fName=fileName)
    
    title = 'World vaccinated per hundred,' + getDataStr()
    y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred']
    fileName = gSaveBasePath + 'World_vaccinatedPerHundred.png'
    plotData(df, title=title, kind='line', y=y, fName=fileName)
    
    title = 'World new vaccinated,' + getDataStr()
    y=['new_vaccinations']
    fileName = gSaveBasePath + 'World_vaccinatedNew.png'
    plotData(df, title=title, kind='bar', y=y, fName=fileName)   
   
    title = 'World total vaccinated,' + getDataStr()
    y=['total_vaccinations']
    fileName = gSaveBasePath + 'World_vaccinatedTotal.png'
    plotData(df, title=title, kind='bar', y=y, fName=fileName)   
    
def plotContinentVaccinations(dfAll): 
    dfContinent = dfAll[dfAll['continent'].isnull()]  
    print('dfContinent=\n', dfContinent)
    dfContinent.set_index(["location"], inplace=True)  
    title = 'Continent vaccinated,' + getDataStr()
    y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred']
    fileName = gSaveBasePath + 'World_vaccineContinent.png'
    plotData(dfContinent, title=title, kind='bar', y=y, fName=fileName, bottom=0.16)

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
      
def getDateIndex(start='1/12/2021'):
    newIndex=[]
    sD=datetime.datetime.strptime(start,'%m/%d/%Y') 
    startIndex = datetime.datetime.strftime(sD,'%m/%d/%Y')
    newIndex.append(startIndex)
    
    today = datetime.datetime.now().strftime('%m/%d/%Y')
    todayD = datetime.datetime.strptime(today,'%m/%d/%Y')
    #print('startIndex,today=', startIndex, today)
    dayLen = (todayD-sD).days
    #print('days=', dayLen)
    for i in range(dayLen):
        d = sD + datetime.timedelta(days=i+1)
        d = datetime.datetime.strftime(d,'%m/%d/%Y')
        #print(d)
        newIndex.append(d)
    #print('newIndex=', newIndex)
    return newIndex
  
def strToDate(str , inFmt='%Y-%m-%d', outFmt='%m/%d/%Y'):
    strD=datetime.datetime.strptime(str,inFmt) 
    strOut = datetime.datetime.strftime(strD,outFmt)
    return strD,strOut

def InterpolationDf(dateIndex, df):
    #print('df=\n', df, df.shape)
    if pd.isna(df.iat[0]):
        #df.iloc[0] = 0
        df.loc[df.keys()[0]] = 0

    for i in range(1, df.shape[0]):
        #print(i, df.iloc[i],  df.iloc[i-1])
        if pd.isna(df.iat[i]) or df.iloc[i]<df.iat[i-1]:
            #df.loc[df.keys()[i]] = df.iloc[i-1]
            df.iloc[i] = df.iat[i-1]
            #print(df.iloc[i])
         
    #df.to_csv(os.path.join(r'./OurWrold', 'test.csv'), index=True)  
    #print('before df=\n', df, df.shape)
    
    #print('dateIndex=', dateIndex, len(dateIndex), type(dateIndex)) # 06/06/2021
    for index, value in df.items():
        #print(index, value) #2021-05-27 115.86
        #indexD=datetime.datetime.strptime(index,'%Y-%m-%d') 
        #indexStr = datetime.datetime.strftime(indexD,'%m/%d/%Y')
        indexD, indexStr = strToDate(index)
        
        if indexStr not in dateIndex:
            df = df.drop(labels=[index])
    #print('df=\n', df, df.shape)
    #start = df['2021-01-12'] #df.iloc[0]
    #print('start=', start)
    for i, date in enumerate(dateIndex):
        indexD, indexStr = strToDate(date, inFmt='%m/%d/%Y', outFmt='%Y-%m-%d')
        #indexD=datetime.datetime.strptime(date,'%m/%d/%Y') 
        #indexStr = datetime.datetime.strftime(indexD,'%Y-%m-%d')
        if indexStr not in df.keys():
            #print('indexStr=', indexStr)
            minKey, maxKey = df.keys()[0], df.keys()[-1]
            minKeyD,minKeyStr = strToDate(minKey, '%Y-%m-%d', '%Y-%m-%d')
            maxKeyD,maxKeyStr = strToDate(maxKey, '%Y-%m-%d', '%Y-%m-%d')
            
            if indexD<=minKeyD:
                df.loc[indexStr] = df[minKeyStr]
            elif indexD<=maxKeyD:
                df.loc[indexStr] = df[maxKeyStr]
            else:
                dBefore = indexD - datetime.timedelta(days=1)
                dBeforeStr = datetime.datetime.strftime(dBefore,'%Y-%m-%d')
                #print('indexStr,dBeforeStr=', indexStr, dBeforeStr, df.keys())
                df.loc[indexStr] = df[dBeforeStr]
                #print('indexStr,dBeforeStr=', indexStr, dBeforeStr, df[dBeforeStr])
                
    #print('after df=\n', df, df.shape)
    df.sort_index(inplace=True)
    #df.to_csv(os.path.join(r'./OurWrold', 'test2.csv'), index=True)  
    #print('keys=', df.keys(),len(df.keys()))
    return df

def plotConuntryVaccinationsByTime(path, dfCountries, coloumnLabel, title, fileName):
    dateIndex = getDateIndex()

    #print('dfCountries=\n', dfCountries)
    countries = list(dfCountries.location.unique())
    #print('countries=', countries)
    dfAll = []
    for country in countries:
        name = 'vaccination_' + country + '.csv'
        #print(name)
        file = os.path.join(path, name)
        df = readCsv(file)
        dfAll.append((country, df))
    
    ax = plt.subplot(1,1,1)
    
    plt.title(title)
    for country, df in dfAll:
        df.set_index(["date"], inplace=True)
        y = df[coloumnLabel]
        y = InterpolationDf(dateIndex, y)
        #y = binaryDf(y)
        inter = 2
        xIndex = dateIndex
        #print('type(y), type(xIndex)=', type(y), y.shape, type(xIndex),len(xIndex))
        xIndex = dateIndex[::inter] #Interval inter value
        y=y[[i%inter==0 for i in range(len(y.index))]]
        #print('type(y), type(xIndex)=', type(y), y.shape, type(xIndex),len(xIndex))
        
        plotDataAx(ax, xIndex, y, country, fontsize=SMALL_SIZE)
        #break
    
    plt.ylim(0)
    plt.tight_layout()
    plt.savefig(fileName)
    plt.show()
        
def plotConuntryVaccinations(): 
    def getCountryNewestLine(file):
        country=getFileName(file)[len('vaccination_'):-4]
        #print('country=', country)
        
        df = readCsv(file)
        #df = df.drop(columns=['continent','iso_code'])
        df = df.dropna(subset=['total_vaccinations'])
        df.set_index(["date"], inplace=True)  
        if not df.empty:
            #print('df=', df.head())
            newestLine = df.iloc[[-1]]
            #vaccPerH = newestLine['people_vaccinated_per_hundred']
            #vaccFullPerH = newestLine['people_fully_vaccinated_per_hundred']
            #print('vaccPerH,vaccFullPerH=', vaccPerH, vaccFullPerH)
            return newestLine
        return None
    
    
    vaccCountryPath=r'./OurWrold/vaccineCountry'
    dfAll = []
    for fileCountry in pathsFiles(vaccCountryPath, 'csv'):
        #fileCountry = os.path.join(vaccCountryPath, 'vaccination_Burkina Faso.csv')
        line = getCountryNewestLine(fileCountry)
        #print('line=', line, type(line))
        if line is not None:
            dfAll.append(line)
        #break
        
    dfAll = pd.concat(dfAll)
    print(dfAll.head())
    print(dfAll.columns)

    plotContinentVaccinations(dfAll)
    
    top = 10
    dfAll = dfAll.sort_values(by=['people_vaccinated_per_hundred'], ascending=False)
    print('dfAll=\n', dfAll)
    
    dfCountries = dfAll.iloc[:top, :]
    #dfCountries = dfAll[dfAll['location'] == 'Falkland Islands' ]
    #print('dfCountries=\n', dfCountries)
    
    fileName = gSaveBasePath + 'World_vaccinePerH_top.png'
    title = 'Top ' + str(top) + ' countries vaccinated per hundred,' + getDataStr()
    columnLabel = 'people_vaccinated_per_hundred'
    plotConuntryVaccinationsByTime(vaccCountryPath, dfCountries, columnLabel, title, fileName)
   
    dfAll = dfAll.sort_values(by=['people_fully_vaccinated_per_hundred'], ascending=False)
    dfCountries = dfAll.iloc[:top, :]
    fileName = gSaveBasePath + 'World_vaccineFully_top.png'
    title = 'Top ' + str(top) + ' countries vaccinated fully,' + getDataStr()
    columnLabel = 'people_fully_vaccinated_per_hundred'
    plotConuntryVaccinationsByTime(vaccCountryPath, dfCountries, columnLabel, title, fileName)
 
    dfAll = dfAll.sort_values(by=['people_vaccinated'], ascending=False)
    #print(dfAll.head())
    dfCountries = dfAll.dropna(subset=['continent']) #remove continent only remain countries
    dfCountries = dfCountries.iloc[:top, :]
    fileName = gSaveBasePath + 'World_peopleVaccined_top.png'
    title = 'Top ' + str(top) + ' countries people vaccinated,' + getDataStr()
    columnLabel = 'people_vaccinated'
    plotConuntryVaccinationsByTime(vaccCountryPath, dfCountries, columnLabel, title, fileName)
    
    
def main():
    file = r'./OurWrold/vaccinations.csv'
    df = readCsv(file)
    
    #saveCountryVaccData(df)
    #plotWorldVaccinations(df)
    plotConuntryVaccinations()
    #plotContinentVaccinations(df)
    
if __name__=="__main__":
    main()
