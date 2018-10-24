#!/usr/bin/python
# -*- coding:utf-8 -*-

from numpy import *
import numpy as np
from os import listdir
import os
import pandas as pd
import requests

# 以下是爬取txt文本，保存到source文件夹中
data = pd.read_csv('middle_sample.csv')
os.mkdir('source')

urls = 'https://www.sec.gov/Archives/' + data['index']

for num, url in enumerate(urls):
    if url[-4:] == '.txt':
        text = requests.get(url).text

        fileName = ''
        for j in range(6):
            fileName += str(data.iloc[num][j]) + '-'
        fileName = 'source/' + fileName[:-1] + '.txt'
        file = open(fileName, 'w')
        file.write(text)
        file.close()

# 从一个文本中找出某个关键词本中段索引位置
# text为原文本，keyword为需要查找的关键词，返回关键词第一个字符串在原文本出现在的索引位置
def my_find(fileName, keyword):
    text = open('source/' + fileName).read()    # 打开文本并读取
    keyword_len = len(keyword)                  # 查找关键词的长度
    index_keyword = []                          # 新建空list，将用来存放关键词在文本中的索引位置

    for i in range(int(len(text) / keyword_len)):
        if text.find(keyword) != -1:            # 如果关键词keyword存在
            index_str = text.find(keyword)      # 在原文本中查找keyword中第一次出现在索引
            index_keyword.append(index_str)     # 并添加到空list中
            text = text[index_str + keyword_len:]   # 原本更新成keyword后面的文本字符，然后循环

    index_keyword_len = len(index_keyword)      # 算出keyword在文本中出现的次数

    if index_keyword_len == 0:                  # 如果index_keyword_len为0，即没有找到keyword
        print('在文件{}中未找到keyword'.format(fileName))
    else:
        new_index_keyword = zeros(index_keyword_len)    # 如果找到keyword，新建零list，将用于更新keyword中在原文本中真正的索引位置

    # 这是因为只有在index_keyword中的第一个索引是原文本中真正的索引位置，后面的索引位置对应的是
    # 删去前面一次keyword末尾之前的所有字符后的文本中下一个keyword的索引位置
    # 因此在index_keyword中第二个数字之后的索引值需要加上删掉的字符个数
        for i in range(index_keyword_len):
            if i == 0:
                new_index_keyword[i] = index_keyword[i]
            else:
                new_index_keyword[i] = index_keyword[i] + index_keyword[i - 1] + keyword_len
        index_keyword = []

    # 更新后的为一个float类型的数组，而由于索引必须为整数，以下是把索引数组的数值换成整数列表

        for i in range(len(new_index_keyword)):
            index_keyword.append(int(new_index_keyword[i]))

    return index_keyword

# 以下函数跟上面思路一致，不过下面这个函数是把原文本中的所有字符换成小写
def table_find(fileName, keyword):
    text = open('source/' + fileName).read()
    text = text.lower()     # 把原文本换成小写
    keyword_len = len(keyword)
    index_keyword = []
    for i in range(int(len(text) / keyword_len)):
        if text.find(keyword) != -1:
            index_str = text.find(keyword)
            index_keyword.append(index_str)
            text = text[index_str + keyword_len:]

    index_keyword_len = len(index_keyword)
    if index_keyword_len == 0:
        print('在文件{}中未找到Table'.format(fileName))
    else:
        new_index_keyword = zeros(index_keyword_len)
        out = zeros(index_keyword_len)

        for i in range(index_keyword_len):
            new_index_keyword[i] = index_keyword[i]

        for i in range(len(new_index_keyword)):
            out[i] = sum(new_index_keyword[:i + 1]) + keyword_len * (i)

        index_keyword = []

        for i in range(len(out)):
            index_keyword.append(int(out[i]))

    return index_keyword


# 主函数
# 以下程序的作用主要为： 假设在小写文本中第一次出现table的索引位置为 1000，
# 那么在原文本中前 1000个字符里最后一次出现keyword的索引位置为800
# 则把原文本索引为800之后的所有字符抽取出来，记为text2
# 若所有table在小写文档中出现的索引都小于keyword在原文档第一次出现的索引
# 则直接把原文档另存为为新文档

def main():
    os.mkdir('result')      # 新建空文件夹result，用于存放输出文档
    keyword = 'LETTER OF CREDIT AND REIMBURSEMENT AGREEMENT'  # 需要在原文本中查找的keyword
    table = 'Table of Contents'.lower()  # 需要在小写原文本中查找的关键字，记作 table

    for fileName in listdir('source'):
        text = open('source/' + fileName).read()

        final_Keyword = 0;
        final_Table = 0;
        temp_distance = np.inf;

        index_Keyword = my_find(fileName, keyword=keyword)  # 找出keyword在原文本中的所有索引位置
        index_Table = table_find(fileName, keyword=table)  # 找出table在小写原文本中的所有索引位置

        if len(index_Keyword) != 0 and len(index_Table) != 0:
            for k_1 in range(len(index_Keyword)):
                for k_2 in range(len(index_Table)):
                    distance = index_Table[k_2] - index_Keyword[k_1]
                    if distance > 0:  # 如果 table出现在keyword的后面
                        if distance < temp_distance:
                            final_Keyword = index_Keyword[k_1]
                            final_table = index_Table[k_2]
                            temp_distance = distance

            text2 = text[final_Keyword:]
            fid = open('result/' + fileName, 'w')
            fid.write(text2)
            fid.close()

if __name__ == "__main__" :
    main()
