import pandas as pd

country1 = pd.Series({
    'Name': '中国',
    'Language': 'Chinese',
    'Area': '9.59M km2',
    'Happiness Rank': 79
})
country2 = pd.Series({
    'Name': '美国',
    'Language': 'English(US)',
    'Area': '9.834M km2',
    'Happiness Rank': 14
})
country3 = pd.Series({
    'Name': '澳大利亚',
    'Language': 'English(AU)',
    'Area': '7.62M km2',
    'Happiness Rank': 9
})

#df = pd.DataFrame([country1, country2, country3], index=['CH', 'US', 'AU'])
#print(df.loc['CH']['Name'])


#  Pandas 加载 csv 文件
report_2015_df = pd.read_csv('./data1/2015.csv')
# print(report_2015_df.describe().loc['mean'])
#print(report_2015_df.index[0] )
grouped = report_2015_df.groupby('Region')
print(grouped.size())

report_2015_df2 = report_2015_df.set_index(['Region', 'Country'])   # 设置新的 行索引
# print(report_2015_df2.loc['Western Europe'].loc['Switzerland']) # report_2015_df2.loc['Western Europe', 'Switzerland']
# print(report_2015_df2.sort_index(level=0))

report_2016_df = pd.read_csv(
    './data1/2016.csv',
    index_col='Country',
    usecols=['Country', 'Happiness Rank', 'Happiness Score', 'Region']
)
# print(report_2016_df.reset_index().head())
# print(report_2016_df.head())
report_2016_df.reset_index(inplace=True)
report_2016_df.rename(columns={'Region': '地区', 'Happiness Rank': '排名', 'Happiness Score': '幸福指数', 'Country': '国家'},
                      inplace=True)
# print(report_2016_df)
#print(report_2016_df[(report_2016_df['地区']=='Western Europe') & (report_2016_df['排名'] > 10)])

log_data = pd.read_csv('./data1/log.csv')
# print(log_data[log_data['volume'].notnull()])
# print(log_data.dropna())
