#python3 unicode
#author:Steven Huang 07/25/20
#function: Query NZ COVID-19 from https://www.health.govt.nz/
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#usgae:
#python .\mainNZ.py
#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys
import os
sys.path.append("..")
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common.getHtml import openUrl,openUrlUrlLib,downWebFile
from lxml import etree

from plotCoronavirous import gSaveBasePath,readCsv

#plt.rcParams['figure.dpi'] = 120 #high resolution

#reference: https://www.health.govt.nz/our-work/diseases-and-conditions/covid-getDataFileFromWeb19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases
#https://www.health.govt.nz/system/files/documents/pages/covid-cases-24july20.xlsx

mainUrl='https://www.health.govt.nz/'
url=mainUrl + 'our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-data-and-statistics/covid-19-case-demographics'

def getDataFileFromWeb(url=url):
    html = openUrl(url) #openUrlUrlLib(url)
    #print(html)
    html = etree.HTML(html)
    #X = '//*[@id="node-10866"]/div/div/div/ul[2]/li[1]/a'
    #X = '//*[@id="node-10866"]/div[2]/div/div/p[13]/a'
    X = '//*[@id="case-details-csv-file"]'
    #X = '//table'
    res = html.xpath(X)
    #print(len(res), res)
    if len(res) > 0:
        print(res[0].get('href'))
        return mainUrl+res[0].get('href')
    return None

def readExcel(file,sheetname=0,header=2,verbose=False):
    df = pd.read_excel(file,sheet_name=sheetname,header=header)
    print(type(df),'df.shape=',df.shape)
    
    if verbose:
        print(df.describe().transpose())
        print(df.head())
        #df.set_index(["Location"], inplace=True)
        print('df.columns=',df.columns)
        print('df.dtypes = ',df.dtypes)
        #df = df.apply(pd.to_numeric, axis=0)
        #print('df.dtypes = ',df.dtypes)
    return df

# def readCSV(file,sheetname=0,header=0,verbose=False):
#     df = pd.read_csv(file,header=header)
#     #print(type(df),'df.shape=',df.shape)
#     if verbose:
#         print(df.describe().transpose())
#         print(df.head())
#         #df.set_index(["Location"], inplace=True)
#         print('df.columns=',df.columns)
#         print('df.dtypes = ',df.dtypes)
#         #df = df.apply(pd.to_numeric, axis=0)
#         #print('df.dtypes = ',df.dtypes)
#     return df

def plotStatistcs(df,title,label):
    fontsize = 7
    kind='bar'
    # if df.shape[0]>25:
    #     kind='barh'
    ax = df.plot(kind=kind,legend=False) #color='gray'
    
    x_offset = -0.06
    y_offset = 2.0
    for p in ax.patches:
        b = p.get_bbox()
        val = "{}".format(int(b.y1 + b.y0))        
        ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=fontsize)
    
    ax.set_title(title,fontsize=fontsize)
    #ax.legend(fontsize=fontsize)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
    plt.setp(ax.get_yticklabels(),rotation=30, fontsize=fontsize)
    plt.xlabel('')
    plt.ylabel('')
    plt.subplots_adjust(left=0.2, bottom=0.22, right=0.98, top=0.94, wspace=None, hspace=None) 
    plt.savefig(gSaveBasePath + 'NZ_'+label+'.png')
    #plt.show()
        
locationColumns = 'Last location before return' #'Last country before return'
def parseConfirmed(df):
    print('Confirmed dataset:\n',df.head())
    Sex = list(set(df['Sex']))
    AgeGroup = list(set(df['Age group']))
    AgeGroup.sort()
    #AgeGroup = [ '<1', '1 to 4', '5 to 9', '10 to 14', '15 to 19', '20 to 29', '30 to 39', '40 to 49', '50 to 59', '60 to 69', '70+']
    
    DHB = list(set(df['DHB']))
    bOverseas = list(set(df['Overseas travel']))
    
    if ' ' in bOverseas:
        bOverseas.remove(' ')
    #LastTravelCountry = list(set(df[locationColumns]))
    #LastTravelCountry.remove(np.nan)
    
    print('Sex=',Sex)
    print('AgeGroup=',AgeGroup)
    print('DHB=',DHB)
    print('bOverseas=',bOverseas)
    #print('LastTravelCountry=',LastTravelCountry)
    
    columns=['Gender','Number']
    dfSex  = pd.DataFrame()
    for i in Sex:
        line = pd.DataFrame([[i, df[df['Sex']==i].shape[0]]],columns=columns)
        dfSex = dfSex.append(line, ignore_index=True) 
    dfSex.set_index(["Gender"], inplace=True)
   
    columns=['Group','Number']
    dfAgeGroup  = pd.DataFrame()
    for i in AgeGroup:
        line = pd.DataFrame([[i, df[df['Age group']==i].shape[0]]],columns=columns)
        dfAgeGroup = dfAgeGroup.append(line, ignore_index=True) 
    dfAgeGroup.set_index(["Group"], inplace=True)
    
    columns=['DHB','Number']
    dfDHB  = pd.DataFrame()
    for i in DHB:
        line = pd.DataFrame([[i, df[df['DHB']==i].shape[0]]],columns=columns)
        dfDHB = dfDHB.append(line, ignore_index=True) 
    #print(dfDHB)
    dfDHB.set_index(["DHB"], inplace=True)
    
    columns=['Overseas','Number']
    dfbOverseas  = pd.DataFrame()
    for i in bOverseas:
        line = pd.DataFrame([[i, df[df['Overseas travel']==i].shape[0]]],columns=columns)
        dfbOverseas = dfbOverseas.append(line, ignore_index=True) 
    dfbOverseas.set_index(["Overseas"], inplace=True)
    
    # columns=['RecturnCountry','Number']
    # dfLastTravelCountry  = pd.DataFrame()
    # for i in LastTravelCountry:
    #     line = pd.DataFrame([[i, df[df[locationColumns]==i].shape[0]]],columns=columns)
    #     dfLastTravelCountry = dfLastTravelCountry.append(line, ignore_index=True) 
    # dfLastTravelCountry.set_index(["RecturnCountry"], inplace=True)
    
    #dfSex = dfSex.sort_values(by = 0, axis=1) #dfSex.sort_values(by=['Female'],ascending=False)
    # dfAgeGroup = dfAgeGroup.sort_values(by=['Case_Per_1M_people'],ascending=False)
    dfDHB = dfDHB.sort_values(by=['Number'],ascending=False)
    # dfbOverseas = dfbOverseas.sort_values(by=['Case_Per_1M_people'],ascending=False)
    #dfLastTravelCountry = dfLastTravelCountry.sort_values(by=['Number'],ascending=False)
    
    # print(dfSex)
    # print(dfAgeGroup)
    # print(dfDHB)
    # print(dfbOverseas)
    # print(dfLastTravelCountry)
    
    now = datetime.datetime.now()
    today = str(' Date:') + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    label='Gender'
    plotStatistcs(dfSex,label=label,title=label + ' ' + today)
    label='AgeGroup'
    plotStatistcs(dfAgeGroup,label=label,title=label + ' ' + today)
    label='DHB'
    plotStatistcs(dfDHB,label=label,title=label + ' ' + today)
    label='IsOVerseas'
    plotStatistcs(dfbOverseas,label=label,title=label + ' ' + today)
    #label='LastTravelCountry'
    #plotStatistcs(dfLastTravelCountry,label=label,title=label + ' ' + today)
    plt.show()
    
def plotTotal(df,title,label,showNumberOnBar=False):
    fontsize = 8 
    plt.figure()
    ax = df.plot(kind='bar',legend=False) 
    
    if showNumberOnBar:
        x_offset = -0.3
        y_offset = 0.1
        for p in ax.patches:
            b = p.get_bbox()
            val = "{}".format(int(b.y1 + b.y0))        
            ax.annotate(val, ((b.x0 + b.x1)/2 + x_offset, b.y1 + y_offset), fontsize=fontsize)
        
    ax.set_title(title,fontsize=fontsize)
    #ax.legend(fontsize=fontsize)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
    plt.setp(ax.get_yticklabels(),rotation=30, fontsize=fontsize)
    plt.xlabel('')
    plt.ylabel('')
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None) 
    plt.savefig(gSaveBasePath + label + '.png')
    #plt.show()

def plotNZDataChange(df):
    def getDataRecordNum(df,date):
        records = df[df['Report Date'] == date]
        return records.shape[0]
    
    def totalDays(start,stop):
        delta = stop-start
        #print(delta.days) #type(days)
        return delta.days
    
    DATEFORMAT=r'%Y-%m-%d' #r'%d/%m/%Y'
    #print(df.head())
    #pd.to_datetime(df['Report Date'])
    
    dfDate = df['Report Date']
    dfDate= pd.to_datetime(dfDate)#format=DATEFORMAT
    #print('dtypes=', dfDate.dtypes)
    #print(dfDate.shape)
    
    dfDate = list(set(dfDate))
    dfDate.sort()
    #print('dfDate=', len(dfDate),dfDate)
    
    startDate = dfDate[0]
    stopDate = dfDate[-1]
    days = totalDays(startDate,stopDate)
    #print('startDate,stopDate=',startDate,stopDate,days)

    columns=['Date','Number','Cumlative']
    dfStat  = pd.DataFrame()
    s = 0
    for i in range(days+1):
        d = startDate + datetime.timedelta(days=i)
        d = datetime.datetime.strftime(d, DATEFORMAT)
        number = getDataRecordNum(df,d)
        #print(d,number)
        s += number
        line = pd.DataFrame([[d, number, s]],columns=columns)
        dfStat = dfStat.append(line, ignore_index=True)
        
    now = datetime.datetime.now()
    today = str(' Date:') + str(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    dfStat.set_index(["Date"], inplace=True)
    #print('dfStat=', dfStat)

    label='NZ_COVID-19_EveryDayCases'
    plotTotal(dfStat['Number'], label=label, title=label + ' ' + today)
    
    label='NZ_COVID-19_CumlativeCases'
    plotTotal(dfStat['Cumlative'], label=label, title=label + ' ' + today)
    #print(dfStat['Number'][-30:])
    
    recentDays=40
    label='NZ_COVID-19_RecentCases'
    title=label + ' ' + str(recentDays) + ' days, ' + today
    plotTotal(dfStat['Number'][-1*recentDays:], label=label, title=title, showNumberOnBar=True)
    plt.show()
    
def getNZCovid19():
    #file=r'.\NZ\covid-cases-24july20.xlsx'
    fileUrl = getDataFileFromWeb()
    if fileUrl is None:
        print(r"Can't find the file, something wrong!")
        return None
    
    name = fileUrl[fileUrl.rfind('/')+1:]
    print(fileUrl,'name=',name)
    file = os.path.join(r'./NZ/', name)
    res = downWebFile(fileUrl, file)
    if not res:
        print(r"Download file failed, please check the real url!")
        return None
    
    #excel = r'./NZ'+'/'+name
    #dfConfirmed = readExcel(excel,'Confirmed') #'Probable'
    return readCsv(file)
    
def plotStatistic(df):
    if df is not None:
        parseConfirmed(df)
        plotNZDataChange(df)
        
def main():
    df = getNZCovid19()
    plotStatistic(df)
    
if __name__ == '__main__':
    main()
    