# K-means++聚类
# 使用集成环境的Anaconda3 2023.03-1(Python 3.10.9 64-bit)程序或
# 预先安装 pandas=1.5.3, matplotlib=3.7.0, **scikit-learn=1.2.1** 库, python=3.10.9。

import pandas as pd
from sklearn.cluster import KMeans
import os
os.environ["OMP_NUM_THREADS"] = '3'

# 引入csv数据(跳过表头1行)
filename = './聚类所用数据.csv'
data = pd.read_csv(filename)

# 设置聚类数
k = 31

# 聚类计算（聚类数k及对应数据data）
kmeans = KMeans(init='k-means++', n_init='auto',
                n_clusters=k, random_state=42, algorithm='lloyd').fit(data)

# 输出聚类中心结果并设置好类名
jlzx = pd.DataFrame(kmeans.cluster_centers_)
jlzx.columns = data.columns.values
jlzx.index.name = 'ID'
jlzx.to_csv('%s_聚_%s_簇结果.csv' % (filename, k), index=True, header=True)
# 输出源数据及聚类标签簇
data.insert(loc=0, column='ID', value=kmeans.labels_)
data.to_csv('%s_聚_%s_簇标签.csv' % (filename, k), index=False, header=True)
