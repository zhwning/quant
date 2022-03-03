from selenium import webdriver
import re


def dongfang(company):
    chrome_op = webdriver.ChromeOptions()
    chrome_op.add_argument('--headless--')
    browser = webdriver.Chrome(options=chrome_op)
    url = 'https://so.eastmoney.com/news/s?keyword='+company+'&type=title&sort=time' #sort:time/relate;type:title/content
    browser.get(url)
    data = browser.page_source
    browser.quit()

    p_title = '<div class="news_item_t"><a href=".*?">(.*?)</a>'
    p_href = '<div class="news_item_t"><a href="(.*?)" target="_blank">.*?</a>'
    p_date = '<span class="news_item_time">(.*?)</span>'
    title = re.findall(p_title, data)
    href = re.findall(p_href, data)
    date = re.findall(p_date, data, re.S)

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        date[i] = date[i].split(' ')[0]
        print(str(i+1) + '.' + title[i] + ' - '+ date[i])
        print(href[i])



companys = ['阿里巴巴', '恒大', '京东', '万科']
for i in companys:
    try:
        dongfang(i)
        print(i + '东方财富网爬取成功')
    except:
        print(i + '东方财富网爬取失败')


