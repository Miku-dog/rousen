import csv
from datetime import date
import requests
from bs4 import BeautifulSoup
Headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
response = requests.get('https://www.bilibili.com/v/popular/rank/bangumi/',headers=Headers)
print(response)
html=response.text
soup=BeautifulSoup(html,"html.parser")
all_title=soup.findAll(attrs={'class':"title"})
all_shuju=soup.findAll(attrs={'class':"detail-state"})
fanming=[]
biaoxian=[]
for i in all_title:
    fanming.append(i.text)
for j in all_shuju:
    j=j.text
    j = j.replace(' ', '')
    j = j.split('\n')
    for s in j:
        if s == '':
            j.remove(s)
    b=[]
    for a in j:
        if a[-1] == '亿':
            a=float(a[0:-1])*10000
            b.append(a)
        elif a[-1] == '万':
            a=float(a[0:-1])
            b.append(a)
        else:
            a=float(a)/10000
            b.append(a)
    biaoxian.append(b)
print("播放量（万）")
for i in range(len(biaoxian)):
     print(f"{fanming[i]}"+'\n'+f'{biaoxian[i][0]}'+'\t'+f'{biaoxian[i][1]}')
#写文件

data1=[]
for s in range(50):
    data=[]
    data.append(fanming[s])
    data.append(biaoxian[s][0])
    data.append(biaoxian[s][1])
    data1.append(data)
today = date.today()
with open (r'C:\Users\Rousen\数据可视化\202012903718石志滨\dark♂作业\DATA\{}.csv'.format(today), 'w', encoding='utf-8', newline='') as file_csv:
    writer=csv.writer(file_csv)
    writer.writerow(['番名','播放量(万)','追番人数(万)'])
    writer.writerows(data1)
