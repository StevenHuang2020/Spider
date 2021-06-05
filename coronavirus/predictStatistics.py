#python3 steven 
#LSTM regression, solve data set with time change
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import os 

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #not print tf debug info
plt.rcParams['savefig.dpi'] = 300 #matplot figure quality when save

from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,BatchNormalization,TimeDistributed,Dropout
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score

from plotCoronavirous import binaryDf,pathsFiles
from jsonUpdate import getDataTime

gScaler = MinMaxScaler() #StandardScaler() #

gSaveBasePath = r'.\images\\'
gSavePredict = r'.\dataPredict\\'

def plotDataSet(data):
    plt.plot(data)
    plt.show()
    
def preprocessDb(dataset):
    dataset = gScaler.fit_transform(dataset)
    #print('dataset=',dataset[:5])
    return dataset

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataset = dataset.flatten()
    #print(dataset.shape)
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)
    
def getDataSet(file=r'.\OurWrold\owid-covid-data.csv'):
    dataset = pd.read_csv(file)
    #dataset = pd.read_csv(file,sep=',', encoding='utf-8')
    dataset = dataset[dataset['location'] == 'World' ]
    #dataset = dataset.rename(columns={"Total confirmed cases of COVID-19 (cases)": "Cases"})
    print(dataset.head())
    dataset = dataset.loc[:, ['date','total_cases']]
    dataset = dataset.rename(columns={'date':'Date', "total_cases": "Cases"})
    #dataset = dataset['Date', 'Cases']
        
    dataset = dataset.dropna()
    
    #print(dataset.describe().T)
    print(dataset.head())
    print(dataset.tail())
    print(dataset.shape)
    print(dataset.dtypes)
    return dataset

def plotData(ax,x,y,label=''):
    fontsize = 5
    ax.plot(x,y,label=label)
    #ax.set_aspect(1)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize,fontweight=10)
    plt.setp(ax.get_yticklabels(), fontsize=fontsize)
    plt.subplots_adjust(left=0.02, bottom=0.09, right=0.99, top=0.92, wspace=None, hspace=None)

def predictFuture(model,start,Number=5):
    print('---------------future')
    print(start)    
    #print(start.shape,'startval:', gScaler.inverse_transform(start.reshape(1,-1)))
    start = np.array([start]).reshape(1,1,1)
    result = []
    result.append(start.flatten()[0])
    for i in range(Number):
        next = model.predict(start)
        #print(next)
        result.append(next.flatten()[0])
        start = next
    print('predict value=',result)
    result = gScaler.inverse_transform(np.array(result).reshape(1,-1)).flatten()
    result = list(map(int, result))
    print('after inverse redict value=',result)
    return result

def plotPredictCompare(model,trainX,index,data):
    trainPredict = model.predict(trainX).flatten()
    trainPredict = gScaler.inverse_transform(trainPredict.reshape((trainPredict.shape[0],1))).flatten()
    
    data = data.flatten()
    #print(index.shape)
    #print(trainPredict.shape)    
    #print(data.shape)
    #print('raw=',data)
    #print('pred=',trainPredict)

    offset=70 #120
    plt.figure(figsize=(12,10))
    ax = plt.subplot(1,1,1)
    plt.title('PredictTime: ' + getDataTime())
    plotData(ax,index[offset+2:-1],data[offset+2:-1],'True Data')
    plotData(ax,index[offset+2:-1],trainPredict[offset+1:-1],'Prediction')
    plt.savefig(gSaveBasePath + 'WorldPredictCompare.png')
    plt.show()
 
def changeNewIndexFmt(newIndex):
    new = []
    for i in newIndex:
        i=datetime.datetime.strptime(i,'%m/%d/%Y')
        i = datetime.datetime.strftime(i,'%Y-%m-%d') #'%b %d, %Y'
        new.append(i)
    return new

def plotPredictFuture(model,trainY,index,data):
    Number = 10 #predict future Number days
    pred = predictFuture(model,trainY[-1],Number)
    print('predict start date:',index[-1])

    startIndex = index[-1]
    #sD=datetime.datetime.strptime(startIndex,'%b %d, %Y')
    sD=datetime.datetime.strptime(startIndex,'%m/%d/%y') #'%Y-%m-%d'
    
    newIndex=[]
    startIndex = datetime.datetime.strftime(sD,'%m/%d/%Y')
    newIndex.append(startIndex)
    for i in range(Number):
        d = sD + datetime.timedelta(days=i+1)
        d = datetime.datetime.strftime(d,'%m/%d/%Y')
        #print(d)
        newIndex.append(d)
    print('predict period:',newIndex)
    
    df = pd.DataFrame({'Date':newIndex,'Predicted cases':pred})
    
    #add predict day newCases
    df['Predicted day newCases'] = 0
    for i in range(1, df.shape[0]):
        df.iloc[i, 2] =  df.iloc[i,1] - df.iloc[i-1,1]
        
    print('table:',df)
    
    startIndex = datetime.datetime.strptime(startIndex, '%m/%d/%Y')
    predictTime=datetime.datetime.strftime(startIndex,'%Y-%m-%d')
    df.to_csv(gSavePredict+predictTime+'_predict.csv',index=True)
    
    offset=150#70 #120
    #plt.figure(figsize=(8,6))
    plt.title('Future ' + str(Number) + ' days Covid-19,' + ' Prediction time: '+ getDataTime())
       
    ax = plt.gca()
    #ax = plt.subplot(1,1,1)
    plotData(ax,index[offset:],data[offset:],'Now cases')
    
    newIndex = changeNewIndexFmt(newIndex)
    plotData(ax,newIndex,pred,'Predicted cases')
    #print('oldIndex=',index[offset:])
    #print('newIndex=',newIndex)
    
    #ax.table(cellText=df.values, colLabels=df.columns, loc='center') #,clip_box=[[0,5],[0+100,5+100]]
    tb = plt.table(cellText=df.values, colLabels=df.columns, loc='center',cellLoc='center')
    tb.auto_set_font_size(False)
    tb.set_fontsize(8)
    #colList = list(range(len(df.columns)))
    colList = [2]
    tb.auto_set_column_width(col=colList)
    
    #plt.axis('off')
    plt.savefig(gSaveBasePath + 'WorldFuturePredict.png')
    plt.show()
    
def createModel(look_back = 1):
    model = Sequential()
    model.add(LSTM(100,input_shape=(1, look_back), activation='relu', return_sequences=True))
    #model.add(LSTM(100, activation='relu', return_sequences=True))
    #model.add(LSTM(50, activation='relu', return_sequences=True))
    model.add(Dense(30,activation='relu'))
    model.add(Dense(20,activation='relu'))
    model.add(Dense(10,activation='relu'))
    model.add(Dense(1))
    
    lr = 1e-3
    #opt = optimizers.SGD(learning_rate=lr) #optimizers.SGD(learning_rate=lr, momentum=0.8, nesterov=False)
    #opt = optimizers.RMSprop(learning_rate=lr, rho=0.9, epsilon=1e-08)
    opt = optimizers.Adam(learning_rate=lr)
    #opt = optimizers.Adadelta(learning_rate=lr)
    #opt = optimizers.Adagrad(learning_rate=lr)
    #opt = optimizers.Adamax(learning_rate=lr)
    #opt = optimizers.Nadam(learning_rate=lr)
    #opt = optimizers.Ftrl(learning_rate=lr)
    
    model.compile(optimizer=opt, loss='mean_squared_error')  #optimizer='adam'
    model.summary()
    return model

def prepareDataset(dataset,look_back):  
    index = dataset.iloc[:,0].values
    rawdata = dataset.iloc[:,1].values 
    rawdata = rawdata.reshape((rawdata.shape[0],1))
    #print('raw=',rawdata[-5:])
    data = preprocessDb(rawdata) #scaler features
    #print('raw=',rawdata[-5:])
    #print('index=',index[-5:])
    X, Y = create_dataset(data, look_back) 
    X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
    
    #x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=12)
    return X,Y, index,rawdata

def train(dataset):
    look_back = 1
    x_train, y_train, index,rawdata = prepareDataset(dataset,look_back)

    model = createModel(look_back)
    model.fit(x_train, y_train, epochs=500, batch_size=150, verbose=2) #500
    
    # a = np.array([trainY[-1]]).reshape(-1,1,1)
    # #a = np.array([[0.88964097]]).reshape(-1,1,1)
    # #a = np.array([0.6]).reshape(1,1,1)
    # print(a)
    # print('predict=', model.predict(a))
    
    #-----------------start plot---------------#
    plotPredictCompare(model,x_train,index,rawdata)
    plotPredictFuture(model,y_train,index,rawdata)
       
def getPredictDf(file):
    df = pd.read_csv(file)
    #df['Date'] = pd.to_datetime(df.Date, format='%m %d, %Y')
    #df.set_index(["Date"], inplace=True)
    return df

def evaulatePredition(df,file):
    def getTrueCases(day,df):
        for i in range(df.shape[0]):
            d = df.iloc[i, df.columns.get_loc('Date')]
            cases = df.iloc[i, df.columns.get_loc('Cases')]
            #d = datetime.datetime.strptime(d,'%b %d, %Y')
            d = datetime.datetime.strptime(d,'%Y-%m-%d')
            #print('day=',day)
            date = datetime.datetime.strptime(day,'%m/%d/%Y')
            #print(d,date,cases)
            if date == d:
                return cases
        return 0
    
    predict = getPredictDf(file) #r'.\dataPredict\2020-08-24_predict.csv'
    predictTime = file[file.rfind('\\')+1 : file.rfind('_')]
    
    #print(predict)
    print('predictTime=',predictTime)
    allCases = np.zeros((predict.shape[0],))
    accs = np.zeros((predict.shape[0],))
    for i in range(predict.shape[0]):
        #date = predict.iloc[i,0]
        #predictCase = predict.iloc[i,1]
        date = predict.loc[i]['Date']
        predictCase = predict.loc[i]['Predicted cases']
        cases = getTrueCases(date,df)
        acc = 0
        if cases != 0:
            acc = round((1 - (np.abs(cases-predictCase)/cases))*100,3)
        
        #print(date,predictCase)
        #print(date,predictCase,cases)
        accs[i] = acc
        allCases[i] = cases
        #break
    predict['Cases'] = allCases
    predict['Precision'] = accs
    predict = predict.iloc[:,1:] #remove index number column
    #print(predict)
    
    #plt.figure(figsize=(8,6))
    title = 'Prediction Precision\n' + 'PredictTime: ' + predictTime + ' CheckTime: '+ getDataTime()
    plt.title(title,fontsize=9)
    tb = plt.table(cellText=predict.values, colLabels=predict.columns, loc='center',  cellLoc='center')
    tb.auto_set_font_size(False)
    tb.set_fontsize(8)
    #colList = list(range(len(predict.columns)))
    colList = [1,2]
    tb.auto_set_column_width(col=colList)
    
    plt.axis('off')
    plt.savefig(gSaveBasePath + 'WorldFuturePredictPrecise.png')
    plt.show()

    
def getNewestFile(path,fmt='csv',index=-1):
    file_dict = {}
    for i in pathsFiles(path,fmt):
        ctime = os.stat(os.path.join(i)).st_ctime
        file_dict[ctime] = i 
        
    #file_dict = sorted(file_dict)
    #print('file_dict=',file_dict)
    #file = file_dict[max(file_dict.keys())]
    #print('file=',file)
    sort = sorted(file_dict.keys())
    #print('sort=',sort)
    return file_dict[sort[index]]

def predict():
    datasetToday = getDataSet()
    train(datasetToday)

    #file = getNewestFile(r'.\dataPredict',index=-4) #compare last time predict 
    #print('Last predicted file:',file)
    #evaulatePredition(datasetToday, file)
    
def main():
    predict()
    
if __name__=='__main__':
    main()