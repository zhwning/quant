#8.汇总每日评分
import time
import datetime
import pymysql
import pandas as pd

companys=['阿里巴巴','万科','百度集团','腾讯','京东']
today = time.strftime("%Y-%m-%d")
# today = (datetime.date.today() + datetime.timedelta(days = -1)).strftime("%Y-%m-%d")
for company in companys:
    score=100
    db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
    cur = db.cursor()

    sql = 'select score from article where company = %s and date = %s'
    cur.execute(sql,(company,today))
    data = cur.fetchall()   #每一条数据放入小元组，所有数据构成大元组
    for i in range(len(data)):
        score += data[i][0]
    print(company+'的今日舆情评分为：'+str(score))

    cur.close()
    db.close()



#9.遍历数据库获取日期和评分

company='阿里巴巴'
date_list=list(pd.date_range('2021-09-01','2021-09-30')) #以列表格式存放的'时间格式'数据
for i in range(len(date_list)):
    date_list[i] = datetime.datetime.strftime(date_list[i],'%Y-%m-%d') #时间格式转字符串格式


db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
cur = db.cursor()
sql = 'select score from article where company = %s and date = %s'

score_list={} #取出的每日评分和放入字典
for d in date_list:
    cur.execute(sql,(company,d))
    data = cur.fetchall()   #每一条数据放入小元组，所有数据构成大元组
    score = 100
    for i in range(len(data)):
        score += data[i][0]
    # print(company+'的今日舆情评分为：'+str(score))
    score_list[d]=score

cur.close()
db.close()


#10.数据可视化
import datetime
import pandas as pd
import matplotlib.pyplot as plt


# 设置中文格式为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
data = pd.read_excel('data.xlsx')

#  把日期由string字符串格式转为timestamp时间戳格式，方便坐标轴显示
d = []
for i in range(len(data)):
    d.append(datetime.datetime.strptime(data['date'][i], '%Y-%m-%d'))
data['date'] = d  # 将原来的date那一列数据换成新生成的时间戳格式日期


#  数据可视化并设置双坐标轴
plt.plot(data['date'], data['score'], 'b--', label='分数')
plt.xticks(rotation=45)  # 设置x轴刻度显示角度
plt.legend(loc=2)  # 分数的图例设置在左上角
plt.twinx()  # 设置双坐标轴（x轴用两次）
plt.plot(data['date'], data['price'], 'r-', label='价格')
plt.xticks(rotation=45)
plt.legend(loc=1)
plt.show()


#11.用IP代理爬取
import requests
from selenium import webdriver
import re



# 讯代理官网：http://www.xdaili.cn/；
proxy = requests.get('讯代理API（需花钱买）').text
proxy = proxy.strip()  # 这一步非常重要，因为要把看不见的换行符等给清除掉
print(proxy)
proxies = {"http": "http://"+proxy, "https": "https://"+proxy}
url = 'https://httpbin.org/get'   #查看本机IP，验证是否代理成功
res = requests.get(url, proxies=proxies).text
print(res)


# selenium库使用IP代理
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--proxy-server=http://" + proxy)
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(options=chromeOptions)
browser.get("http://httpbin.org/ip")
print(browser.page_source)
browser.quit()

#12.用selenium库中的模拟浏览器爬取经过渲染的或者反爬虫处理的网页（常规requests.get()爬取不到）
chrome_op=webdriver.ChromeOptions()
chrome_op.add_argument('--headless--')
browser=webdriver.Chrome(options=chrome_op)
browser.get('http://finance.sina.com.cn/realstock/company/sh000001/nc.shtml')  #爬取新浪财经上证综指
data=browser.page_source
# print(data)
browser.quit()

p_price='<div id="price" class=".*?">(.*?)</div>'
price=re.findall(p_price,data)
print(price)







