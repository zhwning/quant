# 1.下载CSV数据文件
import requests
# url = 'http://search.worldbank.org/api/projects/all.csv'
# res = requests.get(url)  # 只要能够获得下载链接，像Excel文件、图片文件都可以进行下载
# file = open('世界银行项目表.csv', 'wb')  # 可以修改所需的文件保存路径，这里得选择wb二进制的文件写入方式
# file.write(res.content)
# file.close()  # 通过close()函数关闭open()函数打开的文件，有助于释放内存，是个编程的好习惯
# print('世界银行项目表.csv下载完毕')

#通过pandas直接获取表格
import pandas as pd
pd.set_option('display.max_columns',None)

url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml'  # 新浪财经数据中心提供股票大宗交易的在线表格
table = pd.read_html(url)[0]  # 通过pd.read_html(url)获取的是一个列表，所以仍需通过[0]的方式提取列表的第一个元素
print(table)


table.to_excel('大宗交易表2.xlsx',index=False,)  # 如果想忽略行索引的话，可以设置index参数为False
print('获取表格成功！')


#和讯网研报获取（和讯网反爬能力强）
import pandas as pd
from selenium import webdriver
import re
chrome_options=webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)


data_all = pd.DataFrame()  # 创建一个空列表用来汇总所有表格信息
for pg in range(1, 3):  # 可以将页码调大
    url = 'http://yanbao.stock.hexun.com/listnews1_' + str(pg) + '.shtml'
    browser.get(url)  # 通过Selenium访问网站
    data = browser.page_source  # 获取网页源代码
    table = pd.read_html(data)[0]  # 通过pandas库提取表格

    # print(table)
    # 如果上面打印的table里的表头有问题，则需要使用如下代码将第一行为表头，然后从第二行开始取数
    # table.columns = table.iloc[0]  # 将原来的第一行内容设置为表头
    # table = table.iloc[1:]  # 改变表格结构，从第二行开始选取

    # 添加股票代码信息
#     p_code = '<a href="yb_(.*?).shtml'
#     code = re.findall(p_code, data)
#     table['股票代码'] = code
#
    # 通过concat()函数纵向拼接成一个总的DataFrame
    data_all = pd.concat([data_all, table], ignore_index=True)

browser.quit()
print(data_all)
print('分析师评级报告获取成功')
data_all.to_excel('分析师评级报告_new.xlsx')

