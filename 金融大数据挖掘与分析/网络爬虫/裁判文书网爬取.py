

'''网页反爬设置，先登录再爬取'''

from selenium import webdriver
import time
browser = webdriver.Chrome()
browser.get('https://wenshu.court.gov.cn/')
browser.find_element_by_xpath('//*[@id="loginLi"]/a').click() #点击登录

# browser.get('https://wenshu.court.gov.cn/website/wenshu/181010CARHS5BS3C/index.html?open=browser')
browser.maximize_window()

time.sleep(5)

try:
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/div/div/input').clear()  # 清空'手机号码'
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/div/div/input').send_keys('')  # 输入登录账号
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[2]/div/div/div/input').clear()  # 清空'密码'
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[2]/div/div/div/input').send_keys('')  # 输入登录密码
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[3]/span').click() #点击登录
except:
    browser.refresh()
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/div/div/input').clear()  # 清空'手机号码'
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/div/div/input').send_keys(
        '')  # 输入登录账号
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[2]/div/div/div/input').clear()  # 清空'密码'
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[2]/div/div/div/input').send_keys(
        '')  # 输入登录密码
    browser.find_element_by_xpath('//*[@id="root"]/div/form/div/div[3]/span').click()  # 点击登录


browser.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[2]/input').clear()  # 清空原搜索框
browser.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[2]/input').send_keys('房地产')  # 在搜索框内模拟输入'房地产'三个字
browser.find_element_by_xpath('//*[@id="_view_1540966814000"]/div/div[1]/div[3]').click()  # 点击搜索按钮
time.sleep(10)
data = browser.page_source
browser.quit()
print(data)

