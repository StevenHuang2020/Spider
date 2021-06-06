#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#Description: Probability of antibodies after vaccination
#Please note: For entertainment only, not scientific
#Date: 2021/06/05
#Author: Steven Huang, Auckland, NZ
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.rcParams['figure.dpi'] = 150 #high resolution 100~300

def probablityVaccine(p, N): #1-(1-p)^N
    """
    p: Vaccine effectiveness
    N: Number of courses of vaccine
    """
    return np.round(1-np.power(1-p, N), 6)

def plotVaccins(data):
    ax = plt.subplot(1,1,1)
    plt.title('Success probability after numbers of vaccination')
    
    markers=['o', 'v', '*', 's', '^']
    for i, d in enumerate(data):
        name,prob = d
        x = np.arange(len(prob))+1
        y = prob
        ax.plot(x,y,label=name, linestyle='-.', marker=markers[i])
    
    plt.text(2.5, 0.3, r'$Prob = 1-(1-p)^N$', fontsize=12)

    ax.set_xlabel('Times')
    ax.set_ylabel('Probablity')
    ax.legend()
    #plt.legend()
    plt.grid(linestyle='-.', alpha=0.5) #'-', '--', '-.', ':', '',
    #plt.legend(loc='lower left')
    plt.savefig(r'.\images\probVaccine.png')
    plt.show()
    pass
    
def plotVaccinsTable(data):
    columns = ['name', '1', '2', '3', '4', '5', '6']
    df  = pd. DataFrame()
    for name,prob in data:
        dfLine = pd.DataFrame([[name, prob[0], prob[1],prob[2],prob[3],prob[4],prob[5]]], columns=columns)
        df = df.append(dfLine)
    print(df)
    
    title = 'Success probability after numbers of vaccination'
    #plt.title(title)
    plt.text(0.16, 0.7, title, fontsize=12)
    tb = plt.table(cellText=df.values, colLabels=df.columns, loc='center',cellLoc='center')
    tb.auto_set_font_size(False)
    tb.set_fontsize(10)
    #colList = list(range(len(df.columns)))
    colList = [1,2,3,4,5,6]
    tb.auto_set_column_width(col=colList)
       
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(r'.\images\probVaccineT.png')
    plt.show()
    
def generateData():
    pl = [0.2, 0.5, 0.6, 0.8, 0.9]
    N = np.arange(1, 7)
    
    data = []
    for p in pl:
        prob = probablityVaccine(p, N)
        #print(prob)
        data.append(('vaccine-'+str(p), prob))
    print(data)
    return data 

def main():
    data = generateData()
    plotVaccins(data)
    plotVaccinsTable(data)
    
if __name__=="__main__":
    main()
