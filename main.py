from os import listdir
import os
from numpy import *
import numpy as np
from find_tool import my_find,table_find
'''

主函数
以下程序的作用主要为： 假设在小写文本中第一次出现table的索引位置为 1000，
那么在原文本中前 1000个字符里最后一次出现keyword的索引位置为800
则把原文本索引为800之后的所有字符抽取出来，记为text2
若所有table在小写文档中出现的索引都小于keyword在原文档第一次出现的索引
则直接把原文档另存为为新文档

'''

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
