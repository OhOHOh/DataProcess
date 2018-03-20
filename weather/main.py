# -*- coding: utf-8 -*-

"""
中国五大城市PM2.5数据分析
数据集来源：https://www.kaggle.com/uciml/pm25-data-for-five-chinese-cities, 下载在 data 文件夹中
"""
import csv
import os
import numpy as np
import pandas as pd
import config, config2

def load_data(data_file, usecols):
    """
    读取数据文件, 加载数据
    :param
            - data_file: 数据文件的路径
            - usecols:  data_file 中所使用到的列, list 类型
    :return:
            - data_arr:     数据的多维数组表示
    """
    dataOK = []
    with open(data_file) as csvfile:
        data_reader = csv.DictReader(csvfile)
        # === Step 2. 数据处理 ===
        for row in data_reader: # 目的是把每行数据提取出来, 放在 row_data 中
            row_data = []
            for col in usecols:
                row_data.append(float(row[col]) if row[col] != 'NA' else np.nan)
            if not any(np.isnan(row_data)): # 要是一行中有数据是 'NA' 的, 那这行数据就不能要
                dataOK.append(row_data)

    data_arr = np.array(dataOK) # 将 dataOK 转换为 ndarray

    return data_arr

def get_polluted_perh(data_arr):
    """
    获取所给 data_arr 中每个城市总体污染程度的小时数占总小时数的比例, 借此来分析天气情况
    规则：
            重度污染(heavy)     PM2.5 > 150
            重度污染(medium)    75 < PM2.5 <= 150
            轻度污染(light)     35 < PM2.5 <= 75
            优良空气(good)      PM2.5 <= 35
    :param
            - data_arr: 清洗过的数据
    :return:
            - polluted_perc_list: 污染小时数百分比列表
    """
    hour_val = np.mean(data_arr[:, 2:], axis=1) #返回值是 list, 并且是 ndarry 对象
    n_hours = hour_val.shape[0]     # 总的小时数
    # 重度污染小时
    n_heavy_hours = hour_val[hour_val > 150].shape[0] # shape[0] 就是看第一维的大小
    # 中度污染小时数
    n_medium_hours = hour_val[(hour_val > 75) & (hour_val <= 150)].shape[0]
    # 轻度污染小时数
    n_light_hours = hour_val[(hour_val > 35) & (hour_val <= 75)].shape[0]
    # 优良空气小时数
    n_good_hours = hour_val[hour_val <= 35].shape[0]

    polluted_perh_list = [
        n_heavy_hours/n_hours, n_medium_hours/n_hours, n_light_hours/n_hours, n_good_hours/n_hours
    ]

    return polluted_perh_list

def get_avg_pm_per_month(data_arr):
    """
    获取每个区每月的平均PM值
    :param
            - data_arr:
    :return:
            - results_arr:
    """
    results = []
    # 获取年份
    years = np.unique(data_arr[:, 0])

    for year in years:
        year_data_arr = data_arr[data_arr[:, 0] == year]
        month_list = np.unique(year_data_arr[:, 1])

        for month in month_list:
            month_data_arr = data_arr[data_arr[:, 1] == month]
            mean_vals = np.mean(month_data_arr[:, 2:], axis=0).tolist()  # 只有3列数据
            # 格式化字符串
            row_data = ["{:.0f}-{:02.0f}".format(year, month)] + mean_vals
            results.append(row_data)
    results_arr = np.array(results)

    return results_arr

def save_stats_to_csv(results_arr, save_file, headers):
    """
    将统计结果保存至 csv 文件中
    :param results_arr:
    :param
            - save_file:
            - headers:
    """
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in results_arr:
            writer.writerow(row)


# == 接下来是任务2, 主要探讨中美之间的数据差异, 并使用 pandas ==

def perprocess_data(data_df, city_name):
    """
    :param
        - data_df:
        - city_name:
    :return:
        - cln_data_df
    """
    # 把有空数据的行 , 都扔掉
    cln_data_df = data_df.dropna()
    # 重建索引 , drop=True 表示我不要原来的 index 了
    cln_data_df = cln_data_df.reset_index(drop=True)
    # 添加新的 1 列
    cln_data_df['city'] = city_name

    # 输出信息
    print('{}共有{}行数据，其中有效数据为{}行'.format(city_name, data_df.shape[0], cln_data_df.shape[0]))
    print('{}的前10行有效数据：'.format(city_name))
    print(cln_data_df.head(10))

    return cln_data_df

def get_china_us_pm_df(cln_data_df, suburb_cols):
    """

    :param
        - cln_data_df:
        - suburb_cols:
    :return:
        - proc_data_df
    """
    pm_suburb_cols = ['PM_'+col for col in suburb_cols]
    cln_data_df['PM_China'] = cln_data_df[pm_suburb_cols].mean(axis=1)
    proc_data_df = cln_data_df[config2.common_cols + ['city', 'PM_China']]

    return proc_data_df

def add_date_col_to_df(cln_data_df):
    """

    :param
        - cln_data_df:
    :return:
    """
    proc_data_df = cln_data_df.copy()
    proc_data_df[['year', 'month', 'day']] = proc_data_df[['year', 'month', 'day']].astype('str')
    # 合并 3 列
    proc_data_df['date'] = proc_data_df['year'].str.cat([proc_data_df['month'], proc_data_df['day']], sep='-')
    # 删除列
    proc_data_df = proc_data_df.drop(['year', 'month', 'day'], axis=1)
    # 调整列的顺序
    proc_data_df = proc_data_df[['date', 'city', 'PM_China', 'PM_US Post']]

    return proc_data_df

def add_polluted_state_col_to_df(day_stats):
    """
    分箱操作
    :param
        - cln_data_df:
    :return:
        - proc_day_stats
    """
    proc_day_stats = day_stats.copy()
    bins = [-np.inf, 35, 75, 150, np.inf]
    state_labels = ['good', 'light', 'medium', 'heavy']
    proc_day_stats['Polluted State CH'] = pd.cut(proc_day_stats['PM_China'], bins=bins, labels=state_labels)
    proc_day_stats['Polluted State US'] = pd.cut(proc_day_stats['PM_US Post'], bins=bins, labels=state_labels)

    return proc_day_stats

def compare_state_by_day(day_status):
    """

    :param
        - day_status:
    :return:
        - comparison_result
    """
    city_names = config2.data_config_dict.keys()    # 获取城市名字 list
    city_comparison_list = []
    for city_name in city_names:
        city_df = day_status[day_status['city'] == city_name]

        city_polluted_days_count_ch = pd.value_counts(city_df['Polluted State CH']).to_frame(name=city_name + '_ch')
        city_polluted_days_count_us = pd.value_counts(city_df['Polluted State US']).to_frame(name=city_name + '_us')

        series_city_polluted_days_count_ch = pd.value_counts(city_df['Polluted State CH'])
        series_city_polluted_days_count_ch.index.name = 'polluted state'
        df_city_polluted_days_count_ch = series_city_polluted_days_count_ch.to_frame(name=city_name+'_ch')

        series_city_polluted_days_count_us = pd.value_counts(city_df['Polluted State US'])
        series_city_polluted_days_count_us.index.name = 'polluted state'
        df_city_polluted_days_count_us = series_city_polluted_days_count_us.to_frame(name=city_name+'_us')

        city_comparison_list.append(city_polluted_days_count_ch)
        city_comparison_list.append(city_polluted_days_count_us)

    # 横向组合 DataFrame
    comparison_result = pd.concat(city_comparison_list, axis=1)
    comparison_result.index.name = 'polluted state'
    print('\n============\n============\n============')
    print(city_comparison_list)
    print(comparison_result)

    return comparison_result




def main():
    print('hello world')
    # polluted_state_list = []
    #
    # for cityname, (filename, cols) in config.data_config_dict.items():
    #     # === Step 1+2. 数据获取 + 数据处理 === load_data
    #     data_file = os.path.join(config.dataset_path, filename)
    #     usecols = config.common_cols + [('PM_' + col) for col in cols]
    #     print(cityname, filename, data_file, usecols)
    #
    #     data_arr = load_data(data_file, usecols)
    #
    #     print("{}共有{}行有效数据".format(cityname, len(data_arr)))
    #
    #     # === Step 3. 数据分析 === get_polluted_perh
    #     # 五城市污染状态，统计污染小时数的占比
    #     polluted_perh_list = get_polluted_perh(data_arr)
    #     polluted_state_list.append([cityname]+polluted_perh_list)
    #
    #     print("{}的污染小时数百分比{}".format(cityname, polluted_perh_list))
    #
    #     # 五城市每个区空气质量的月度差异，分析计算每个月，每个区的平均PM值
    #     results_arr = get_avg_pm_per_month(data_arr)
    #     print('{}的每月平均PM值预览：'.format(cityname))
    #     print(results_arr[:10])
    #
    #     # === Step 4. 结果展示 ===
    #     # 4.1 保存月度统计结果至csv文件
    #     save_filename = cityname + '_month_stats.csv'
    #     save_file = os.path.join(config.output_path, save_filename) #最终的路径, 包括文件名
    #
    #     save_stats_to_csv(results_arr, save_file, headers=['month'] + cols)
    #     print('月度统计结果已保存至{}'.format(save_file))
    #
    #     # 4.2 污染状态结果保存
    #     save_file = os.path.join(config.output_path, 'polluted_percentage.csv')
    #     with open(save_file, 'w', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow(['city', 'heavy', 'medium', 'light', 'good'])
    #         for row in polluted_state_list: #polluted_state_list 中也应该是对应 5 列
    #             writer.writerow(row)
    #     print('污染状态结果已保存至{}'.format(save_file))
    #     print()
    #     print()
    print('接下来是任务2, 主要探讨中美之间的数据差异, 并使用 pandas')
    city_data_list = []
    for city_name, (filename, cols) in config2.data_config_dict.items():
        # == 1. 数据获取 ==
        data_file = os.path.join(config2.dataset_path, filename)
        usecols = config2.common_cols + ['PM_'+col for col in cols]
        # 读入数据
        data_df = pd.read_csv(data_file, usecols=usecols)
        # == 2. 数据处理 ==
        cln_data_df = perprocess_data(data_df, city_name)

        # 处理获取中国与美国的 PM 数据
        proc_data_df = get_china_us_pm_df(cln_data_df, cols)
        city_data_list.append(proc_data_df)

    print('city_data_list: ')
    print(city_data_list)

    # 合并 5 个城市的处理后的数据
    all_data_df = pd.concat(city_data_list)
    all_data_df = add_date_col_to_df(all_data_df)

    # == 3. 数据分析 ==
    # 通过分组操作获取每个城市每天的 PM 均值
    day_status = all_data_df.groupby(['city', 'date'])[['PM_China', 'PM_US Post']].mean()
    print("\n\n\n\n")
    print(day_status)
    day_status.reset_index(inplace=True)

    # 分箱操作 !!!
    day_status = add_polluted_state_col_to_df(day_status)
    print("\n\n\n\n")
    print(day_status)
    comparison_result = compare_state_by_day(day_status)

    # == 4. 结果展示 == 统计各个污染程度的天数
    all_data_df.to_csv(os.path.join(config2.output_path, 'all_cities_pm.csv'), index=False)
    day_status.to_csv(os.path.join(config2.output_path, 'day_status.csv'))
    comparison_result.to_csv(os.path.join(config2.output_path, 'comparison_result.csv'))





if __name__ == '__main__':
    main()
