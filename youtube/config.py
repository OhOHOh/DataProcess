# -*- coding: utf-8 -*-

import os

# 指定数据集
dataset_path = './data'

# 指定输出
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)

countries = ['CA', 'DE', 'GB', 'US']

# 使用的列
usecols = ['video_id', 'trending_date', 'channel_title', 'category_id', 'publish_time', 'views', 'likes',
           'dislikes', 'comment_count', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']
