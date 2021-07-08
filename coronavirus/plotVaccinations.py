#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#Description: statistic of world vaccinations
#Date: 2021/06/05
#Author: Steven Huang, Auckland, NZ
import os
import datetime
from numpy.core.numeric import NaN
import pandas as pd
import matplotlib.pyplot as plt
from plotCoronavirous import readCsv, gSaveBasePath
from plotCoronavirous import getVaccinesFile,getDateStr,plotData
from plotCoronavirous import SMALL_SIZE
from predictStatistics import plotDataAx,binaryDf
from commonPath import createPath,getFileName,pathsFiles
from common.getHtml import downWebFile

#data source: https://ourworldindata.org/covid-vaccinations?country=OWID_WRL
gCovidCsv = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv' 

    
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
    
    title = 'World people vaccinated,' + getDateStr()
    y=['people_vaccinated', 'people_fully_vaccinated']
    fileName = gSaveBasePath + 'World_vaccinated.png'
    color=['#1f77b4','r']
    plotData(df, title=title, kind='line', y=y, fName=fileName, color=color, show=False)
    
    title = 'World vaccinated per hundred,' + getDateStr()
    y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred']
    fileName = gSaveBasePath + 'World_vaccinatedPerHundred.png'
    plotData(df, title=title, kind='line', y=y, fName=fileName, color=color, show=False)
    
    title = 'World new vaccinated,' + getDateStr()
    y=['new_vaccinations']
    fileName = gSaveBasePath + 'World_vaccinatedNew.png'
    plotData(df, title=title, kind='bar', y=y, fName=fileName, show=False)   
   
    title = 'World total vaccinated,' + getDateStr()
    y=['total_vaccinations']
    fileName = gSaveBasePath + 'World_vaccinatedTotal.png'
    plotData(df, title=title, kind='bar', y=y, fName=fileName, show=False)   
    plt.show()
    
def plotVaccinationRankings(dfAll): 
    #----vaccine contienet ranking------
    plotContinentVaccinations(dfAll)
    
    top = 25
    dfCountries = dfAll[dfAll['continent'].notnull()] #remain countries not continent
    dfCountries.set_index(["location"], inplace=True)  
    print('dfCountries=\n', dfCountries)
    
    #----vaccinated people ranking------
    dfCountries = dfCountries.sort_values(by=['people_vaccinated'], ascending=False)
    dfData = dfCountries.iloc[:top, :]
    title = 'Top ' + str(top) + ' countries people vaccinated,' + getDateStr()
    y=['people_vaccinated']
    fileName = gSaveBasePath + 'World_vaccineRankingPeople.png'
    plotData(dfData, title=title, kind='bar', y=y, fName=fileName, show=False)
    
    #----vaccinated peope per hundred ranking------
    dfCountries = dfCountries.sort_values(by=['people_vaccinated_per_hundred'], ascending=False)
    dfData = dfCountries.iloc[:top, :]
    title = 'Top ' + str(top) + ' countries people vaccinated per hundred,' + getDateStr()
    y=['people_vaccinated_per_hundred']
    fileName = gSaveBasePath + 'World_vaccineRankingPeoplePerH.png'
    plotData(dfData, title=title, kind='bar', y=y, fName=fileName, color=['#1f77b4','r'], show=False)
    plt.show()
    
def plotContinentVaccinations(dfAll): 
    dfContinent = dfAll[dfAll['continent'].isnull()]  
    print('dfContinent=\n', dfContinent)
    dfContinent.set_index(["location"], inplace=True)  
    title = 'Continent vaccinated,' + getDateStr()
    y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred']
    fileName = gSaveBasePath + 'World_vaccineContinent.png'
    plotData(dfContinent, title=title, kind='bar', y=y, fName=fileName, bottom=0.16, color=['#1f77b4','r'], show=False)

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
    """
    @Desciption
    Interpolate df to identical length for plot multi-countries' data at same 
    date range. If this function is not called, the plot will not be smooth. 
    Please note that there are various date formats, improper 
    handling will cause this function to crash. Date comparison must be under 
    DateTime format instead of string.
    
    Date format: #Reference: https://docs.python.org/3/library/datetime.html
    '01/02/2021'    %m/%d/%Y
    '01/02/21'      %m/%d/%y
    '1/2/2021'      %#m/%#d/%Y
    '2021-01-02'    %Y-%m-%d
    
    @parameters
    dateIndex: form '01/12/2021' to today, please see function getDateIndex()
    df: Pandas dataframe/series to be interpolated
    1) if df's line is NaN, set zeor if first line or the previous day's value
    2) if df's date index out of dateIndex, remove the line
    3) if df does not contain a row with index belongs to dateIndex,interpolate by the value
        of the most recent day before in df.
    """
    
    df.sort_index(inplace=True) 
    #print('df=\n', df, df.shape)
    if pd.isna(df.iat[0]):
        df.iat[0] = 0
        #df.loc[df.keys()[0]] = 0
        
    for i in range(1, df.shape[0]):
        #print(i, df.iloc[i],  df.iloc[i-1])
        if pd.isna(df.iat[i]) or df.iloc[i]<df.iat[i-1]:
            #df.loc[df.keys()[i]] = df.iloc[i-1]
            df.iat[i] = df.iat[i-1]
            #df.iloc[i] = df.iat[i-1]
            #print(df.iloc[i])

    #df.to_csv(os.path.join(r'./OurWrold', 'test.csv'), index=True)  
    #print('before df=\n', df, df.shape)
    
    #print('dateIndex=', dateIndex, len(dateIndex), type(dateIndex)) # 06/06/2021
    indexFmt='%#m/%#d/%y'
    if '-' in df.keys()[0]:
        indexFmt='%Y-%m-%d'
        
    for index in df.keys():
        try:
            indexD, indexStr = strToDate(index, inFmt=indexFmt, outFmt='%m/%d/%Y')
            if indexStr not in dateIndex:
                df = df.drop(labels=[index])
        except:
            assert('Date format processing error!')
            print('Date format not same, index=', index)
            
    #print('df=\n', df, df.shape)
    #start = df['2021-01-12'] #df.iloc[0]
    #print('start=', start)
    #print('df.keys()=', df.keys(), 'minKey, maxKey=', df.keys()[0], df.keys()[-1])
            
    for i, date in enumerate(dateIndex):
        indexD, indexStr = strToDate(date, inFmt='%m/%d/%Y', outFmt=indexFmt)
        if indexStr not in df.keys():
            minKey, maxKey = df.keys()[0], df.keys()[-1]
            #print(i, 'indexStr=', indexStr, 'minKey, maxKey=', minKey, maxKey)

            minKeyD,minKeyStr = strToDate(minKey, indexFmt, indexFmt)
            maxKeyD,maxKeyStr = strToDate(maxKey, indexFmt, indexFmt) 
            
            if indexD<=minKeyD: #comparison under datetime format not string 
                df.loc[indexStr] = df[minKey]
            elif indexD>=maxKeyD:
                df.loc[indexStr] = df[maxKey]
            else:
                dBefore = indexD - datetime.timedelta(days=1)
                dBeforeStr = datetime.datetime.strftime(dBefore, indexFmt)
                #print('indexStr,dBeforeStr=', indexStr, dBeforeStr, df.keys())
                df.loc[indexStr] = df[dBeforeStr]
                #print('indexStr,dBeforeStr=', indexStr, dBeforeStr, df[dBeforeStr])
                
            df.sort_index(inplace=True)    
                
    #print('after df=\n', df, df.shape)
    #print('df,dateIndex=', df.shape, len(dateIndex))
    #print('df.keys()=', df.keys())
    assert(df.shape[0] == len(dateIndex))
    
    #pd.to_datetime(df.index, infer_datetime_format=True)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    #df.to_csv(os.path.join(r'./OurWrold', 'test2.csv'), index=True)  
    #print('keys=', df.keys(),len(df.keys()))
    return df

def plotConuntryVaccinationsByTime(path, dfCountries, coloumnLabel, title, fileName, show=True):
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
    
    plt.clf()
    ax = plt.subplot(1,1,1)
    
    plt.title(title)
    for country, df in dfAll:
        df.set_index(["date"], inplace=True)
        y = df[coloumnLabel]
        y = InterpolationDf(dateIndex, y)

        inter = 2
        xIndex = dateIndex
        #print('type(y), type(xIndex)=', type(y), y.shape, type(xIndex),len(xIndex))
        xIndex = dateIndex[::inter] #Interval inter value
        y=y[[i%inter==0 for i in range(len(y.index))]]
        #print('type(y), type(xIndex)=', type(y), y.shape, type(xIndex),len(xIndex))
        
        plotDataAx(ax, y.index, y, country, fontsize=SMALL_SIZE)
        #break
    
    plt.ylim(0)
    plt.tight_layout()
    plt.savefig(fileName)
    if show:
        plt.show()
        
def plotConuntryVaccinations(vaccPath=r'./OurWrold/vaccineCountry'): 
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
    
    dfAll = []
    for fileCountry in pathsFiles(vaccPath, 'csv'):
        #fileCountry = os.path.join(vaccPath, 'vaccination_Burkina Faso.csv')
        line = getCountryNewestLine(fileCountry)
        #print('line=', line, type(line))
        if line is not None:
            dfAll.append(line)
        #break
        
    dfAll = pd.concat(dfAll)
    print(dfAll.head())
    print(dfAll.columns)
    
    plotVaccinationRankings(dfAll)
   
    #start to plot country's vaccination by time
    dfAll = dfAll[dfAll['continent'].notnull()] #remain countries not continent
    
    top = 20
    dfAll = dfAll.sort_values(by=['people_vaccinated_per_hundred'], ascending=False)
    print('dfAll=\n', dfAll)
    
    dfCountries = dfAll.iloc[:top, :]
    #dfCountries = dfAll[dfAll['location'] == 'Saint Helena' ]
    #print('dfCountries=\n', dfCountries)
    
    fileName = gSaveBasePath + 'World_vaccinePerH_top.png'
    title = 'Top ' + str(top) + ' countries vaccinated per hundred,' + getDateStr()
    columnLabel = 'people_vaccinated_per_hundred'
    plotConuntryVaccinationsByTime(vaccPath, dfCountries, columnLabel, title, fileName)
    
    dfAll = dfAll.sort_values(by=['people_fully_vaccinated_per_hundred'], ascending=False)
    dfCountries = dfAll.iloc[:top, :]
    fileName = gSaveBasePath + 'World_vaccineFully_top.png'
    title = 'Top ' + str(top) + ' countries vaccinated fully,' + getDateStr()
    columnLabel = 'people_fully_vaccinated_per_hundred'
    plotConuntryVaccinationsByTime(vaccPath, dfCountries, columnLabel, title, fileName)
      
    top = 20
    dfAll = dfAll.sort_values(by=['people_vaccinated'], ascending=False)
    #print(dfAll.head())
    dfCountries = dfAll.dropna(subset=['continent']) #remove continent only remain countries
    dfCountries = dfCountries.iloc[:top, :]
    fileName = gSaveBasePath + 'World_peopleVaccined_top.png'
    title = 'Top ' + str(top) + ' countries people vaccinated,' + getDateStr()
    columnLabel = 'people_vaccinated'
    plotConuntryVaccinationsByTime(vaccPath, dfCountries, columnLabel, title, fileName)
    
    countries = list(dfAll.location.unique())
    #print('countries=', countries)
    observeCountries=['United Kingdom', 'United States', 'Brazil', 'Germany', 'France', \
        'Russia', 'Turkey', 'Argentina', 'Colombia', 'Mexico', 'Ukraine', 'Peru', \
        'Indonesia', 'Iran', 'Poland', 'Spain'] #select country in countries
    
    #observeCountries=['Chile', 'Mongolia', 'Bahrain', 'Seychelles']
    
    dfCountries = dfAll[dfAll.location.isin(observeCountries)]
    
    fileName = gSaveBasePath + 'World_peopleVaccined_topCasesCountries.png'
    title = 'Top covid-19 cases countries people vaccinated,' + getDateStr()
    columnLabel = 'people_vaccinated'
    plotConuntryVaccinationsByTime(vaccPath, dfCountries, columnLabel, title, fileName)
    
    fileName = gSaveBasePath + 'World_peopleVaccinedPerH_topCasesCountries.png'
    title = 'Top covid-19 cases countries people vaccinated per hundred,' + getDateStr()
    columnLabel = 'people_vaccinated_per_hundred'
    plotConuntryVaccinationsByTime(vaccPath, dfCountries, columnLabel, title, fileName)
    
    
def downloadOurWorldData(csvpath=r'./OurWrold/'):
    createPath(csvpath)
    file = os.path.join(csvpath, 'owid-covid-data.csv')
    downWebFile(gCovidCsv, file)
    return file
    
def main():
    path = r'./OurWrold/'
    vaccineFile = os.path.join(path, 'vaccinations.csv')
    vaccCountryPath = os.path.join(path, 'vaccineCountry')
    createPath(vaccCountryPath)
    
    download = True
    if download:
        dataAllFile = downloadOurWorldData(path)
        #dataAllFile = os.path.join(path, 'owid-covid-data.csv')
        getVaccinesFile(dataAllFile, vaccineFile)
    
    df = readCsv(vaccineFile)
    saveCountryVaccData(df)
    
    plotWorldVaccinations(df)
    plotConuntryVaccinations(vaccCountryPath)
    
if __name__=="__main__":
    main()
