# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 20:29:26 2022

@author: mcxru
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rc('font', family='Malgun Gothic')
news = pd.read_csv('C:/Users/mcxru/Desktop/뉴스.csv')
sns = pd.read_csv('C:/Users/mcxru/Desktop/sns.csv')
#hyundai_news= news[news['id']==5380]
#hyundai_sns= sns[sns['id']== 5380]
#naver_news= news[news['id']==35420]
#naver_sns= sns[sns['id']== 35420]
#kakao_news= news[news['id']== 35720]
#kakao_sns= sns[sns['id']== 35720]
#lg_news= news[news['id']==66570]
lg_sns= sns[sns['id']== 66570]


#hyundai_news = hyundai_news['value'].value_counts()
#hyundai_sns = hyundai_sns['value'].value_counts()
#naver_news= naver_news['value'].value_counts()
#naver_sns= naver_sns['value'].value_counts()
#kakao_news= kakao_news['value'].value_counts()
#kakao_sns= kakao_sns['value'].value_counts()
#lg_news= lg_news['value'].value_counts()
lg_sns= lg_sns['value'].value_counts()

#plt.pie(hyundai_news, labels = hyundai_news.index,autopct=lambda p : '{:.2f}%'.format(p))
#plt.pie(hyundai_sns, labels=hyundai_sns.index,autopct=lambda p : '{:.2f}%'.format(p))
#plt.pie(naver_news, labels=naver_news.index,autopct=lambda p : '{:.2f}%'.format(p))
#plt.pie(naver_sns, labels=naver_sns.index,autopct=lambda p : '{:.2f}%'.format(p))
#plt.pie(kakao_news, labels=kakao_news.index,autopct=lambda p : '{:.2f}%'.format(p))
#plt.pie(kakao_sns, labels=kakao_sns.index,autopct=lambda p : '{:.2f}%'.format(p))
#plt.pie(lg_news, labels= lg_news.index,autopct=lambda p : '{:.2f}%'.format(p))
plt.pie(lg_sns, labels=lg_sns.index,autopct=lambda p : '{:.2f}%'.format(p))
plt.title('LG전자 SNS')
plt.figure(figsize=(14,9))