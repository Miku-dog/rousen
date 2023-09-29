import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time

url = 'https://space.bilibili.com/94510621/video/'

def get_BV(url):
    path_BV = []
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    data = driver.page_source
    driver.close()
    soup = BeautifulSoup(data, 'html.parser')
    BVS = soup.find_all('li', attrs={"data-aid": True})
    for i in BVS:
        data_aid = i['data-aid']
        path_BV.append(data_aid)
    return path_BV

def speaker_get(path_BV):
    URL_comments = []
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.bilibili.com/video/"+path_BV)
    target_url_prefix = "https://api.bilibili.com/x/v2/reply/wbi/main?"
    network = driver.execute_script("return window.performance.getEntries();")
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(8)
   #须保证评论加载成功，出现文件
    for data in network:
        if data["name"].startswith(target_url_prefix):
            URL_comments.append(data['name'])
            print("Found a matching URL:", data["name"])
    URL_comments = list(set(URL_comments))
    driver.close()
    print(URL_comments)
    return URL_comments

def parser_comment(url, folder_name, name):
    time.sleep(1)
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    data = requests.get(url, headers=head).json()
    if data['data']['replies']:
        for i in data['data']['replies']:
            dic = {}
            oid = i["oid"]
            root_id =i["rpid"]
            if i['replies']:
                dic["content"] = i["content"]["message"]
                print('父评论:', i["content"]["message"])
                sub_string = []
                url = f"https://api.bilibili.com/x/v2/reply/reply?oid={oid}&type=1&root={root_id}&pn=1"
                sub_data = requests.get(url, headers=head).json()
                for j in sub_data['data']['replies']:
                    sub = j["content"]["message"] + '\t'
                    sub_string.append(sub)
                print('子评论: ', sub_string)
                sub_string = ''.join(sub_string)
                dic['sub_content'] = sub_string
            file_path = os.getcwd()
            path = os.path.join(file_path, folder_name)
            if not os.path.exists(path):
                os.makedirs(path)
            #dic["oid"]=url.split("oid=")[-1].replace("&sort=2","")
            with open(f'./{folder_name}/{str(name)}.csv', 'a', encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(dic.values())

BV_LIST = []
BV_PATH = []
a = '730732'
for i in range(1,9):
    url = f'https://space.bilibili.com/{a}/video'
    url = url + '?pn=' + str(i)
    path_BV = get_BV(url)
    BV_LIST.append(path_BV)
for i in BV_LIST:
    for j in i:
        BV_PATH.append(j)
print(BV_PATH)
for i in BV_PATH:
    c = speaker_get(i)
    if c:
        parser_comment(c[0], a, i)
        print(f'{i}爬取成功')

# c = speaker_get('BV18j41117xg')
# if c:
#     parser_comment(c[0], 'BV18j41117xg')
#     print('爬取成功')

#https://api.bilibili.com/x/v2/reply/reply?oid=872131372&type=1&root=180760980992&ps=10&pn=1&web_location=333.788



