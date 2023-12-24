import numpy as np
import matplotlib.pyplot as plt

def calcfunc(x, y):
    result = y / (x + y) / 2
    result_formatted = '{:.3%}'.format(result)
    return result_formatted


x = np.arange(4)
division1 = np.array([78, 83, 86, 247])
division2 = np.array([14, 16, 16, 47])

plt.bar(x, division2, label = 'second division')

plt.bar(x, division1, bottom=division2, label = 'first division')
plt.legend()
plt.xticks(x, ['LiZehua', 'YuZhenyang', 'YuXiaoxuan', 'sum'])
# 添加文字
for i in range(len(x)):
    plt.text(x[i], division1[i] + division2[i], calcfunc(division1[i], division2[i]), ha='center', va='bottom')

plt.savefig('../img/python_result.png')