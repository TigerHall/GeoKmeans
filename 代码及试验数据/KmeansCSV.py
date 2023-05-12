# K-means++聚类。
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from matplotlib import rcParams
# 防止内存泄漏
os.environ["OMP_NUM_THREADS"] = '3'
# 中文正常显示设置
config = {
    "font.family": 'serif',  # 衬线字体
    "font.size": 12,  # 相当于小四大小
    "font.serif": ['SimSun'],  # 宋体
    "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
    'axes.unicode_minus': False  # 处理负号，即-号
}
rcParams.update(config)


# 聚类数设置
k = 2

# 传入文件名及聚类数
def kmeanscsv(filename,k):
    # 读取数据
    data = pd.read_csv(filename)
    # 聚类计算（聚类数k及对应数据data）
    kmeans = KMeans(init='k-means++', n_init=1,
                    n_clusters=k, random_state=42).fit(data)
    # 输出聚类中心结果并设置好类名
    jlzx = pd.DataFrame(kmeans.cluster_centers_)
    jlzx.columns = data.columns.values
    jlzx.index.name = 'ID'
    jlzx.to_csv(f'{filename}_聚_{k}_簇聚类中心.csv', index=True, header=True)
    # 输出源数据及聚类标签簇
    data.insert(loc=0, column='ID', value=kmeans.labels_)
    data.to_csv(f'{filename}_聚_{k}_簇原数据及聚类簇标签.csv', index=False, header=True)

def lkxscsv(filename):
    # 引入csv数据(跳过表头1行)
    data = pd.read_csv(filename)
    rows = len(data.index)
    # 设置聚类数范围(大于2)
    Kran = range(2, (rows-1), int(rows/10))

    # 设置存放轮廓系数(silhouette coefficient)和SSE(sum of the squared errors，误差平方和)计算结果的数组
    Silhouette = []
    SSE = []
    # 循环运算以获得各聚类数下的轮廓系数
    for kk in Kran:
        # 定义KMeans，以及K值
        kmeans = KMeans(init='k-means++', n_init=1,
                        n_clusters=kk, random_state=42)
        # 根据数据data进行聚类计算并获得聚类序列，结果存放于result_list中
        result_list = kmeans.fit_predict(data)
        # 将原始数据data和聚类序列result_list传入对应的函数计算出该结果下的轮廓系数
        score = silhouette_score(data, result_list)
        # 存放每种聚类数计算出的两个结果
        Silhouette.append(score)
        SSE.append(kmeans.fit(data).inertia_)

    # 将数据转化为CSV
    dfc = pd.DataFrame()
    dfc['X(K值)'] = Kran
    dfc['Y1(轮廓系数)'] = Silhouette
    dfc['Y2(均值失真)'] = SSE
    dfc.index.name = 'Ordinal'
    dfc.to_csv(f'{filename}_轮廓系数计算[{Kran}].csv', index=True,
            header=True, encoding="utf_8_sig")

    # 绘图
    fig, ax1 = plt.subplots(dpi=600)
    # 用同一个X轴
    ax2 = ax1.twinx()
    # 绘制线
    ax1.plot(Kran, SSE, 'b-', linewidth=2)
    ax2.plot(Kran, Silhouette, 'r-', linewidth=2)

    # 设置轴标题
    ax1.set_xlabel('K值', color='k')
    ax1.set_ylabel('误差平方和(均值失真)', color='b')
    ax2.set_ylabel('轮廓系数', color='r')
    # 设置轴标签样式
    ax1.tick_params(tickdir='inout', labelsize=10)
    ax1.ticklabel_format(style='sci', axis='y',
                        scilimits=(-1, 2), useMathText=True)
    ax2.tick_params(tickdir='inout', labelsize=10)

    # 图输出
    plt.tight_layout()
    svgfilename=f"{filename}_轮廓系数及误差平方和_{Kran}.svg"
    plt.savefig(fname=svgfilename,
                format="svg", dpi=600, transparent=True, bbox_inches='tight')