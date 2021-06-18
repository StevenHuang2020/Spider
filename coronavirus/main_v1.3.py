#python3 unicode
#author:Steven Huang 31/03/20
#function: Query cases of COVID-19 from website using selenium
"""""""""""""""""""""""""""""""""""""""""""""""""""""
#usgae:
#python .\main_v1.3.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""
import datetime
import os
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import argparse 
from main_v1 import preprocessData

#from predictStatistics import predict
from common.getHtml import downWebFile
from plotCoronavirous import plotDataGoogle,plotCountriesFromOurWorld
from commonPath import createPath
from plotCoronavirous import plotWorldStatisticByTime, getVaccinesFile
from plotVaccinations import gCovidCsv,downloadOurWorldData

mainUrl = 'https://google.com/covid19-map/'

def parseXpathTr(tr,columns):
    location,confirmed,NewCases,Case_Per_1M_people,deaths = '','','','',''
    
    #path='//th[@class="l3HOY"]/div/div[@class="pcAJd"]'
    #path='//th/div[@class="pcAJd"]'
    #path='//th//div'
    #div = tr.find_elements_by_xpath(path)
    #div = tr.find_elements(By.TAG_NAME,'div')
    div = tr.find_elements(By.CLASS_NAME,'pcAJd')
    #print('len=',len(div))
    if len(div)>0:
        location = div[0].text #third div store the location
    
    tds = tr.find_elements(By.TAG_NAME, "td")
    #print(len(tds))
    for i,td in enumerate(tds):
        if i == 0:
            confirmed = td.text.strip()
        elif i == 1:
            NewCases = td.text.strip()
        elif i == 2:
            pass
        elif i == 3:
            Case_Per_1M_people = td.text.strip()
        elif i == 4:
            deaths = td.text.strip()

    if Case_Per_1M_people == '' or Case_Per_1M_people == 'No data':
        Case_Per_1M_people = '0'
    if deaths == '' or deaths == 'No data':
        deaths = '0'
    if confirmed == '' or confirmed == 'No data':
        confirmed = '0'
    if NewCases == '' or NewCases == 'No data':
        NewCases = '0'
        
    #print('Location:',location,'Confirmed:',confirmed,'NewCases:',NewCases,'Case_Per_1M_people:',Case_Per_1M_people,'deaths:',deaths)
    return pd.DataFrame([[location, confirmed, NewCases, Case_Per_1M_people, deaths]], columns=columns)

def getHeader(thead):
    ths = thead.find_elements_by_xpath('//tr[@class="sgXwHf"]//div[@class="XmCM0b"]')
    print('len=',len(ths))
    columns = [th.text for th in ths]
    return columns

def clickBtn(driver,btnXpath):
    btn = driver.find_element_by_xpath(btnXpath)
    if btn:
        btn.click()

def scroll_down_element(driver, element):
    try:
        action = ActionChains(driver)
        action.move_to_element(element).perform()
        #element.click() 
    except Exception as e:
        print('error scrolling down web element', e)
        
def Load(url):
    print("Open:",url)
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(2)
    
    #btn_More='//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div[4]/div'
    #clickBtn(driver,btn_More)
    
    #X = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div/div[2]/div[2]/c-wiz/div/div[2]/div/div[1]/table'
    X = '//table[@class="pH8O4c"]'
    table_id = driver.find_element_by_xpath(X)
    
    scroll_down_element(driver,table_id) #do an table action to get all table lines
    sleep(2)
    
    thead = table_id.find_element_by_tag_name('thead')
    tbody = table_id.find_element_by_tag_name('tbody')
    
    originalColumns = getHeader(thead)
    print('Original Columns: ', originalColumns)
    columns = []
    columns.append('Location')
    columns.append('Confirmed')
    columns.append('NewCases')
    columns.append('Case_Per_1M_people')
    columns.append('Deaths')
    print('Columns: ', columns)
    
    df = pd.DataFrame()
    result = tbody.find_elements(By.TAG_NAME, "tr")
    print('result=',len(result))
    for i in result:
        df = df.append(parseXpathTr(i, columns), ignore_index=True)
  
    print('df.shape=', df.shape)
    return preprocessData(df)
            
def argCmdParse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--noplot', action="store_true", help = 'only download data, not plot it')
    return parser.parse_args()

if __name__ == '__main__':
    arg = argCmdParse()
    plot = True
    if arg.noplot:
        plot = False
    print('plot=',plot)
    
    downloadOurWorldData()
    
    #df = Load(mainUrl) #from google data
    # if plot:
    #     plotDataGoogle(df,60)

    plotCountriesFromOurWorld()