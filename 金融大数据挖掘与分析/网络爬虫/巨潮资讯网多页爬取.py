
from selenium import webdriver
import re
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=理财'
browser.get(url)
time.sleep(3)
data = browser.page_source
p_count = '<span class="total-box" style="">约(.*?)条'
count = re.findall(p_count, data)[0]  # 获取公告个数，注意这里要加一个[0],因为findall返回的是一个列表
if type(int(count)/10) == float:
    pages = int(int(count)/10)       #总页数为浮点数(n.。。。)，需要翻页n（第一页不算）
else:
    pages = int(int(count)/10) - 1   #总页数为整数n，需要翻页n-1（第一页不算）

# 1.自动翻页获取源码源代码
datas = []
datas.append(data)  # 这边是把第一页源代码先放到datas这个列表里
for i in range(1):  # 这边为了演示改成了range(1)，想爬全部的话改成range(pages)
    browser.find_element_by_xpath('//*[@id="fulltext-search"]/div/div[1]/div[2]/div[4]/div[2]/div/button[2]').click()
    time.sleep(2)
    data = browser.page_source
    datas.append(data)
    time.sleep(1)

alldata = "".join(datas)
browser.quit()

# 2.编写正则表达式
p_title = '<span title="" class="r-title">(.*?)</span>'
p_href = 'class="el-table_1_column_2.*?<a target="_blank" href="(.*?)" data-id='
p_date = 'class="el-table_1_column_3 is-left.*?<span class="time">(.*?)</span>'
title = re.findall(p_title, alldata)
href = re.findall(p_href, alldata)
date = re.findall(p_date, alldata, re.S)  # 注意(.*?)中有换行（/n），而常规的(.*?)匹配不了换行，所以需要加上re.S取消换行的影响


# 3.清洗数据
for i in range(len(title)):
    title[i] = re.sub('<.*?>', '', title[i])
    href[i] = 'http://www.cninfo.com.cn' + href[i]
    href[i] = re.sub('amp;', '', href[i])
    date[i] = date[i].strip()
    date[i] = date[i].split(' ')[0]


# 4.自动筛选
for i in range(len(title)):
    if '2020' in date[i] or '2021' in date[i]:  # 筛选2020和2021年的，可以自己调节
        title[i] = title[i]
        href[i] = href[i]
        date[i] = date[i]
    else:
        title[i] = 'd'     #赋值为'd'而不是'',避免字段为空的数据被误删（比如date本身为空）
        href[i] = 'd'
        date[i] = 'd'
while 'd' in title:
    title.remove('d')
while 'd' in href:
    href.remove('d')
while 'd' in date:
    date.remove('d')

'''利用同样的思路，我们也能对标题进行清洗，如果该标题里还有某些不想要的关键词，比如说“保底”、“刚兑”等关键词，我们就把它赋值然后删掉'''
for i in range(len(title)):
    if '保底' in title[i] or '刚兑' in title[i]:
        title[i] = 'd'
        href[i] = 'd'
        date[i] = 'd'
    # else:
    #     title[i] = title[i]
    #     href[i] = href[i]
    #     date[i] = date[i]
while 'd' in title:
    title.remove('d')
while 'd' in href:
    href.remove('d')
while 'd' in date:
    date.remove('d')

for i in range(len(title)):
    print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
    print(href[i])



# #5.自动批量爬取PDF - 选择默认储存位置
# for i in range(len(href)):
#     browser = webdriver.Chrome()
#     browser.get(href[i])
#     try:
#         browser.find_element_by_xpath('//*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button').click()
#         time.sleep(5)  # 这个一定要加，因为下载需要一点时间
#         browser.quit()
#         print(str(i+1) + '.' + title[i] + '下载完毕')
#     except:
#         print(title[i] + '不是PDF文件')


#  补充1：无界面浏览器设置（通过后台不打开浏览器的方式，无法下载）
# for i in range(len(href)):
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--headless')
#     browser = webdriver.Chrome(options=chrome_options)
#     browser.get(href[i])
#     try:
#         browser.find_element_by_xpath('//*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button').click()
#         time.sleep(5)  # 这个一定要加，因为下载需要一点时间
#         browser.quit()
#         print(str(i+1) + '.' + title[i] + '下载完毕')
#     except:
#         print(title[i] + '不是PDF文件')


# 补充2：自动批量爬取PDF - 自己设定储存位置
# for i in range(len(href)):
#     chrome_options = webdriver.ChromeOptions()
#     prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\Users\\Administrator\\Desktop\\公告'} #可以自定义文件储存的位置
#     chrome_options.add_experimental_option('prefs', prefs)
#     browser = webdriver.Chrome(options=chrome_options)
#     browser.get(href[i])
#     try:
#         browser.find_element_by_xpath('//*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button').click()
#         time.sleep(3) # 这个一定要加，因为下载需要一点时间
#         print(str(i+1) + '.' + title[i] + '下载完毕')
#         browser.quit()
#     except:
#         print(title[i] + '不是PDF')