import pandas as pd
import matplotlib.pyplot as plt

# 创建数据
data = {
    '列1': [10, 20, 30],
    '列2': [15, 25, 35],
    '列3': [20, 30, 40]
}

# 创建 DataFrame，没有标题行
df = pd.DataFrame(data, index=['行1', '行2', '行3'])

# 创建自定义表格
def create_custom_table(dataframe):
    fig, ax = plt.subplots()

    # 隐藏轴
    ax.axis('off')
    ax.axis('tight')

    # 绘制表格，没有列标签
    table = ax.table(cellText=dataframe.values,
                     rowLabels=dataframe.index,
                     cellLoc='center',
                     loc='center')

    # 设置表格样式
    table.scale(1, 2)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # 自定义边框线
    for (i, j), cell in table.get_celld().items():
        cell.set_linewidth(0)  # 移除所有边框线

        # 设置第一行的上下框线
        if i == 0:
            cell.set_edgecolor('black')
            if j == -1:  # 行标签
                cell.set_linewidth(0)
            else:
                cell.set_linewidth(2)  # 上下框线

        # 设置最后一行的下框线
        if i == len(dataframe):
            if j >= 0:  # 不设置行标签边框
                cell.set_edgecolor('black')
                cell.set_linewidth(2)  # 下框线

    plt.show()

# 调用函数创建自定义表格
create_custom_table(df)
