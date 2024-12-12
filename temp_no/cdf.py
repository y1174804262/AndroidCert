import numpy as np
import pandas as pd
from matplotlib import rcParams
import matplotlib.pyplot as plt

from neo4j.neo4j_match.table_5_cert_validity import match_node_validity

# 设置中文字体，解决中文显示乱码问题
rcParams['font.sans-serif'] = ['Times New Roman']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
rcParams.update({'font.weight': 'bold'})
days = list()
counts = list()
# rcParams.update({'font.size': 12, 'fontweight='bold'})
days = list()
counts = list()
validity = match_node_validity("根证书")
series = pd.Series(validity)
count = series.value_counts()
for i in count.index:
    days = days + [i]
    counts = counts + [count[i]]
months = np.array(days) / 365   # 将天数转换为月数
expanded_data = np.repeat(months, counts)  # 重复数据以绘制CDF
sorted_data_1 = np.sort(expanded_data)  # 对数据进行排序

# 计算CDF
cdf_1 = np.arange(1, len(sorted_data_1) + 1) / len(sorted_data_1)


days = list()
counts = list()
validity = match_node_validity("中间证书")
series = pd.Series(validity)
count = series.value_counts()
for i in count.index:
    days = days + [i]
    counts = counts + [count[i]]
months = np.array(days) / 365   # 将天数转换为月数
expanded_data = np.repeat(months, counts)  # 重复数据以绘制CDF
sorted_data_2 = np.sort(expanded_data)  # 对数据进行排序

# 计算CDF
cdf_2 = np.arange(1, len(sorted_data_2) + 1) / len(sorted_data_2)



days = list()
counts = list()
validity = match_node_validity("终端证书")
series = pd.Series(validity)
count = series.value_counts()
for i in count.index:
    days = days + [i]
    counts = counts + [count[i]]
months = np.array(days) / 365   # 将天数转换为月数
expanded_data = np.repeat(months, counts)  # 重复数据以绘制CDF
sorted_data_3 = np.sort(expanded_data)  # 对数据进行排序

# 计算CDF
cdf_3 = np.arange(1, len(sorted_data_3) + 1) / len(sorted_data_3)

# 开始绘制
plt.figure(figsize=(11.5, 8))

# 绘制CDF曲线

plt.plot(sorted_data_1, cdf_1, color="black", linestyle='-.', label='Root Certificates')
plt.plot(sorted_data_2, cdf_2, color="black", linestyle=':', label='Intermediate Certificates')
plt.plot(sorted_data_3, cdf_3, color="black", linestyle='--', label='Leaf Certificates')

# 添加标题和标签
# plt.title('证书的有效期累积分布')
plt.xlabel('Validity Period (in years)', fontsize=18, fontweight='bold')
plt.ylabel('Certificates', fontsize=18, fontweight='bold')

# 设置坐标轴范围
plt.xlim(0, 35)
plt.ylim(0.0, 1.0)

plt.xticks(range(0, 35, 2), fontsize=18)
plt.yticks(np.arange(0.0, 1.0, 0.1), fontsize=18)
# 添加图例
plt.legend(fontsize=18)

# 显示网格
# plt.grid(True)

# 显示图形
plt.show()
