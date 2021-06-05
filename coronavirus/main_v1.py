#python3 unicode
#author:Steven Huang 27/03/20
#function: Query cases of COVID-19 from website

"""""""""""""""""""""""""""""""""""""""""""""""""""""
#usgae:
#python main.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""
import sys
import os
sys.path.append("..")
import datetime
import pandas as pd
from lxml import etree
from common.getHtml import openUrl, openUrlUrlLib
import matplotlib.pyplot as plt

from  plotCoronavirous import plotData
from jsonUpdate import updateJson

mainUrl = "https://google.com/covid19-map/"

def writeToCsv(df):
    base=r'./data/'
    daytime = datetime.datetime.now()
    today = datetime.date.today()
    t = str(today) + '_' + str(daytime.__format__('%H%M%S'))
    
    #file='coronavirous.csv'
    file = os.path.join(base, 'coronavirous_' + t + '.csv')
    df.to_csv(file,index=True)
          
def preprocessData(df):
    #print(df)
    print('\n\nBefore preprocess:\n',df.head())
    #print(df.isnull())
    #print(df.isnull().any(axis=1))
    #null_columns=df.columns[df.isnull().any()]
    #print(df[df.isnull().any(axis=1)][null_columns])

    df[df.columns[1:]] = df[df.columns[1:]].apply(lambda x: x.str.replace(',',''))
    #print('before preprocess:\n\n',df.head())
    
    df['Confirmed'] = pd.to_numeric(df['Confirmed'])
    df['Confirmed'] = df['Confirmed'].astype('int64')

    df['Case_Per_1M_people'] = pd.to_numeric(df['Case_Per_1M_people'])
    #df['Case_Per_1M_people'] = df['Case_Per_1M_people'].astype(float)

    df['NewCases'] = pd.to_numeric(df['NewCases'])
    df['NewCases'] = df['NewCases'].astype('int64')

    #df['Recovered'] = pd.to_numeric(df['Recovered'])
    #df['Recovered'] = df['Recovered'].astype('int64')

    df['Deaths'] = pd.to_numeric(df['Deaths'])
    df['Deaths'] = df['Deaths'].astype('int64')
    
    '''Add coloumn mortality rate: df['Deaths'] / df['Confirmed'].
    But please note that this is not necessarily the correct definition.
    '''
    Mortality = (df['Deaths']/df['Confirmed']).round(4)
    #print(type(Mortality))
    #print(Mortality)
    dfMortality = pd.DataFrame(Mortality, columns=['Mortality'])

    df = pd.concat([df, dfMortality], axis=1)
    df.set_index(["Location"], inplace=True)

    print('\n\nAfter preprocess:\n',df.head())
    writeToCsv(df)
    updateJson()
    return df

def parseXpathTr(tr, columns):
    html = etree.HTML(etree.tostring(tr))
    #print(len(result),result)
    location,confirmed,Case_Per_1M_people,recovered,deaths = '','','','',''
    # span = html.xpath('//span')    
    path='//th//div' #'//div[@class="pcAJd"]' #'//th[@class="l3HOY"]//div[@class="pcAJd"]' #
    div = html.xpath(path)  
    #print('div=',len(div))
    location=''
    if len(div)==2:
        location = div[1].text
    
    result = html.xpath('//td') 
    for i,td in enumerate(result):
        if i == 0:
            confirmed = td.text.strip()
        elif i == 1:
            pass
        elif i == 2:
            Case_Per_1M_people = td.text.strip() 
        elif i == 3:
            recovered = td.text.strip()
        elif i == 4:
            deaths = td.text.strip()

    if Case_Per_1M_people == '' or Case_Per_1M_people == '—':
        Case_Per_1M_people = '0'
    if recovered == '' or recovered == '—':
        recovered = '0'
    if deaths == '' or deaths == '—':
        deaths = '0'
    if confirmed == '' or confirmed == '—':
        confirmed = '0'

    print('Location:',location,'Confirmed:',confirmed,'Case_Per_1M_people:',Case_Per_1M_people,'Recovered:',recovered,'deaths:',deaths)
    #columns=['Location', 'Confirmed', 'Cases per 1M people', 'Recovered', 'Deaths']
    dfLine = pd.DataFrame([[location, confirmed, Case_Per_1M_people, recovered, deaths]], columns=columns)
    return dfLine

def getHeader(thead):
    html = etree.HTML(etree.tostring(thead))
    #res = html.xpath('//th//div[@id="c1"]')
    #res = html.xpath('//div[@class="DdCLrb"]')
    res = html.xpath('//tr[@class="sgXwHf"]//div[@class="XmCM0b"]')
    print(len(res))
    
    columns = [th.text for th in res]
    return columns

def parseHtml(htmlContent):
    html = etree.HTML(htmlContent)
    #X = '//*[@id="main"]/div[2]/div/div/div/div/div[1]/table'
    #X = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div/div[2]/div[2]/c-wiz/div/div[2]/div/div[1]/table/tbody/tr'
    #X = '/html/body/c-wiz/div/div/div/div/div[2]/div[2]/c-wiz/div/div[2]/div/div[1]/table/tbody/tr'
    X = '//table[@class="pH8O4c"]/thead'
    #X = '//table'
    resHead = html.xpath(X)
    print('type(html)=',type(html))
    #print(len(resHead))    
    columns = getHeader(resHead[0])
    print('columns = ', columns)
    columns[3]='Case_Per_1M_people'
    columns.pop(2) #remove 'New cases (last 60 days)'
    print('columns = ', columns)
    
    X = '//table[@class="pH8O4c"]//tbody/tr' #[@class="SAGQRD"]'
    result = html.xpath(X)
    print(len(result))
    df  = pd. DataFrame()
    for i in result:
        df = df.append(parseXpathTr(i, columns),ignore_index=True)
    print('df.shape=', df.shape)
    
    df = preprocessData(df)
    plotData(df)

def Load(url):
    print("Open:",url)
    #html = openUrl(url)
    html = openUrlUrlLib(url)
    return parseHtml(html)
    
if __name__ == '__main__':
    Load(mainUrl)