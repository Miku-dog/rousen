import re
import pandas as pd
# 读取CSV文件
df = pd.read_csv('BV1Qh411L7ES.csv')

# 循环遍历每一行
filtered_rows = []
for index, row in df.iterrows():
    # 检查第二列的值是否为空
    if pd.isnull(row[df.columns[1]]) or pd.isnull(row[df.columns[0]]):
        continue  # 如果为空，跳过该行
    else:
        # 将第一列和第二列的内容作为元组加入列表
        filtered_rows.append((row[df.columns[0]], row[df.columns[1]]))

# 分别获取第一列和第二列的内容
first_column, second_column = zip(*filtered_rows)
# 转换为列表
first_column = list(first_column)
second_column = list(second_column)
for i in range(len(first_column)):
    a = re.sub(r"\[.*?\]", "", first_column[i])
    a = re.sub(r".*:", "", a)
    first_column[i] = re.sub(r"@\w+ ", "", a)
    b = re.sub(r"\[.*?\]", "", second_column[i])
    b = re.sub(r".*:", "", b)
    second_column[i] = re.sub(r"@\w+ ", "", b)

# 原始评论
comment = "回复 @Orange_tiger :[脱单doge][脱单doge][脸红]"

# 移除表情图片和回复内容
cleaned_comment = re.sub(r"\[(?:\w+)?\]", "", comment)
cleaned_comment = re.sub(r"回复 @\w+ :", "", cleaned_comment)



sub_list = []
for i in second_column:
    sub_comments = []
    sub = i.split('\t')
    sub_list.append(sub)
print(first_column)
print(sub_list)