# 对 北京 进行操作, 看看结果是怎么样的

import pandas as pd
import config
import os

data_file = './data/BeijingPM20100101_20151231.csv'
usecols = ['year', 'month', 'day', 'PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']

data_df = pd.read_csv(data_file, usecols=usecols)
# 数据清洗
cln_data_df = data_df.dropna()
cln_data_df = cln_data_df.reset_index(drop=True)
cln_data_df['city'] = 'beijing'


print(cln_data_df)
