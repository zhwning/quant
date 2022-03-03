import pdfplumber
import pandas as pd

#解析pdf所有页数文本内容
pdf=pdfplumber.open('公司A理财公告.PDF')
pages=pdf.pages #得到的pages是一个列表
text_all=[]
for i in pages:
    text=i.extract_text()  #得到的text是字符串
    text_all.append(text)
text_all=''.join(text_all)
print(text_all)
pdf.close()

#解析表格内容
pdf = pdfplumber.open('公司A理财公告.PDF')
pages = pdf.pages
page = pages[3]  # 因为表格在第四页，所以提取pages[3]
tables = page.extract_tables()  # 通过extract_tables方法获取该页所有表格，得到的tables是列表:1个元素
table = tables[0]  # 因为第四页只有一个表格，所以通过tables[0]提取，得到的table是嵌套列表结构：4个子列表元素

# 替换原来table中的换行符
for i in range(len(table)):  # 遍历大列表中的每一个子列表
    for j in range(len(table[i])):  # 遍历子列表中的每一个元素
        table[i][j] = table[i][j].replace('\n', '')  # 替换换行符
pd.set_option('display.max_columns', None)  # 显示全部列
df = pd.DataFrame(table[1:], columns=table[0])  # 得到的table是嵌套列表类型，转化成DataFrame更加方便查看和分析
print(df)
pdf.close()