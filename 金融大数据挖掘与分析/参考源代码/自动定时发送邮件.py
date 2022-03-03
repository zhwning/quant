
import smtplib  # 引入两个控制邮箱发送邮件的库
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pymysql
import time
import schedule


user = '781088605@qq.com'  # 发件人邮箱
pwd = 'umymtkjonklgbche'  # 781088605@qq.com：'umymtkjonklgbche' ;zhwning8804@163.com：'FBLTQEEHKLZUDNMB'
to = 'zhwning8804@163.com'  # 可以设置多个收件人，英文逗号隔开，如：'***@qq.com, ***@163.com'


def send_email():
    # 设置一个可以添加正文和附件的msg
    msg = MIMEMultipart()
    #正文引言
    mail_msg = []
    mail_msg.append('<p style="margin:0 auto">尊敬的小主，您好，以下是今天的舆情监控报告，望查阅：</p>')  # style="margin:0 auto"用来调节行间距

    # 1.连接数据库，提取所有相关公司的新闻信息，编写邮件正文内容
    db = pymysql.connect(host='localhost', port=3306, user='root', password='', database='pachong', charset='utf8')
    cur = db.cursor()  # 获取会话指针，用来调用SQL语句

    today = time.strftime("%Y-%m-%d")  # 这边采用标准格式的日期格式
    companys = ['阿里巴巴', '万科', '百度集团','腾讯','京东']
    N=1
    for company in companys:
        sql = 'SELECT * FROM article WHERE company = %s AND date = %s'
        cur.execute(sql, (company,today))
        data = cur.fetchall()  # 提取所有数据，并赋值给data变量，data为元组

        mail_msg.append('<p style="margin:0 auto"><b>'+ str(N) + '.' + company +'舆情报告</b></p>')  # 加上<b>表示加粗
        N += 1
        for i in range(len(data)):
            href = '<p style="margin:0 auto"><a href="' + data[i][2] + '">' + str(i + 1) + '.' + data[i][1] + '</a></p>'
            mail_msg.append(href)

    cur.close()  # 关闭会话指针
    db.close()  # 关闭数据库链接

    #正文署名
    mail_msg.append('<br>')  # <br>表示换行
    mail_msg.append('<p style="margin:0 auto">祝好</p>')
    mail_msg.append('<p style="margin:0 auto">小猿</p>')
    mail_msg = '\n'.join(mail_msg)
    # print(mail_msg)

    msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))


    # 2.再添加附件
    att1 = MIMEText(open('舆情报告.docx', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 下面的filename是在邮件中显示的名字及后缀名
    att1.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', '舆情报告.docx'))
    msg.attach(att1)


    # 3.设置邮件主题、发件人、收件人
    msg['Subject'] = 'test'  # 邮件的标题
    msg['From'] = user  # 设置发件人
    msg['To'] = to  # 设置收件人

    # 4.发送邮件
    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    s.login(user, pwd)
    s.send_message(msg)  # 发送邮件
    s.quit()  # 退出邮箱服务
    print('Success!')


schedule.every().day.at('17:00').do(send_email)
while True:
    schedule.run_pending()
    time.sleep(10)

