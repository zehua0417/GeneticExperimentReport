import os
import pandas as pd

# 设置工作目录
os.chdir("F:/Onedrive/study/生物/遗传学/实验报告/3_Human DNA Fingerprint Analysis/python")

# 导入数据 ###########################
csv_files = [file for file in os.listdir("../data") if file.endswith(".csv") and file != "summary.csv"]
csv_files = [os.path.join("..\data", file) for file in csv_files]
data_list = [pd.read_csv(file) for file in csv_files]
# 显示导入的数据 ######################
#for i, data in enumerate(data_list):
#    print(f"Data from file {csv_files[i]}:\n")
#    print(data)

class DnaFingerprintLane:
    """
    DNA 指纹泳道类

    Attributes:

        m_filename: 文件名
        m_data: 数据
        m_edge: 177
        m_edge2: 4945
        m_laneID: 泳道编号
        m_category: 类别（marker 或 sample）
        m_MW: 分子量
        m_repeatNum: 重复次数
        m_homoORheter: 同源或异源
    """
    def __init__(self, data, filename):
        self.m_filename = filename
        self.m_data = data

        self.m_edge = 177
        self.m_edge2 = 4945
        self.m_laneID = data["Lane #"].iloc[0]
        if len(data[" Band #"]) == 11:
            self.m_category = "marker"
            self.m_MW = None
            self.m_repeatNum = None
            self.m_homoORheter = None

        else:
            self.m_category = "sample"
            self.m_MW = data[" MW"][(data[" MW"] > self.m_edge) & (data[" MW"] < self.m_edge2)].astype(float).tolist()
            self.m_repeatNum = self.calculate_repeat_num()
            if len(self.m_MW) == 1:
                self.m_homoORheter = "homo"
            elif len(self.m_MW) == 2:
                self.m_homoORheter = "heter"
            elif len(self.m_MW) > 2:
                self.m_homoORheter = "contamination"
            elif len(self.m_MW) == 0:
                self.m_homoORheter = "no result"
            else:
                self.m_homoORheter = "???"

    def calculate_repeat_num(self):

        mw_series = pd.Series(self.m_MW)
        repeat_num = 1 + (mw_series[mw_series > self.m_edge] - 161) / 16
        return repeat_num.astype(float).tolist()
    def printLane(self):
        print(f"文件：{self.m_filename}")
        print(f"泳道编号：{self.m_laneID}")
        print(f"类别：{self.m_category}")
        if self.m_category == "sample":
            print(f"分子量：{', '.join(map(str, self.m_MW))}")
            print(f"重复次数：{', '.join(map(str, self.m_repeatNum))}")
            print(f"同源或异源：{self.m_homoORheter}")
            print("-" * 30)

lane_objects = []

for i, data_frame in enumerate(data_list):
    for j in data_frame["Lane #"].unique():
        lane = data_frame[data_frame["Lane #"] == j]
        #DnaFingerprintLane(lane, csv_files[i]).printLane()
        lane_objects.append(DnaFingerprintLane(lane, csv_files[i]))

# for lane in lane_objects:
#     lane.printLane()

import matplotlib.pyplot as plt
import numpy as np

# Filter lanes based on m_homoORheter attribute
filtered_lanes = [lane for lane in lane_objects if lane.m_category == "sample" and lane.m_homoORheter in ["homo", "heter"]]
for lane in filtered_lanes:
    lane.printLane()

repeat_nums = []
for lane in filtered_lanes:
    repeat_nums.extend(lane.m_repeatNum)

plt.hist(repeat_nums, bins=30, edgecolor='black')
plt.title('Repeat Number Frequency')
plt.xlabel('Repeat Number')
plt.ylabel('Frequency')
#plt.show()
plt.savefig(f'../output/frequencyimg.png')

# 生成汇总表格
# 排除 marker, no result, contamination
lane_objects = [lane for lane in lane_objects if lane.m_category == "sample" and lane.m_homoORheter not in ["no result", "contamination"]]
# 排序
lane_objects.sort(key=lambda x: x.m_MW)

# 生成汇总表格
summary = pd.DataFrame(columns=["File", "Lane #", "MW", "RepeatNum", "HomoOrHeter"])

for lane in lane_objects:
    summary = pd.concat([
        summary, pd.DataFrame({
            "File": [lane.m_filename],
            "Lane #": [lane.m_laneID],
            "MW": [lane.m_MW],
            "RepeatNum": [lane.m_repeatNum],
            "HomoOrHeter": [lane.m_homoORheter]
        })
    ],
    ignore_index=True)

# 统计同源和异源的数量
nums = summary["HomoOrHeter"].value_counts()
print(nums)

# 导出 CSV 文件
summary.to_csv(r"..\data\summary.csv", index=False)
print(summary)

length = 45
imgcount = 0
for i in range(0, 4):
    # 选择 m 到 n 行数据
    m = i * length + 1
    n = m + length
    selected_summary = summary.iloc[m - 1:n]

    # 修改 Scatter Plot 部分
    plt.figure(figsize=(10, 6))

    # 定义一个颜色映射以区分同源和异源
    color_mapping = {'homo': 'blue', 'heter': 'orange'}

    # 遍历 selected_summary 中的每一行
    for index, row in selected_summary.iterrows():
        # 获取文件名和泳道号
        filename_lane = f"{row['File']} - Lane {row['Lane #']}"

        # 遍历 RepeatNum 列表中的每个值
        for i, repeat_num in enumerate(row['RepeatNum']):
            # 根据同源或异源选择颜色
            color = color_mapping[row['HomoOrHeter']]

            # 绘制 Scatter Plot
            plt.scatter(index - m + 1, repeat_num, label=filename_lane, color=color, marker='o')

    # 设置横轴刻度标签
    plt.xticks(range(len(selected_summary)))

    # 添加标签和标题
    plt.xlabel('Sample - Lane')
    plt.ylabel('RepeatNum')
    plt.title(f'Selected DNA Fingerprint Lanes (Rows {m} to {n})')

    # 添加图例
    #plt.legend()

    # 显示图形
    #plt.show()

    # 保存图形为图片文件（例如PNG），使用不同的文件名
    plt.savefig(f'../output/result{imgcount + 1}.png')
    imgcount = imgcount + 1