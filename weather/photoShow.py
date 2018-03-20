# 绘制一个 柱状图, 第3讲的内容
from pyecharts import Bar
import pandas as pd

comp_df = pd.read_csv('./output/comparison_result.csv', index_col='polluted state')
print(comp_df)


good_state_results = comp_df.iloc[0, :].values
heavy_state_results = comp_df.iloc[1, :].values
light_state_results = comp_df.iloc[2, :].values
medium_state_results = comp_df.iloc[3, :].values

labels = comp_df.index.values.tolist()
city_names = comp_df.columns.tolist()

bar = Bar("堆叠柱状图")
bar.add('良好', city_names, good_state_results, is_stack=True, xaxis_interval=0, xaxis_rotate=30)
bar.add('轻度污染', city_names, light_state_results, is_stack=True, xaxis_interval=0, xaxis_rotate=30)
bar.add('中度污染', city_names, medium_state_results, is_stack=True, xaxis_interval=0, xaxis_rotate=30)
bar.add('重度污染', city_names, heavy_state_results, is_stack=True, xaxis_interval=0, xaxis_rotate=30)

bar.render(path='./output/picture.html')
