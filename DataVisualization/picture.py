from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# plt.figure()
# plt.plot(3, 2, '*')
# plt.plot(4, 3, '*')
# plt.show()

# x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# y = x
# colors = ['red'] * x.shape[0]
# plt.figure()
# plt.scatter(x, y, s=10, c=colors)
#
# plt.show()

# l1 = list(range(1, 6))
# l2 = list(range(6, 11))
# zip_generator = zip(l1, l2)  # 返回值是 zip 类型的
# tuple_list = list(zip_generator)
# # print(type(zip_generator))
# # print(tuple_list)
#
# x, y = zip(*tuple_list)
# # print(x)
# # print(y)
#
# plt.figure()
# plt.scatter(x=x[:2], y=y[:2], c='red', label='sample 1')
# plt.scatter(x=x[2:], y=y[2:], c='blue', label='sample 2')
# plt.xlabel('x label')
# plt.ylabel('y label')
# plt.title('title')
# plt.legend(loc=4)
#
# plt.show()

linear_data = np.arange(1, 9)
data = linear_data ** 2
#
# plt.figure()
# plt.plot(linear_data, '-o', data, '-o')
# # 填充 2 个line 之间的区域
# plt.gca().fill_between(range(len(linear_data)), linear_data, data, facecolors='g', alpha=0.25)
# # plt.gca().fill_betweenx(range(len(linear_data)), linear_data, data, facecolors='g')
# plt.show()

plt.figure()
dates = np.arange('2017-10-11', '2017-10-19', dtype='datetime64[D]')
dates = list(map(pd.to_datetime, dates))
plt.plot(dates, linear_data, '-o',
         dates, data, '-o')

x = plt.gca().xaxis
for item in x.get_ticklabels():
    item.set_rotation(45)

plt.show()
