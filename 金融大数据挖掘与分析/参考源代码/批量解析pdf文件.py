
import pdfplumber
import os

# 1.遍历文件夹中的所有PDF文件
file_dir = r'C:\Users\Administrator\Desktop\演示文件夹'
file_list = []
for files in os.walk(file_dir):  # 遍历该文件夹及其里面的所有子文件夹
    for file in files[2]:  #files[0]:母文件夹路径信息；files[1]:各个子文件夹路径信息；files[2]:母文件夹和子文件夹里面的各个文件信息（文件名）
        if os.path.splitext(file)[1] == '.pdf' or os.path.splitext(file)[1] == '.PDF':
            file_list.append(file_dir + '\\' + file)  #file：文件名字符串
print(file_list)

# 2.PDF文本解析和内容筛选
pdf_all = []
for i in range(len(file_list)):
    pdf = pdfplumber.open(file_list[i])
    pages = pdf.pages
    text_all = []
    for page in pages:  # 遍历pages中每一页的信息
        text = page.extract_text()  # 提取当页的文本内容
        text_all.append(text)  # 通过列表.append()方法汇总每一页内容
    text_all = ''.join(text_all)  # 把列表转换成字符串
    # print(text_all)  # 打印全部文本内容
    pdf.close()


    # 通过正文进行筛选
    # text_all已经是字符串
    if ('自有' in text_all) or ('议案' in text_all) or ('理财' in text_all) or ('现金管理' in text_all):
        pdf_all.append(file_list[i])
print(pdf_all)  # 打印筛选后的PDF列表

# 3.筛选后文件的移动
for pdf_i in pdf_all:
    newpath = 'C:\\Users\\Administrator\\Desktop\\筛选后的文件夹\\' + pdf_i.split('\\')[-1]  # 筛选后的文件夹一定要提前创建好！
    os.rename(pdf_i, newpath)  # 执行移动（剪切粘贴）操作

print('PDF文本解析及筛选完毕！')
