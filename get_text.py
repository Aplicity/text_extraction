#!/usr/bin/python
# -*- coding:utf-8 -*-

import pandas as pd
import requests
import os
from numpy import *
import numpy as np

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


