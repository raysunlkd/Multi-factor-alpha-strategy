# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 23:56:31 2020

@author: 51722
"""

import pandas as pd
import numpy as np
###读入每日指数数据
BM_price=pd.read_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\code\\h30255CSI_daily.csv',sep=',')
BM_weight=pd.read_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\code\\h30255CSI.csv',sep=',')

##读入指数成分股每日指标数据
stocks_index_d=pd.read_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\code\\index_daily.csv',sep=',')
stocks_price_d=pd.read_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\code\\stocks_daily.csv',sep=',')


###set the trade_date as datetime index
BM_price['trade_date']=pd.to_datetime(BM_price['trade_date'],format='%Y%m%d')
BM_price=BM_price.set_index('trade_date')

BM_weight['trade_date']=pd.to_datetime(BM_weight['trade_date'],format='%Y%m%d')
BM_weight=BM_weight.set_index('trade_date')

stocks_index_d['trade_date']=pd.to_datetime(stocks_index_d['trade_date'],format='%Y%m%d')
stocks_index_d=stocks_index_d.set_index('trade_date')

stocks_price_d['trade_date']=pd.to_datetime(stocks_price_d['trade_date'],format='%Y%m%d')
stocks_price_d=stocks_price_d.set_index('trade_date')

#Due to the available datas in BM_price has NaN from 2019-06-12 to 2019-07-01
##we update all the available datas ending up on 2019-05-31 
BM_price_real=BM_price[BM_price.index<=pd.datetime(2019,5,31)]
BM_weight_real=BM_weight[BM_weight.index<=pd.datetime(2019,5,31)]
stocks_index_d_real=stocks_index_d[stocks_index_d.index<=pd.datetime(2019,5,31)]
stocks_price_d_real=stocks_price_d[stocks_price_d.index<=pd.datetime(2019,5,31)]

#define tradedate respectively per month and per day
tradedate_m=BM_weight_real.index
tradedate_d=BM_price_real.index
tradedate_m=tradedate_m.drop_duplicates()


#Product a well data framework
Data=pd.DataFrame([])
total_m=len(tradedate_m)
for i in range(total_m):
        
    stocks_wgt_m=BM_weight_real[BM_weight_real.index==tradedate_m[i]][['con_code','weight']]
    ##caculate the right weights(divide weights by their sum)
    stocks_wgt_m['weight']=stocks_wgt_m['weight']/sum(stocks_wgt_m['weight'])
    tdm=tradedate_m[i]
    ts_code=stocks_wgt_m['con_code']
    new_index=pd.DataFrame([])
    new_price=pd.DataFrame([])
    print(tdm)
    print('Datas of the {} constituent stocks for current month is going to be arranged'.format(len(ts_code)))
    if i == (total_m-1):
        for j in range(len(ts_code)):
            ##get the daily index datas of stocks forming the benchmark
            new_index_temp=stocks_index_d_real[
                    (stocks_index_d_real.index<=tradedate_m[i])&
                    (stocks_index_d_real.ts_code == ts_code.iloc[j])]
            new_index=pd.concat([new_index,new_index_temp],axis=0,sort=False)
            
            ##get the daily price datas of stocks forming the benchmark
            new_price_temp= stocks_price_d_real[
                    (stocks_price_d_real.index<=tradedate_m[i])&
                    (stocks_price_d_real.ts_code == ts_code.iloc[j])]
            new_price=pd.concat([new_price,new_price_temp],axis=0,sort=False)
        ##add the weight of the stocks in the benchmark
        #stocks_wgt_m['weight']=stocks_wgt_m['weight']/sum(stocks_wgt_m['weight'])
        new_price['weight']= np.linspace(1,len(new_price.ts_code),len(new_price.ts_code))
        for k in range(len(ts_code)):
            new_price.loc[new_price['ts_code']==stocks_wgt_m['con_code'].iloc[k],'weight']=stocks_wgt_m['weight'].iloc[k]
        ##merge index and stocks_price by columns
        Data_new=pd.concat([new_price,new_index],axis=1,sort=False)
        ##drop the duplicated columns(['Unnamed: 0','ts_code']).
        Data_new=Data_new.T.drop_duplicates().T
        Data=pd.concat([Data,Data_new],axis=0,sort=False)
        print('Arrangement well done for current month, {} months remain.'.format(len(tradedate_m)-i-1))    
    else:
        for j in range(len(ts_code)):
            ##get the daily index datas of stocks forming the benchmark
            new_index_temp=stocks_index_d_real[
                    (tradedate_m[i+1]<stocks_index_d_real.index)&
                    (stocks_index_d_real.index<=tradedate_m[i])&
                    (stocks_index_d_real.ts_code == ts_code.iloc[j])]
            new_index=pd.concat([new_index,new_index_temp],axis=0,sort=False)
            
            ##get the daily price datas of stocks forming the benchmark
            new_price_temp= stocks_price_d_real[
                    (tradedate_m[i+1]<stocks_price_d_real.index)&
                    (stocks_price_d_real.index<=tradedate_m[i])&
                    (stocks_price_d_real.ts_code == ts_code.iloc[j])]
            new_price=pd.concat([new_price,new_price_temp],axis=0,sort=False)
        ##add the weight of the stocks in the benchmark
        #stocks_wgt_m['weight']=stocks_wgt_m['weight']/sum(stocks_wgt_m['weight'])
        new_price['weight']= np.linspace(1,len(new_price.ts_code),len(new_price.ts_code))
        for k in range(len(ts_code)):
            new_price.loc[new_price['ts_code']==stocks_wgt_m['con_code'].iloc[k],'weight']=stocks_wgt_m['weight'].iloc[k]
        ##merge index and stocks_price by columns
        Data_new=pd.concat([new_price,new_index],axis=1,sort=False)
        ##drop the duplicated columns(['Unnamed: 0','ts_code']).
        Data_new=Data_new.T.drop_duplicates().T
        Data=pd.concat([Data,Data_new],axis=0,sort=False)
        
        ##Compute the number of missed constituent stocks
        if (len(ts_code)!=len(Data_new.loc[tdm,'weight'])):
            print('There are {} constituent stocks datas missed'
                  .format(len(ts_code)-len(Data_new.loc[tdm,'weight'])))
        print('Arrangement well done for current month, {} months remain.'.format(len(tradedate_m)-i-1))
        
print(Data.isnull().any())

###Dealing with the NaN
Data=Data.fillna(method='bfill')
print(Data.isnull().any())
##save data
Data.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\Data.csv', sep=',', header=True, index=True)
