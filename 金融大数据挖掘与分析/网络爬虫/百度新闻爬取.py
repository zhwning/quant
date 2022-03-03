
import requests
import re
import time
import datetime
import pymysql

headers= {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'}



def baidu(company, page):
    # 1.按时间顺序获取网页源代码：
    n=(page-1)*10  #网页数num（第一页：0*10；第二页：1*10...）
    url='https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd='+company+'&pn='+str(n)   #rtt=1:按焦点排序；rtt=4:按时间排序;
    res=requests.get(url,headers=headers,timeout=10).text

    #2.编写正则表达式提取内容
    p_href='<h3 class="news-title_1YtI1"><a href="(.*?)"'
    p_title='class="news-title-font_1xS-F" aria-label="标题：(.*?)"'
    p_info='<span class="c-color-gray c-font-normal c-gap-right" aria-label="(.*?)</div>'
    href=re.findall(p_href,res,re.S)
    title=re.findall(p_title,res,re.S)
    info=re.findall(p_info,res,re.S)

    #3.数据清洗
    source=[]
    date=[]
    for i in range(len(title)):
        #3.1数据初步清洗
        info[i] = re.sub('新闻来源：', '', info[i])
        info[i] = re.sub('</span>\n', '', info[i])
        info[i] = re.sub('</span>', '', info[i])
        info[i] = re.sub('>.*?>', '', info[i])
        info[i] = re.sub('>.*?\n', '', info[i])
        href[i] = re.sub('amp;','',href[i])
        source.append(info[i].split('"')[0])
        date.append(info[i].split('"')[1])

        #统一日期格式
        if('小时' in date[i]) or ('分钟' in date[i]) or('今天' in date[i]):
            date[i] = time.strftime("%Y-%m-%d")
        elif('昨天' in date[i]):
            date[i] = (datetime.date.today() + datetime.timedelta(days = -1)).strftime("%Y-%m-%d")
        elif ('前天' in date[i]):
            date[i] = (datetime.date.today() + datetime.timedelta(days = -2)).strftime("%Y-%m-%d")
        elif ('天前' in date[i]):
            date[i] = (datetime.date.today() + datetime.timedelta(-int(date[i][0]))).strftime("%Y-%m-%d")
        elif ('年' not in date[i]) and ('月' in date[i]) and ('日' in date[i]):
            date[i] = date[i].split(' ')[0]
            date[i] = re.sub('月', '-', date[i])
            date[i] = re.sub('日', '', date[i])
            date[i] = time.strftime("%Y") +'-' + date[i]
            #转标准格式
            a = datetime.datetime.strptime(date[i], '%Y-%m-%d')
            b = datetime.datetime.date(a)
            date[i] = str(b)
        elif ('年' in date[i]) and ('月' in date[i]) and ('日' in date[i]):
            date[i] = date[i].split(' ')[0]
            date[i] = re.sub('年','-',date[i])
            date[i] = re.sub('月','-',date[i])
            date[i] = re.sub('日','',date[i])
            # 转标准格式
            a = datetime.datetime.strptime(date[i], '%Y-%m-%d')
            b = datetime.datetime.date(a)
            date[i] = str(b)
        else :
            date[i] = date[i]

        #3.2数据深度清洗：删除不相关数据
        try:
            article = requests.get(href[i],headers=headers,timeout=10).text
        except:
            article = '爬取失败'

        #解决article乱码问题（以防万一）
        try:
            article = article.encode('ISO-8859-1').decode('utf-8')
        except:
            try:
                article = article.encode('ISO-8859-1').decode('gbk')
            except:
                article = article

        company_re = company[0] +'.{0,9}' +company[-1]
        if len(re.findall(company_re,article)) < 1:
            title[i]='delete'
            href[i]='delete'
            date[i]='delete'
            source[i]='delete'

    while 'delete' in title:
        title.remove('delete')
    while 'delete' in href:
        href.remove('delete')
    while 'delete' in date:
        date.remove('delete')
    while 'delete' in source:
        source.remove('delete')


    #4.建立舆情数据评分字段
    score=[]
    keywords=['违约','诉讼','兑付','破产','负面','糟糕','恶化','阿里','腾讯']
    for i in range(len(title)):
        num = 0
        try:
            article = requests.get(href[i], headers=headers, timeout=10).text
        except:
            article = '爬取失败'

        # 解决article乱码问题（以防万一）
        try:
            article = article.encode('ISO-8859-1').decode('utf-8')
        except:
            try:
                article = article.encode('ISO-8859-1').decode('gbk')
            except:
                article = article

        #只取网页正文段落
        p_article = '<p>(.*?)</p>'
        article_main = re.findall(p_article,article)
        article = ''.join(article_main)

        #评分机制
        for j in keywords:
            if (j in article) or (j in title[i]):
                num -= 5
        score.append(num)

    #此处可根据爬取到的某些关键词或者股价数据低于某个临界值，设定立即发送邮件，else:正常定时发送

    # #5.导出数据到txt文件或打印输出
    # if page==1:
    #     flag='w' #写入第一页数据，覆盖之前的所有数据
    # else:
    #     flag='a' #写入后续页数数据，增加不覆盖
    # file1=open('C:\\Users\\Administrator\\Desktop\\'+company+'数据挖掘报告.txt',flag)  #a:write'增加'；w：write'覆盖'
    # file1.write(company+'第'+str(page)+'页数据爬取成功:'+'\n'+'\n')
    # for i in range(len(title)):
    #     try:
    #         file1.write(str(i+1)+'.'+title[i]+'('+date[i]+' '+source[i]+')'+'\n')
    #         file1.write(href[i]+'\n')
    #         file1.write(company+'该条舆情评分为：'+str(score[i])+'\n\n')
    #     except:
    #         print('%s第%d页第%d条数据导入txt失败'%(company,page,i+1))
    #
    # file1.write('-----------------------------------'+'\n'+'\n')
    # file1.close()

    #6.导入数据到mysql及数据去重
    for i in range(len(title)):
        db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
        cur = db.cursor()  #获取会话指针，调用SQL语句

        #6.1查询数据
        sql_1='select * from article where company = %s'
        cur.execute(sql_1,company)
        data_all=cur.fetchall()
        title_all=[]
        for j in data_all:
            title_all.append(j[1])

        #6.2判断爬取到的数据是否已在数据库中，不在则导入数据库
        if title[i] not in title_all:
            sql_2='insert into article(company,title,href,date,source,score) values (%s,%s,%s,%s,%s,%s)'
            cur.execute(sql_2,(company,title[i],href[i],date[i],source[i],score[i]))
            db.commit()
        cur.close()
        db.close()




#7.批量爬取多家公司的新闻数据
companys=['阿里巴巴','万科','百度集团','腾讯','京东']
while True:
    for company in companys:
        try:
            for i in range(3):
                try:
                    baidu(company,i+1)
                    print(company+'第'+str(i+1)+'页爬取成功')
                except:
                    print(company+'第'+str(i+1)+'页爬取失败')
            print(company + '数据爬取并存入数据库成功')
        except:
            print(company + '数据爬取并存入数据库失败')

    time.sleep(10800)  #每隔3小时爬取一次











