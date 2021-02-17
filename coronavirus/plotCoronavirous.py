#python3 unicode
#author:Steven Huang 25/04/20
#function: Query cases of COVID-19 from website
#World case statistics by time reference: https://ourworldindata.org/covid-cases
#
import sys
sys.path.append("..")
import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from progressBar import SimpleProgressBar
#from mainNZ import getNZCovid19
from common.getHtml import downWebFile

gSaveBasePath=r'.\images\\'
gSaveChangeData=r'.\dataChange\\'
gSaveCountryData=r'.\dataCountry\\'
gCovidCsv = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv' 


def plotData(df, number=25):    
    if number>df.shape[0]:
        number = df.shape[0]
    #df = df.iloc[1:number,:]
    worldDf = df.iloc[:1,:]
    df = df[1:]
    print(df.head())
    
    df = df.sort_values(by=['Confirmed'], ascending=False)
    # df1 = df.iloc[1:number,['Confirmed']]
    # print(df1)
    dfConfirmed = df.loc[:,['Confirmed']][:number]
    #print(dfConfirmed)
    
    df = df.sort_values(by=['NewCases'], ascending=False)
    dfNewCases = df.loc[:,['NewCases']][:number]

    df = df.sort_values(by=['Case_Per_1M_people'], ascending=False)
    dfCasePer1MPeople = df.loc[:,['Case_Per_1M_people']][:number]
    
    #df = df.sort_values(by=['Recovered'],ascending=False)
    #df3 = df.iloc[1:number,[2]]
    
    df = df.sort_values(by=['Deaths'], ascending=False)
    dfDeathes = df.loc[:,['Deaths']][:number]
    
    df = df.sort_values(by=['Mortality'], ascending=False)
    dfMortality = df.loc[:,['Mortality']][:number]

    dfDeaths200 = df[df['Deaths'] > 200]
    df6 = dfDeaths200.sort_values(by=['Mortality'], ascending=True).loc[:,['Mortality']][:number]

    dfConfirmed5K = df[df['Confirmed'] > 5000]
    df7 = dfConfirmed5K.sort_values(by=['Mortality'], ascending=True).loc[:,['Mortality']][:number]
        
    dfDeathsZero = df[df['Deaths'] == 0]
    df8 = dfDeathsZero.sort_values(by=['Confirmed'], ascending=False).loc[:,['Confirmed']][:number]
    
    dfDeathsThanZero = df[df['Deaths'] > 0]
    df9 = dfDeathsThanZero.sort_values(by=['Mortality'], ascending=True).loc[:,['Mortality']][:number]
    
    # print('df9.shape=',df8.shape)
    # print(df9)
    #print(df.head())
    #print(df.dtypes)
    #worldDf = df.loc['Worldwide']
    #print(worldDf)
    now = datetime.datetime.now()
    
    today = str(' Date:') + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    topStr = 'Top '+str(number) + ' '
    
    ccWorld = topStr + 'Confirmed(World: ' + str(int(worldDf['Confirmed'][0])) + today + ')'
    cpWorld = topStr + 'Case_Per_1M_people(World: ' + str(int(worldDf['Case_Per_1M_people'][0])) + today + ')'
    ncWorld = topStr + 'NewCases(World: ' + str(int(worldDf['NewCases'][0])) + today + ')'
    #reWorld = topStr + 'Recovered(World: ' + str(int(worldDf['Recovered'][0])) + today + ')'
    deWorld = topStr + 'Deaths(World: ' + str(int(worldDf['Deaths'][0]))+ today + ')'
    moWorld = topStr + 'Mortality(World: ' + str(round(worldDf['Mortality'][0],3)) + today + ')'
    moCountries = 'Mortality(Countries: ' + str(dfDeaths200.shape[0]) + ' Deaths>200' + today + ')'
    coCountries = 'Mortality(Countries: ' + str(dfConfirmed5K.shape[0]) + ' Confirmed>5k' + today + ')'
    dzCountries = 'Confirmed(Countries: ' + str(dfDeathsZero.shape[0]) + ' Deaths==0' + today + ')'
    dnzCountries = 'Mortality(Countries: ' + str(dfDeathsThanZero.shape[0]) + ' Deaths>0' + today + ')'
    
    dfs = [(ccWorld, dfConfirmed),(ncWorld, dfNewCases),(cpWorld, dfCasePer1MPeople),(deWorld, dfDeathes),\
        (moWorld, dfMortality),(moCountries,df6),(coCountries,df7),(dzCountries,df8),(dnzCountries,df9)]  #(reWorld, df3),

    fontsize = 7
    for i,data in enumerate(dfs): 
        dataFrame = data[1]
        print(i, data[0], 'Datashape:',dataFrame.shape)
        if dataFrame.shape[0] == 0:
            continue
            
        kind='bar'
        if number>25:
            dataFrame = binaryDf(dataFrame)
            kind='barh'
             
        title = data[0]

        if i in [1,3,4,5,6,8]: #deaths mortality
            ax = dataFrame.plot(kind=kind,color='r')
        else:
            ax = dataFrame.plot(kind=kind)

        ax.set_title(title,fontsize=fontsize)
        ax.legend(fontsize=fontsize)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
        plt.setp(ax.get_yticklabels(),fontsize=fontsize)
        
        if number>25:
            plt.subplots_adjust(left=0.30, bottom=None, right=0.98, top=None, wspace=None, hspace=None)
            
        plt.savefig(gSaveBasePath + str(i+1)+'.png')
    plt.show()
    
    #plotTable(worldDf)
    plotChangeBydata(fontsize = fontsize)
    #plotWorldStatConfirmCaseByTime()
    #plotWorldStatDeathsByTime()
    plotWorldStatisticByTime()
    plotNewCasesByCountry()
    plotCountriesInfo()
    #getNZCovid19()
    
def binaryDf(df,labelAdd=True):
    newdf = pd.DataFrame(columns=df.columns)
    #print('pd.shape=',df.shape)
    newIndex = []
    for i in range(df.shape[0]//2):
        #dd = df.loc[df.index[i*2], :]
        dd = df.iloc[i*2, :]
        #print('dd=',df.index[i*2], dd.values)
        if labelAdd:
            #print('index=',df.index[i*2])
            #print('new=',df.index[i*2] +',' + df.index[i*2+1])
            newIndex.append(str(df.index[i*2]) +',' + str(df.index[i*2+1])) #combine
        else:
            newIndex.append(df.index[i*2])#drop
            
        newdf = newdf.append(dd,ignore_index=True)
        
    #print('newIndex=',len(newIndex))
    #print('newdf.shape=',newdf.shape)
    newdf.index = newIndex
    return newdf

def plotTable(df):
    print(df)
    fig, ax = plt.subplots()
    # hide axes
    #fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    
    ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    plt.title('World statitic')
    #fig.tight_layout()
    plt.show()
    
def readCsv(file):
    df = pd.read_csv(file)
    #print(df.describe().transpose())
    #print(df.head())
    #df.set_index(["Location"], inplace=True)
    #print('df.columns=',df.columns)
    #print('df.dtypes = ',df.dtypes)
    #df = df.apply(pd.to_numeric, axis=0)
    #print('df.dtypes = ',df.dtypes)
    #plotTest(df)
    #plotDataCompare(df)
    return df
      
def plotTest(df,number = 20):
    #df = df.iloc[1:number,:]
    df = df.sort_values(by=['Confirmed'],ascending=False)
    df1 = df.iloc[1:number,[0]]
    df = df.sort_values(by=['Case_Per_1M_people'],ascending=False)
    df2 = df.iloc[1:number,[1]]
    df = df.sort_values(by=['Recovered'],ascending=False)
    df3 = df.iloc[1:number,[2]]
    df = df.sort_values(by=['Deaths'],ascending=False)
    df4 = df.iloc[1:number,[3]]
    df = df.sort_values(by=['Mortality'],ascending=False)
    df5 = df.iloc[1:number,[4]]

    dfDeaths = df[df['Deaths'] > 200]
    df6 = dfDeaths.sort_values(by=['Mortality'],ascending=True).iloc[:number,[4]]
    
    dfConfirmed = df[df['Confirmed'] > 5000]
    df7 = dfConfirmed.sort_values(by=['Mortality'],ascending=True).iloc[:number,[4]]
        
    #print(df.head())
    #print(df.dtypes)
    worldDf = df.loc[0] #'Worldwide'
    #print(worldDf,worldMor)
    now = datetime.datetime.now()
    
    today = str(' Date:') + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    ccWorld = 'Confirmed(World: ' + str(int(worldDf['Confirmed'])) + today + ')'
    cpWorld = 'Case_Per_1M_people(World: ' + str(int(worldDf['Case_Per_1M_people'])) + today + ')'
    reWorld = 'Recovered(World: ' + str(int(worldDf['Recovered'])) + today + ')'
    deWorld = 'Deaths(World: ' + str(int(worldDf['Deaths']))+ today + ')'
    moWorld = 'Mortality(World: ' + str(round(worldDf['Mortality'],3)) + today + ')'
    moCountries = 'Mortality(Countries: ' + str(dfDeaths.shape[0]) + ' Deaths>200' + today + ')'
    coCountries = 'Mortality(Countries: ' + str(dfConfirmed.shape[0]) + ' Confirmed>5k' + today + ')'
    
    #dfs = [(ccWorld, df1),(cpWorld, df2),(reWorld, df3),(deWorld, df4),(moWorld, df5),(moCountries,df6),(coCountries,df7)]
    
    df = df[df['Deaths'] > 0]
    df = df.iloc[1:,:]
    print('df.shape=',df.shape)
    
    df = binaryDf(binaryDf(df))
    
    dfs = [('test', df)]
    fontsize = 7
    for i,data in enumerate(dfs): 
        df = data[1]
        title = data[0]

        kinds = ['bar']# ['line','bar','barh','hist','box','kde','density','area']  
        for k in kinds:
            #df.plot(kind=k, title=k, y='Confirmed',  x = 'Deaths')
            #df.plot(kind=k, title=k, y='Confirmed')
            ax = df.plot(kind=k, title=k, y='Mortality')
            #plt.scatter(x=df['Deaths'], y=df['Confirmed'])
            plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
            plt.setp(ax.get_yticklabels(),fontsize=fontsize)
            plt.show()
            
        #kinds = ['pie','scatter','hexbin']
        kinds =[]# ['hexbin']
        for k in kinds:
            #df.plot(kind=k, title=k, y='Confirmed',  x = 'Deaths')
            #hexbin
            df.plot(kind=k, title=k, y='Confirmed',  x = 'Deaths', bins=10,xscale='log',yscale='log')
            #plt.scatter(x=df['Deaths'], y=df['Confirmed'])
            plt.show()
    
    plt.show()
    
def plotDataCompare(df,number = 50):
    #df = df.iloc[1:number,:]
    df = df.sort_values(by=['Confirmed'],ascending=False)
    df1 = df.iloc[1:number,[0]]
    df = df.sort_values(by=['Case_Per_1M_people'],ascending=False)
    df2 = df.iloc[1:number,[1]]
    df = df.sort_values(by=['Recovered'],ascending=False)
    df3 = df.iloc[1:number,[2]]
    df = df.sort_values(by=['Deaths'],ascending=False)
    df4 = df.iloc[1:number,[3]]
    df = df.sort_values(by=['Mortality'],ascending=False)
    df5 = df.iloc[1:number,[4]]

    dfDeaths = df[df['Deaths'] > 200]
    df6 = dfDeaths.sort_values(by=['Mortality'],ascending=True).iloc[:number,[4]]
    
    dfConfirmed = df[df['Confirmed'] > 5000]
    df7 = dfConfirmed.sort_values(by=['Mortality'],ascending=True).iloc[:number,[4]]
        
    dfDeathsZero = df[df['Deaths'] == 0]
    df8 = dfDeathsZero.sort_values(by=['Confirmed'],ascending=False).iloc[:number,[0]]
    
    dfDeathsThanZero = df[df['Deaths'] > 0]
    df9 = dfDeathsThanZero.sort_values(by=['Mortality'],ascending=True).iloc[:number,[4]]
    
    worldDf = df.loc[0] #Worldwide
    #print(worldDf,worldMor)
    now = datetime.datetime.now()
    
    today = str(' Date:') + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    ccWorld = 'Confirmed(World: ' + str(int(worldDf['Confirmed'])) + today + ')'
    cpWorld = 'Case_Per_1M_people(World: ' + str(int(worldDf['Case_Per_1M_people'])) + today + ')'
    reWorld = 'Recovered(World: ' + str(int(worldDf['Recovered'])) + today + ')'
    deWorld = 'Deaths(World: ' + str(int(worldDf['Deaths']))+ today + ')'
    moWorld = 'Mortality(World: ' + str(round(worldDf['Mortality'],3)) + today + ')'
    moCountries = 'Mortality(Countries: ' + str(dfDeaths.shape[0]) + ' Deaths>200' + today + ')'
    coCountries = 'Mortality(Countries: ' + str(dfConfirmed.shape[0]) + ' Confirmed>5k' + today + ')'
    dzCountries = 'Confirmed(Countries: ' + str(dfDeathsZero.shape[0]) + ' Deaths==0' + today + ')'
    dnzCountries = 'Mortality(Countries: ' + str(dfDeathsThanZero.shape[0]) + ' Deaths>0' + today + ')'
    
    dfs = [(ccWorld, df1),(cpWorld, df2),(reWorld, df3),(deWorld, df4),(moWorld, df5),\
        (moCountries,df6),(coCountries,df7),(dzCountries,df8),(dnzCountries,df9)]
    
    fontsize = 7
    #------------------------#
    df = df.sort_values(by=['Confirmed'],ascending=False)
    if number>25:
        df = binaryDf(df)
        
    #df.set_index(["Location"], inplace=True)
    
    dfConfirmed = df.iloc[1:number,[0]]
    dfCase_Per_1M_people = df.iloc[1:number,[1]]
    dfRecovered = df.iloc[1:number,[2]]
    dfDeaths = df.iloc[1:number,[3]]
    dfMortality = df.iloc[1:number,[4]]
    
    # print(dfConfirmed.head())
    # print(dfRecovered.head())
    # print(dfDeaths.head())
    
    colors=['b','g','r']
    width = 0.5
       
    #-------------------------#
    dC = dfConfirmed.iloc[:,0]
    dM = dfMortality.iloc[:,0]
    dD = dfDeaths.iloc[:,0]
    
    ax = plt.subplot(1,1,1)
    ax.clear()
    #ax.bar(dC.index, dC , width, label='Confirmed',color=colors[0])
    #ax.plot(dC.index, dC)
    ax.plot(dM.index, dM)
    ax.plot(dD.index, dD)
    #print(dM.index,dM.shape)
    ax.set_title('Confirmed & Mortality')
    
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
    plt.setp(ax.get_yticklabels(),fontsize=fontsize)
    #plt.subplots_adjust(left=0.30, bottom=None, right=0.98, top=None, wspace=None, hspace=None)
    plt.show()   
        
def pathsFiles(dir,filter=''): #"cpp h txt jpg"
    def getExtFile(file):
        return file[file.find('.')+1:]
    
    def getFmtFile(path):
        #/home/User/Desktop/file.txt    /home/User/Desktop/file     .txt
        root_ext = os.path.splitext(path) 
        return root_ext[1]

    fmts = filter.split()    
    if fmts:
        for dirpath, dirnames, filenames in os.walk(dir):
            filenames.sort()
            for filename in filenames:
                if getExtFile(getFmtFile(filename)) in fmts:
                    yield dirpath+'\\'+filename
    else:
        for dirpath, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                yield dirpath+'\\'+filename    
           
def getDateFromFileName(name):
    name = name[name.find('s')+1 : ]
    name = name[: name.find('.')]
    if name[0] == '_':
        name = name[1 : ]
    
    name = name[: name.rfind('_')]
    #print('name=',name)
    return name

def getAlldateWorldRecord(csvpath):
    def getWorldDf(df):
        #print('\n', df.head())
        #print(df.iloc[0]['Confirmed'], df.iloc[0]['Case_Per_1M_people'])
        #print(df.iloc[0]['Recovered'], df.iloc[0]['Deaths'], df.iloc[0]['Mortality'])
        
        try:
            totalConfirmed = int(np.sum(df.iloc[1:]['Confirmed']))
            #totalRecovered = int(np.sum(df.iloc[1:]['Recovered']))
            totalDeaths = int(np.sum(df.iloc[1:]['Deaths']))
            mortality = round(totalDeaths/totalConfirmed, 6)
        except:
            print('\n', df.head())
            
        #print('totalConfirmed=', totalConfirmed, totalRecovered, totalDeaths, mortality)
        df.loc['Worldwide', 'Confirmed'] = totalConfirmed
        #df.loc['Worldwide', 'Recovered'] = totalRecovered
        df.loc['Worldwide', 'Deaths'] = totalDeaths
        df.loc['Worldwide', 'Mortality'] = mortality
        
        #print('\n', df.head())
        worldDf = df.iloc[:1,:]
        return worldDf
    
    pdDate = pd.DataFrame()
    for i in pathsFiles(csvpath,'csv'):
        #print(i,getDateFromFileName(i))
        
        df = readCsv(i)
        df.set_index(["Location"], inplace=True)
        
        dateTime = getDateFromFileName(i)
        
        #print('\n', df.head())        
        if pdDate.shape[0]>0:
            if pdDate['DataTime'].isin([dateTime]).any():
                continue
            
        worldDf = getWorldDf(df)#df.iloc[:1,:]    
        #print('worldDf.shape=',worldDf.shape, worldDf)    
        #worldDf['DataTime'] = dateTime
        worldDf.insert(worldDf.shape[1], "DataTime", dateTime, True) 
        pdDate = pdDate.append(worldDf)
        #break
    
    #start add NewCases column
    pdDate = pdDate.drop(columns=['Cases per 1 million people'])
    #print('pdDate.columns=',pdDate.columns)
    #print('pdDate.dtypes=',pdDate.dtypes)
    pdDate["NewCases"] = 0
    for i in range(1, pdDate.shape[0]):#NewCases
        #print(pdDate.iloc[i,0], pdDate.iloc[i-1,0])
        pdDate.iloc[i, 6] =  pdDate.iloc[i,0] - pdDate.iloc[i-1,0]
        
    return pdDate

def plotChangeBydata(csvpath=r'./data/', fontsize = 7):
    def plotItem(df, str='all', title='World COVID19'):
        ax = df.plot(kind='line', xlabel='',ylabel='') #
        
        '''
        if str != 'all':
            pct=df.pct_change()
            #df.rename(columns={"A": "a", "B": "c"})
            #pct = pct.rename(index={0: "Change Rate"}) #Derivative
            pct.columns=["Change Rate"]#Derivative
            #print('pct=',pct)
            pct.plot(kind='line',ax=ax, xlabel='',ylabel='')
        '''    
        
        ax.set_title(title + ' ' + str)
        
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=fontsize)
        plt.setp(ax.get_yticklabels(), fontsize=fontsize)
        plt.subplots_adjust(left=0.07, bottom=0.16, right=0.96, top=0.94, wspace=None, hspace=None)
        #plt.yscale("log")
        plt.savefig(gSaveBasePath + 'WorldChange_' + str + '.png')
        #plt.show()
        
    pdDate = getAlldateWorldRecord(csvpath)
    # print(pdDate.head())
    # print(pdDate.shape)

    pdDate = pdDate.loc[:,['DataTime','Confirmed','NewCases','Case_Per_1M_people','Deaths','Mortality']]
    #print(pdDate.head())

    pdDate.set_index(["DataTime"], inplace=True)
    #df = pdDate.sort_values(by=['DataTime'],ascending=False)
    #print(pdDate)
    
    dfConfirmed = pdDate.loc[:,['Confirmed']]
    dfNewCases = pdDate.loc[:,['NewCases']]
    dfDeaths = pdDate.loc[:,['Deaths']]
    dfCasePer1MPeople = pdDate.loc[:,['Case_Per_1M_people']]
    dfMortality = pdDate.loc[:,['Mortality']]
    #print('dfConfirmed=\n', dfConfirmed)
    
    dfNewCases = dfNewCases[dfNewCases['NewCases'] > 0]
    dfCasePer1MPeople = dfCasePer1MPeople[dfCasePer1MPeople['Case_Per_1M_people'] > 0] #filter no data line
    #dfCasePer1MPeople = dfCasePer1MPeople.loc['2020-09-14' : ]

    plotItem(pdDate)
    plotItem(dfConfirmed,str='confirmed')
    plotItem(dfNewCases,str='newCases')
    plotItem(dfDeaths,str='deaths')
    plotItem(dfCasePer1MPeople,str='case_per1M_people')
    plotItem(dfMortality,str='mortality')
    plt.show()
    
def plotPdColumn(index,data,title,label,color=None):
    fontsize = 7
    plt.figure(figsize=(8,5))
    #ax = plt.subplot(1,1,1)
    plt.title(title,fontsize=fontsize)
    if color:
        plt.bar(index,data,label=label,width=0.6,color=color)
    else:            
        plt.bar(index,data,label=label,width=0.6)
    
    plt.xticks(rotation=30, ha="right",fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.subplots_adjust(left=0.08, bottom=None, right=0.98, top=0.92, wspace=None, hspace=None)
    #plt.yscale("log")
    plt.savefig(gSaveBasePath + 'World_' + label+'.png')
    #plt.show()
  
def getWorldDf(csvpath):
    all = getAlldateRecord(csvpath)
    
    df = pd.DataFrame() #all days world data
    for i in all:
        date = i[0]
        dataDf = i[1]
        
        #print(dataDf.head())
        wolrdLine = dataDf[dataDf['Location'] == 'Worldwide']
        #wolrdLine['Date'] = date
        wolrdLine.insert(0, "Date", [date], True) 
        df = df.append(wolrdLine)
            
    #print(df.head())    
    return df
 
def downloadFile(url,dstPath):
    fileName = url[url.rfind("/")+1:]
    print('Start file download:', url,'file:',fileName,'dst=',dstPath)
    
    if dstPath[-1] == '/':
        dst = dstPath + fileName
    else:
        dst = dstPath + "/" + fileName

    print('url=',url)
    #print('filename=',fileName)
    #print('dst=',dst)
    #wget.download(url, out=dst)
    return downWebFile(url,dst)
    
def plotWorldStatisticByTime(csvpath=r'./'):   
    fileName = 'owid-covid-data.csv'
    if os.path.exists(fileName):
        os.remove(fileName) 
    downloadFile(gCovidCsv, r'.')
    
    df = readCsv(gCovidCsv)
    df = df[df['location'] == 'World' ]
    
    dfWorld = df.loc[:,['date','total_cases','new_cases','total_deaths','new_deaths']]
    dfWorld.set_index(["date"], inplace=True)
    print(dfWorld.head())
    
    newRecentDays = 60
    dfWorldNew = dfWorld.iloc[-1-newRecentDays:-1, :]
    #dfWorld = dfWorld.iloc[::3]
    #dfWorld = binaryDf(dfWorld,False) #drop half
    strRecent = '{} days'.format(newRecentDays)
    
    plotPdColumn(dfWorld.index,dfWorld['total_cases'],title='World COVID-19 Cases',label='Cases')
    plotPdColumn(dfWorld.index,dfWorld['new_cases'],title='World COVID-19 NewCases',label='NewCases')
    
    title='World COVID-19 Recent ' + strRecent + ' NewCases'
    plotPdColumn(dfWorldNew.index,dfWorldNew['new_cases'],title=title,label='RecentNewCases')
    
    plotPdColumn(dfWorld.index,dfWorld['total_deaths'],title='World COVID-19 Deaths',label='Deaths',color='r')
    plotPdColumn(dfWorld.index,dfWorld['new_deaths'],title='World COVID-19 NewDeaths',label='NewDeaths',color='r')
    
    title='World COVID-19 Recent ' + strRecent + ' NewDeaths'
    plotPdColumn(dfWorldNew.index,dfWorldNew['new_deaths'],title=title,label='RecentNewDeaths',color='r')
    plt.show()
    
'''
def plotWorldStatisticByTime2(csvpath=r'./data/'):
    dfWorld = getWorldDf(csvpath)
    dfWorld.set_index(["Date"], inplace=True)
    
    dfNewCases = [0]
    for i in range(dfWorld.shape[0] -1):
        numberI = dfWorld.iloc[i,1]
        numberINext = dfWorld.iloc[i+1,1]
        newCases = numberINext-numberI
        #print(numberI,numberINext,newCases)
        dfNewCases.append(newCases)
    
    #print(dfWorld.shape,len(dfNewCases))
    dfWorld.insert(2, "newCases", dfNewCases, True) 
    #print(dfWorld.head())   
    #print(dfWorld)
    
    newRecentDays = 30
    dfWorldNew = dfWorld.iloc[-1-newRecentDays:-1, :]
    dfWorld = dfWorld.iloc[::3] # even #dfWorld.iloc[1::2] #odd
    
    plotPdColumn(dfWorld.index,dfWorld['Confirmed'],title='World COVID-19 Confirmed',label='Confirmed')
    plotPdColumn(dfWorldNew.index,dfWorldNew['newCases'],title='World COVID-19 Recent NewCases',label='recentNewCases',color='y')
    plotPdColumn(dfWorld.index,dfWorld['newCases'],title='World COVID-19 NewCases',label='newCases',color='y')
    
def plotWorldStatDeathsByTime(csvpath=r'./'):
    csv = csvpath + 'total-deaths-covid-19.csv'
    df = readCsv(csv)
    df = df[df['Entity'] == 'World' ]
    df = df.rename(columns={"Total confirmed deaths due to COVID-19 (deaths)": "Deaths"})
    #print(df.head())
    
    data = {'Date':df['Date'], 'Deaths': df['Deaths']}
    dfWorld = pd.DataFrame(data=data)
    dfWorld.set_index(["Date"], inplace=True)
    
    dfNewDeaths = [0]
    for i in range(len(dfWorld['Deaths']) -1):
        numberI = dfWorld.iloc[i,0]
        numberINext = dfWorld.iloc[i+1,0]
        newCases = numberINext-numberI
        #print(numberI,numberINext,newCases)
        dfNewDeaths.append(newCases)
        
    #print(len(dfNewCases))
    dfWorld['newDeaths'] = dfNewDeaths
    print(dfWorld.head())
    
    newRecentDays = 30
    dfWorldNew = dfWorld.iloc[-1-newRecentDays:-1, :]
    dfWorld = dfWorld.iloc[::3]
    dfWorld = binaryDf(dfWorld,False) #drop half
    
    plotPdColumn(dfWorld.index,dfWorld['Deaths'],title='World COVID-19 Deaths',label='Deaths',color='r')
    plotPdColumn(dfWorld.index,dfWorld['newDeaths'],title='World COVID-19 NewDeaths',label='NewDeaths',color='r')
    plotPdColumn(dfWorldNew.index,dfWorldNew['newDeaths'],title='World COVID-19 Recent NewDeaths',label='RecentNewDeaths',color='r')

def plotWorldStatConfirmCaseByTime(csvpath=r'./'):
    csv = csvpath + 'total-cases-covid-19.csv'
    df = readCsv(csv)
    df = df[df['Entity'] == 'World' ]
    df = df.rename(columns={"Total confirmed cases of COVID-19 (cases)": "Cases"})
    #print(df.head())
    
    data = {'Date':df['Date'], 'Cases': df['Cases']}
    dfWorld = pd.DataFrame(data=data)
    dfWorld.set_index(["Date"], inplace=True)
    #print(dfWorld.tail())
    #print(dfWorld['Cases'].shape)
    #print(dfWorld['Cases'])
    
    dfNewCases = [0]
    for i in range(len(dfWorld['Cases']) -1):
        numberI = dfWorld.iloc[i,0]
        numberINext = dfWorld.iloc[i+1,0]
        newCases = numberINext-numberI
        #print(numberI,numberINext,newCases)
        dfNewCases.append(newCases)
        
    #print(len(dfNewCases))
    dfWorld['newCases'] = dfNewCases
    #print(dfWorld.head())
    #print(dfWorld.index)
    
    newRecentDays = 30
    dfWorldNew = dfWorld.iloc[-1-newRecentDays:-1, :]
    dfWorld = dfWorld.iloc[::3] # even #dfWorld.iloc[1::2] #odd
    #print(dfWorldNew.shape)
    #print(dfWorld.shape)
    
    dfWorld = binaryDf(dfWorld,False) #drop half
    
    plotPdColumn(dfWorld.index,dfWorld['Cases'],title='World COVID-19 Cases',label='Cases')
    plotPdColumn(dfWorld.index,dfWorld['newCases'],title='World COVID-19 NewCases',label='NewCases')
    plotPdColumn(dfWorldNew.index,dfWorldNew['newCases'],title='World COVID-19 Recent NewCases',label='RecentNewCases')
'''

def getAlldateRecord(csvpath, date='2020-06-16'):
    for i in pathsFiles(csvpath,'csv'):
        #print(i,getDateFromFileName(i))
        dateT = getDateFromFileName(i)
        if dateT == date:
            df = readCsv(i)
            #print(df.head())
            return df
    return None

def getNewCasesDf(pdDate,pdDateBefore):
    locations = pdDate['Location']
    #print('pdDate=', pdDate)
    #print('pdDateBefore=', pdDateBefore)
    #print('locations=', locations)
    pdNewCases = pd.DataFrame()
    for i in locations:
        dataD = pdDate[pdDate['Location'] == i]
        dataB = pdDateBefore[pdDateBefore['Location'] == i]
        #print('dataD=',dataD)
        #print('dataB=',dataB)
        location = i
        newCases = dataD['Confirmed'].values[0] - dataB['Confirmed'].values[0]
        newDeaths = dataD['Deaths'].values[0] - dataB['Deaths'].values[0] 
        #print('\nline=',location,newCases,newDeaths)
        #print(dataD.iloc[:,[1]])
        #print(dataD['Confirmed'].values[0])
        
        data = {'Location': location, 'NewCases': newCases, 'NewDeaths': newDeaths}
        #line = pd.DataFrame(data=[location,newCases,newDeaths], columns=['Location','NewCases','NewDeaths'])
        line = pd.DataFrame(data=data,index=[0])
        pdNewCases = pdNewCases.append(line)
    
    #print(pdNewCases.head())    
    return pdNewCases

def plotNewCasesByCountry(csvpath=r'./data/'):
    daytime = datetime.datetime.now()
    today = datetime.date.today()

    d = today - datetime.timedelta(days=1)
    d = datetime.datetime.strftime(d,'%Y-%m-%d')
    
    date = str(today)#'2020-06-16'
    dateBefore = d   #'2020-06-15'
    print('date,before=',date,dateBefore)

    pdDate = getDateRecord(date,csvpath)
    pdDateBefore = getDateRecord(dateBefore, csvpath)
    if pdDate is None:
        print('Read date record error:',date)
        return
    if pdDateBefore is None:
        print('Read date record error:',dateBefore)
        return
    
    print(pdDate.head())
    print(pdDateBefore.head())
    # print(pdDate.index)
    # print(pdDateBefore.index)
    # print(pdDate.index == pdDateBefore.index )

    pdNewCases = getNewCasesDf(pdDate,pdDateBefore)
    
    pdNewCases.to_csv(gSaveChangeData+'NewCasesAndDeaths_'+date+'.csv',index=False)
    plotNewCasesByCountryData(pdNewCases)
    
def plotNewCasesByCountryData(df,number = 40):    
    df.set_index(["Location"], inplace=True)
    #print('newDf=\n',df.head()) #df.head()
    #print(df.shape)
    
    df = df.drop(index = 'Worldwide')
    
    if number>df.shape[0]:
        number = df.shape[0]
    #df = df.iloc[1:number,:]
    worldDf = df.iloc[:1,:]
    
    dfNewCases = df[df['NewCases']>0]
    dfNewDeaths = df[df['NewDeaths']>0]
    #print('dfNewCases.shape=',dfNewCases.shape)
    #print('dfNewDeaths.shape=',dfNewDeaths.shape)
   
    df = df.sort_values(by=['NewCases'], ascending=False)
    df1 = df.iloc[1:number,[0]]
    
    df = df.sort_values(by=['NewDeaths'], ascending=False)
    df2 = df.iloc[1:number,[1]]
    
    #print('df1=\n',df1)
    #print('df2=\n',df2)
    
    #print(df.head())
    #print(df.dtypes)
    #worldDf = df.loc['Worldwide']
    #print(worldDf)
    now = datetime.datetime.now()
    
    today = str(' Date:') + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    topStr = 'Top '+str(number) + ' '
    
    ncWorld = topStr + 'Today NewCases(World: ' + str(int(worldDf['NewCases'][0])) + ' Countries:'+ str(dfNewCases.shape[0]) + today + ')'
    ndWorld = topStr + 'Today NewDeaths(World: ' + str(int(worldDf['NewDeaths'][0])) + ' Countries:'+ str(dfNewDeaths.shape[0])+ today + ')'
    
    dfs = [('nc', ncWorld, df1),('nd', ndWorld, df2)]  #(name title df)
    #print(ncWorld,ndWorld)
    
    fontsize = 7
    for i,data in enumerate(dfs): 
        dataFrame = data[2]
        if dataFrame.shape[0] == 0:
            continue
        title = data[1]
        name = data[0]
            
        kind='bar'
        if number>25:
            dataFrame = binaryDf(dataFrame)
            kind='barh'
             
        if 1: #deaths mortality
            ax = dataFrame.plot(kind=kind,color='r')
        else:
            ax = dataFrame.plot(kind=kind)

        ax.set_title(title,fontsize=fontsize)
        ax.legend(fontsize=fontsize)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
        plt.setp(ax.get_yticklabels(),fontsize=fontsize)
        
        if number>25:
            plt.subplots_adjust(left=0.30, bottom=None, right=0.98, top=None, wspace=None, hspace=None)
            
        plt.subplots_adjust(left=None, bottom=0.12, right=None, top=None, wspace=None, hspace=None)
        #plt.axis('off')
        # ax1 = plt.axes()
        # x_axis = ax1.axes.get_xaxis()
        # x_axis.set_visible(False)
        plt.xlabel('')
        
        plt.savefig(gSaveBasePath + name+str(i+1)+'.png')
    plt.show()
   
def getDateRecord(date, csvpath=r'./data/'):
    for i in pathsFiles(csvpath,'csv'):
        #print(i,getDateFromFileName(i))
        day = getDateFromFileName(i)
        if day == date:
            df = readCsv(i)
            return df
    return None

def getAlldateRecord(csvpath):
    allInfos = []
    for i in pathsFiles(csvpath,'csv'):
        #print(i,getDateFromFileName(i))
        dateT = getDateFromFileName(i)
        df = readCsv(i)
        allInfos.append([dateT,df])
    return allInfos

def plotCountry(all):
    plotCountryInfo(all) #style1
    plotCountryInfo(all,column='Deaths')
    plotCountryInfo(all,column='NewConfirmed')
    plotCountryInfo(all,column='NewDeaths')

    plotCountryInfo2(all) #style2
    plotCountryInfo2(all,column='Deaths')
    plotCountryInfo2(all,column='NewConfirmed')
    plotCountryInfo2(all,column='NewDeaths')
    
    # plotCountryInfo3(all)
    # plotCountryInfo3(all,column='Deaths')
    # plotCountryInfo3(all,column='NewConfirmed')
    # plotCountryInfo3(all,column='NewDeaths')
    plt.show()

def plotCountriesInfo(csvpath=r'./data/'):
    import threading
    all = getAlldateRecord(csvpath)
    if 0:
        saveCountriesInfo(all)
        plotCountry(all)
    else:
        t = threading.Thread(target=saveCountriesInfo, name='Save country covid-19 data file', args=(all, ))
        #t.setDaemon(True)
        t.start()
        plotCountry(all)
        t.join()
    
def getCountryNewCasesAndDeathsDf(pdDate):
    pdDate['NewConfirmed'] = 0
    pdDate['NewDeaths'] = 0
    #print(pdDate.head(5))    
    for i in range(pdDate.shape[0]-1):
        newConfirmed = pdDate['Confirmed'].iloc[i+1] - pdDate['Confirmed'].iloc[i]
        if newConfirmed<0:
            newConfirmed=0
        pdDate.iloc[i+1, pdDate.columns.get_loc("NewConfirmed")] = newConfirmed
        
        newDeaths = pdDate['Deaths'].iloc[i+1] - pdDate['Deaths'].iloc[i]
        if newDeaths<0:
            newDeaths=0
        pdDate.iloc[i+1, pdDate.columns.get_loc("NewDeaths")] = newDeaths
        
        #pdDate['NewConfirmed'].iloc[i+1] = pdDate['Confirmed'].iloc[i+1] - pdDate['Confirmed'].iloc[i]
        #pdDate['NewDeaths'].iloc[i+1] = pdDate['Deaths'].iloc[i+1] - pdDate['Deaths'].iloc[i]

    #print(pdDate.head(5))    
    return pdDate
    
def saveCountriesInfo(all):
    countries = all[-1][1]['Location']
    bar = SimpleProgressBar(total=len(countries),title='Save Country Files',width=30)
    for k,i in enumerate(countries):
        df = getCountryDayData(i,all)
        #print(df.head(5))
        df = getCountryNewCasesAndDeathsDf(df)
        df.to_csv(gSaveCountryData+i+'.csv',index=True)
        bar.update(k+1)
    
def plotCountryInfo(all,column='Confirmed'):
    days = 30
    countriesNumbers = 15
    
    #countries=['United States','Spain','Italy']
    countries = all[-1][1]['Location'][1:countriesNumbers]
    #print(countries)
    
    plt.figure(figsize=(8,5))
    ax = plt.subplot(1,1,1)
   
    for i in countries:
        df = getCountryDayData(i,all)
        df = getCountryNewCasesAndDeathsDf(df)
        #print(df.head(5))
        #df = binaryDf(df,labelAdd=False)
        df = df.iloc[-1*days:,:] #recent 30 days
        title = column + ' Cases, Top ' + str(countriesNumbers) + ' countries, ' + 'Recent ' + str(days) + ' days'
        plotCountryAx(ax,df['Date'],df[column],label=i,title=title)
        
    if column != 'NewConfirmed' and column != 'NewDeaths':
        ax.set_yscale('log')
        
    #plt.xlim('2020-05-01', '2020-06-20') 
    plt.savefig(gSaveBasePath + 'countries_' + column + '.png')
    #plt.show()
    
def plotCountryInfo2(all,column='Confirmed'):
    countriesNumbers = 8
    days = 30
    countries = all[-1][1]['Location'][1:countriesNumbers]
    #print(countries)
    
    plt.figure(figsize=(8,5))
    ax = plt.subplot(1,1,1)
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False) 
    
    for k,i in enumerate(countries):
        df = getCountryDayData(i,all)
        df = getCountryNewCasesAndDeathsDf(df)
        
        #df = binaryDf(df,labelAdd=False)
        df = df.iloc[-1*days:,:] #recent 30 days
        color = cm.jet(float(k) / countriesNumbers)
        #print('color=',color)
        title = column + ' Cases, Top ' + str(countriesNumbers) + ' countries, ' + 'Recent ' + str(days) + ' days'
        plotCountryAx(ax,df['Date'],df[column],label=i,title=title,color=color)
        
        #ax.text(df['Date'][-1], df[column][-1], i)
        #print(df.head(5))
        #print(df[column])
        ax.text(df['Date'].iloc[-1], df[column].iloc[-1], i,color=color)
        #break
        
    bottom, top = plt.ylim()
    #print('bottom, top =',bottom, top)
    inter = 10000
    if column=='Confirmed':
        inter = 1000000
    for y in range(int(bottom), int(top), inter):    
        plt.plot(df['Date'], [y] * len(df['Date']), "--", lw=0.5, color="black", alpha=0.3) 
          
    #plt.xlim('2020-05-01', '2020-06-20') 
    #plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")  
    #ax.set_yscale('log')
    plt.tight_layout()
    plt.savefig(gSaveBasePath + 'countries0_' + column + '.png')
    #plt.show()
    
def plotCountryInfo3(all,column='Confirmed'):
    countriesNumbers = 8
    countries = all[-1][1]['Location'][1:countriesNumbers]
    #print(countries)
    
    plt.figure(figsize=(8,5))
    ax = plt.subplot(1,1,1)
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False) 
    
    for k,i in enumerate(countries):
        df = getCountryDayData(i,all)
        df = getCountryNewCasesAndDeathsDf(df)
        #df = binaryDf(df,labelAdd=False)
        color = cm.jet(float(k) / countriesNumbers)
        
        title = column + ' Cases, Top ' + str(countriesNumbers) + ' countries'
        
        plotCountryAxBar(ax,df['Date'],df[column],label=i,title=title,color=color)
        #ax.text(df['Date'].iloc[-1], df[column].iloc[-1], i,color=color)
        
    bottom, top = plt.ylim()
    #print('bottom, top =',bottom, top)
    inter = 10000
    if column=='Confirmed':
        inter = 1000000
    for y in range(int(bottom), int(top), inter):    
        plt.plot(df['Date'], [y] * len(df['Date']), "--", lw=0.5, color="black", alpha=0.3) 
          
    #plt.xlim('2020-05-01', '2020-06-20') 
    #plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")  
    #ax.set_yscale('log')
    plt.tight_layout()
    plt.savefig(gSaveBasePath + 'countries1_' + column + '.png')
    plt.show()
    
def plotCountryAx(ax,x,y,label,title,color=None):
    fontsize = 7
    ax.plot(x,y,label=label,c=color)
    ax.set_title(title,fontsize=fontsize)
    ax.legend(fontsize=fontsize,loc='upper left')
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
    plt.setp(ax.get_yticklabels(),fontsize=fontsize)
    #plt.show()
    
def plotCountryAxBar(ax,x,y,label,title,color=None):
    fontsize = 7
    ax.bar(x,y,label=label,color=color)
    ax.set_title(title,fontsize=fontsize)
    ax.legend(fontsize=fontsize,loc='upper left')
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
    plt.setp(ax.get_yticklabels(),fontsize=fontsize)
    #plt.show()
    
# def plotCountry(ax,x,y,label):
#     plt.plot(x,y,label=label)
#     plt.yscale("log")
#     plt.legend()
#     plt.show()    
    
def getCountryDayData(country,allList):
    pdCountry = pd.DataFrame()
    for i in allList:
        date = i[0]
        df = i[1]
        
        countryLine = df[df['Location'] == country]
        #countryLine['Date'] = date
        try:
            countryLine.insert(1, "Date", [date], True) 
            #print('countryLine=',countryLine)
            pdCountry = pdCountry.append(pd.DataFrame(data=countryLine))
        except:
            #print('date,country=',date,country)
            #print('countryLine=',countryLine)
            pass
        
    pdCountry.set_index(["Location"], inplace=True)   
    #print(pdCountry)    
    return pdCountry
    
if __name__ == '__main__':
    csvpath=r'./data/'
    # df = readCsv(csvpath+'coronavirous_2020-10-28_213546.csv')
    # df = df[1:]
    # df.set_index(["Location"], inplace=True)
    # plotData(df, number=60)
    
    #readCsv(csvpath+'coronavirous_2020-07-02_110250.csv')
    #plotChangeBydata(csvpath)
    #plotWorldStatConfirmCaseByTime()
    #plotWorldStatisticByTime()
    plotNewCasesByCountry(csvpath)
    #plotCountriesInfo(csvpath)
    