import requests
import re
import time
import pymysql

headers= {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'}



#搜狗新闻数据爬取
def sogou(company,page):
    url='https://www.sogou.com/sogou?query='+company+'&interation=1728053249&pid=sogou-wsse-9fc36fa768a74fa9&page='+str(page)
    res=requests.get(url,headers=headers,timeout=10).text

    #正则提取：网址、标题、信息源、日期
    p_href = '<a id="sogou_vr_.*?" target="_blank"  cacheStrategy="qcr:-1" href="(.*?)"'
    p_title = '<a id="sogou_vr_.*?" target="_blank"  cacheStrategy="qcr:-1" href=".*?">(.*?)</a>'
    p_source = '<p class="news-from text-lightgray">.*?<span>(.*?)</span>'
    p_date = '<p class="news-from text-lightgray">.*?</span><span>(.*?)</span>'
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)
    source = re.findall(p_source, res, re.S)
    date = re.findall(p_date, res, re.S)

    #数据清洗和打印输出
    for i in range(len(title)):
        title[i] = re.sub('<em><!--red_beg-->', '', title[i])
        title[i] = re.sub('<!--red_end--></em>', '', title[i])
        href[i] = 'https://www.sogou.com' + href[i]

        # print(str(i+1)+'.'+title[i]+'('+date[i]+'-'+source[i]+')'+'\n')
        # print(href[i]+'\n')



    #导出数据
    if page==1:
        flag='w' #写入第一页数据，覆盖之前的所有数据
    else:
        flag='a' #写入后续页数数据，增加不覆盖
    file1=open('C:\\Users\\Administrator\\Desktop\\'+company+'数据挖掘报告.txt',flag)  #a:write'增加'；w：write'覆盖'
    file1.write(company+'第'+str(page)+'页数据爬取成功:'+'\n'+'\n')
    for i in range(len(title)):
        file1.write(str(i+1)+'.'+title[i]+'('+date[i]+'-'+source[i]+')'+'\n')
        file1.write(href[i]+'\n')
    file1.write('-----------------------------------'+'\n'+'\n')
    file1.close()



companys=['阿里巴巴','万科','百度','腾讯','京东']
while True:
    for company in companys:
        try:
            for i in range(3):
                try:
                    sogou(company,i+1)
                    print('第'+str(i+1)+'页爬取成功')
                except:
                    print('第'+str(i+1)+'页爬取失败')
            print(company + '爬取并存入数据库成功')
        except:
            print(company + '爬取并存入数据库失败')

    time.sleep(10800)  #每隔3小时爬取一次


#新浪财经新闻数据爬取
def xinlang(company,page):
    url='https://search.sina.com.cn/news?q='+company+'&c=news&range=all&size=10&dpc=0&ps=0&pf=0&page='+str(page)
    res=requests.get(url,headers=headers,timeout=10).text

    #正则提取：网址、标题、信息源、日期
    p_href = '<h2>.*?<a href="(.*?)" target="_blank">'
    p_title = '<h2>.*?<a href=".*?" target="_blank">(.*?)</a>'
    p_info = '<span class="fgray_time">(.*?)</span>'
    href = re.findall(p_href, res, re.S)
    title = re.findall(p_title, res, re.S)
    info = re.findall(p_info, res, re.S)

    #数据清洗和打印输出
    source = []
    date = []
    for i in range(len(title)):
        title[i] = re.sub("<font color='red'>", '', title[i])
        title[i] = re.sub("</font>", '', title[i])
        source.append(info[i].split(' ')[0])
        date.append(info[i].split(' ')[1])



    #导出数据
    if page==1:
        flag='w' #写入第一页数据，覆盖之前的所有数据
    else:
        flag='a' #写入后续页数数据，增加不覆盖
    file1=open('C:\\Users\\Administrator\\Desktop\\'+company+'数据挖掘报告.txt',flag)  #a:write'增加'；w：write'覆盖'
    file1.write(company+'第'+str(page)+'页数据爬取成功:'+'\n'+'\n')
    for i in range(len(title)):
        file1.write(str(i+1)+'.'+title[i]+'('+date[i]+'-'+source[i]+')'+'\n')
        file1.write(href[i]+'\n')
    file1.write('-----------------------------------'+'\n'+'\n')
    file1.close()



companys=['阿里巴巴','万科','百度','腾讯','京东']
while True:
    for company in companys:
        try:
            for i in range(3):
                try:
                    xinlang(company,i+1)
                    print('第'+str(i+1)+'页爬取成功')
                except:
                    print('第'+str(i+1)+'页爬取失败')
            print(company + '爬取并存入数据库成功')
        except:
            print(company + '爬取并存入数据库失败')

    time.sleep(10800)  #每隔3小时爬取一次