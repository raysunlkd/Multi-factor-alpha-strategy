# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:39:54 2020

@author: 51722
"""
import pandas as pd
import tushare as ts
ts.set_token('cf3f095c14b78999cb35c771a5df6a2b59af7d3539043975c3e9aa48')
pro=ts.pro_api()
######################################################数据读取#######################################
#获取h30255.CSI（中证500医药）指标每日行情数据
df1_d = pro.index_daily(ts_code='h30255.CSI', start_date='20140101', end_date='20191230')

#df = pro.index_basic(market='CSI')
#df.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\csi.csv', sep=',', header=True, index=True)

##中证500医药20140101-20191230所有成分股
df2 = pro.index_weight(index_code='h30255.CSI', start_date='20140101', end_date='20191230')
stocks=pd.DataFrame(df2['con_code'])
stocks=stocks.drop_duplicates()

##中证500医药20140101-20191230所有成分股
stocks1=stocks.reset_index()


#20140101-20191230 h30255.CSI所有成分股每日行情数据
Data=pd.DataFrame([])

#20140101-20191230 h30255.CSI所有成分股每日指标数据
Index=pd.DataFrame([])
for i in range(len(stocks1)):
    new= pro.daily(ts_code=stocks1['con_code'].iloc[i], start_date='20140101', end_date='20191230')
    new_index=pro.daily_basic(ts_code=stocks1['con_code'].iloc[i], start_date='20140101', end_date='20191230', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,ps,dv_ratio,float_share,free_share,total_mv,circ_mv')
    Data=pd.concat([Data,new],axis=0)
    Index=pd.concat([Index,new_index],axis=0)


###################################################数据存储#################################################
#20140101-20191230 h30255.CSI所有成分股每日指标数据
Index.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\index_daily.csv', sep=',', header=True, index=True)

#20140101-20191230 h30255.CSI所有成分股每日行情数据
Data.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\stocks_daily.csv', sep=',', header=True, index=True)

#20140101-20191230 h30255.CSI指标每日行情数据
df1_d.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\h30255CSI_daily.csv', sep=',', header=True, index=True)

#20140101-20191230 h30255.CSI指标所有成分股组成
df2.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\h30255CSI.csv', sep=',', header=True, index=True)



#df1 = pro.index_basic(market='SW')
#df = pro.index_weight(index_code='801150.SI', start_date='20130131', end_date='20181228')
#df1.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\swindex.csv', sep=',', header=True, index=True)
#df.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\sw_wtg.csv', sep=',', header=True, index=True)

#data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
#data.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\stock_industry.csv', sep=',', header=True, index=True)
#medical=data[(data['industry']=='医疗保健')]
#df = pro.daily_basic(ts_code='', trade_date='20180726', fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,ps,total_share,float_share,total_mv,circ_mv')
#df.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\Dailiy_index.csv', sep=',', header=True, index=True)
#medical.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\medical_basic.csv', sep=',', header=True, index=True)
#medical_daily_index=[]
#medical_daily_index=pd.DataFrame(medical_daily_index)

#for i in range(len(medical['ts_code'])):
#    new=pro.daily_basic(ts_code=medical['ts_code'].iloc[i], trade_date='20180726', fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,ps,total_share,float_share,total_mv,circ_mv')
#    print(new)
#    medical_daily_index=pd.concat([medical_daily_index,new],axis=0)

#medical_daily_index.to_csv('F:\\Courses\\HKUST_Semester_Spring\\MAFS5210\\project1\\medical_daily_index3.csv', sep=',', header=True, index=True)