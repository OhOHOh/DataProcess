# 对 北京 进行操作, 看看结果是怎么样的

import numpy as np
import pandas as pd
import config
import os
import config2

data_file = './data/BeijingPM20100101_20151231.csv'
usecols = ['year', 'month', 'day', 'PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan', 'PM_US Post']
suburb_cols = ['year', 'month', 'day']

data_df = pd.read_csv(data_file, usecols=usecols)
# === 数据清洗
cln_data_df = data_df.dropna()
cln_data_df = cln_data_df.reset_index(drop=True)
cln_data_df['city'] = 'beijing'

# === 求得 beijing 3 个区的 PM 的均值
cln_data_df['PM_China'] = cln_data_df[['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan']].mean(axis=1)
cln_data_df.drop(columns=['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan'], inplace=True)

# === 把日期3列格式化一下
cln_data_df[suburb_cols] = cln_data_df[suburb_cols].astype('str')
# cln_data_df['date'] = cln_data_df['year'].str.cat(cln_data_df['month'], sep='-').str.cat(cln_data_df['day'], sep='-')
cln_data_df['date'] = cln_data_df['year'].str.cat([cln_data_df['month'], cln_data_df['day']], sep='-')
cln_data_df.drop(columns=suburb_cols, inplace=True)
cln_data_df = cln_data_df[['date', 'city', 'PM_China', 'PM_US Post']]

# === 对不同的 PM 值, 进行分类, 良好、轻度、中等、重度 4个等级
bins = [-np.inf, 35, 75, 150, np.inf]
pm_state_labels = ['good', 'light', 'medium', 'heavy']
cln_data_df['PM_State CH'] = pd.cut(cln_data_df['PM_China'], bins=bins, labels=pm_state_labels)
cln_data_df['PM_State US'] = pd.cut(cln_data_df['PM_US Post'], bins=bins, labels=pm_state_labels)

cln_data_df.drop(columns=['PM_China', 'PM_US Post'], inplace=True)
# === 统计 中美 两国对各个等级，天数的比较
city_polluted_state_count_ch = pd.value_counts(cln_data_df['PM_State CH']).to_frame()
city_polluted_state_count_us = pd.value_counts(cln_data_df['PM_State US']).to_frame()
# compare_result = pd.concat(city_polluted_state_count_ch, city_polluted_state_count_us)
compare_result = pd.concat(objs=[city_polluted_state_count_ch, city_polluted_state_count_us], axis=1)

compare_result.to_csv(os.path.join(config2.output_path, 'beijing_CH_US.csv'))

print(city_polluted_state_count_us)
print(type(city_polluted_state_count_ch))
print(compare_result)
# print(cln_data_df.head(10))

