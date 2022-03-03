
from selenium import webdriver
import re


def juchao(keyword):
    chrome_op = webdriver.ChromeOptions()
    chrome_op.add_argument('--headless--')
    browser = webdriver.Chrome(options=chrome_op)
    url = 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=' + keyword
    browser.get(url)
    data = browser.page_source
    # print(data)
    browser.quit()


    p_title = '<span title="" class="r-title">(.*?)</span>'
    p_href = '<a target="_blank" href="(.*?)" data-id='
    p_date = '<span class="time">(.*?)</span>'
    title = re.findall(p_title, data)
    href = re.findall(p_href, data)
    date = re.findall(p_date, data, re.S)  # 注意(.*?)中有换行（/n），而常规的(.*?)匹配不了换行，所以需要加上re.S取消换行的影响

    for i in range(len(title)):
        title[i] = re.sub('<.*?>', '', title[i])
        href[i] = re.sub('amp;', '', href[i])
        href[i] = 'http://www.cninfo.com.cn' + href[i]
        date[i] = date[i].strip()  # 清除空格和换行符
        date[i] = date[i].split(' ')[0]  # 只取“年月日”信息，不用“时分秒”信息
        print(str(i + 1) + '.' + title[i] + ' - ' + date[i])
        print(href[i])


keywords = ['理财', '现金管理', '纾困']
for i in keywords:
    try:
        juchao(i)
        print('巨潮网' + i + '爬取成功')
    except:
        print('巨潮网' + i + '爬取失败')
