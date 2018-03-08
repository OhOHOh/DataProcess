# -*- coding: utf-8 -*-

"""
中国五大城市PM2.5数据分析
数据集来源：https://www.kaggle.com/uciml/pm25-data-for-five-chinese-cities, 下载在 data 文件夹中
"""
import csv
import os
import numpy as np
import config

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


def main():
    print('hello world')
    polluted_state_list = []

    for cityname, (filename, cols) in config.data_config_dict.items():
        # === Step 1+2. 数据获取 + 数据处理 === load_data
        data_file = os.path.join(config.dataset_path, filename)
        usecols = config.common_cols + [('PM_' + col) for col in cols]
        print(cityname, filename, data_file, usecols)

        data_arr = load_data(data_file, usecols)

        print("{}共有{}行有效数据".format(cityname, len(data_arr)))

        # === Step 3. 数据分析 === get_polluted_perh
        # 五城市污染状态，统计污染小时数的占比
        polluted_perh_list = get_polluted_perh(data_arr)
        polluted_state_list.append([cityname]+polluted_perh_list)

        print("{}的污染小时数百分比{}".format(cityname, polluted_perh_list))

        # 五城市每个区空气质量的月度差异，分析计算每个月，每个区的平均PM值
        results_arr = get_avg_pm_per_month(data_arr)
        print('{}的每月平均PM值预览：'.format(cityname))
        print(results_arr[:10])

        # === Step 4. 结果展示 ===
        # 4.1 保存月度统计结果至csv文件
        save_filename = cityname + '_month_stats.csv'
        save_file = os.path.join(config.output_path, save_filename) #最终的路径, 包括文件名

        save_stats_to_csv(results_arr, save_file, headers=['month'] + cols)
        print('月度统计结果已保存至{}'.format(save_file))

        # 4.2 污染状态结果保存
        save_file = os.path.join(config.output_path, 'polluted_percentage.csv')
        with open(save_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['city', 'heavy', 'medium', 'light', 'good'])
            for row in polluted_state_list: #polluted_state_list 中也应该是对应 5 列
                writer.writerow(row)
        print('污染状态结果已保存至{}'.format(save_file))
        print()
        print()


if __name__ == '__main__':
    main()
