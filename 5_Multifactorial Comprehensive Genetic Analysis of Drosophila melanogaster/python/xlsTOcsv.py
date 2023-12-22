import os
import pandas as pd

#  complain about the data format.
#  I don't know what the statistics teacher's fucking mind looks like.
#  Why are the formats of the data statistics different twice?
#  Once, the statistics are in different worksheets of the same Excel file,
#  and the other time, they are in different Excel files. It's frustrating.
file_f1 = '../data/Genetics Experiment F1 Data Compilation for Fall 2023.xls'
filedir_f2 = '../data/f2/'
outputdir_f1 = './data/f1/'
outputdir_f2 = './data/f2/'

# f1
data_f1 = pd.ExcelFile(file_f1)
sheet_name_f1 = data_f1.sheet_names

for sheet in sheet_name_f1:
    df = data_f1.parse(sheet)
    output_file = f'{outputdir_f1}data_{sheet}.csv'
    df.to_csv(output_file, index=False)

data_f1.close()

csv_files = [
    file for file in os.listdir(outputdir_f1) if file.endswith('.csv')
]

for file_name in csv_files:
    file_path = os.path.join(outputdir_f1, file_name)
    df = pd.read_csv(file_path)
    if file_name == "data_全体汇总.csv":
        df = df.iloc[0:, 2:]
    else:
        df = df.iloc[0:-2, 4:]
    df.to_csv(file_path, index=False, header=False)


import os
import csv

def remove_empty_rows(csv_file):
    with open(csv_file, 'r', newline='') as file:
        rows = [row for row in csv.reader(file) if any(field.strip() for field in row)]

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            remove_empty_rows(file_path)

# 指定目录路径
directory_path = './data/f1/'

# 处理目录下所有CSV文件
process_files_in_directory(directory_path)


# f2
datas_f2 = [
    file for file in os.listdir(filedir_f2) if file.endswith('.xls')
]

for data in datas_f2:
    data_f2 = pd.ExcelFile(os.path.join(filedir_f2, data))
    sheet_name_f2 = data_f2.sheet_names
    for sheet in sheet_name_f2:
        df = data_f2.parse(sheet)
        file_name = os.path.splitext(data)[0]
        sheet_directory = os.path.join(outputdir_f2, file_name)

        if not os.path.exists(sheet_directory):
            os.makedirs(sheet_directory)

        output_file = os.path.join(sheet_directory, f'{sheet}.csv')
        df.to_csv(output_file, index=False)
