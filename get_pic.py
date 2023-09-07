import requests
from bs4 import BeautifulSoup
import re
import os
Headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
url='https://www.bilibili.com/v/popular/rank/bangumi/'
def analysis(item,results):  #item为正则表达式，
    pattern = re.compile(item, re.I|re.M)
    result_list = pattern.findall(results)
    return result_list
def get_picture(url,Headers):
    response = requests.get(url, headers=Headers)
    html = response.text
    soup=BeautifulSoup(html, 'html.parser')
    titles = soup.findAll(attrs={'class': "title"})
    results = soup.find_all('script')  #爬取的图片类型为懒加载，通过调用资源文件找到代码
    image_dirty = str(results)    #将byte类型的数据转化为字符串，用于findall匹配
    urls = analysis(r'"cover":"(.*?)"',image_dirty)
    pictures=[]
    names=[]
    for i in range(0,2*len(titles),2):
        aa=urls[i].encode('utf-8').decode('unicode-escape')  #转化编码格式，
        pictures.append(aa)
    for j in range(len(titles)):
        names.append(titles[j].text)
    return pictures,names
pictures,names=get_picture(url,Headers)
print(pictures)
print(len(pictures))
print(len(names))

if not os.path.exists('picture'):
    os.makedirs('picture', exist_ok=True)
try:
    for i in range(len(names)):
        path='picture'
        response = requests.get(pictures[i], stream=True)
        path = os.path.join(path, names[i] + '.jpg')
        print(path)
        with open(path, 'wb') as fw:
            fw.write(response.content)
except:
    print('写入失败')


