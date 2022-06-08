# -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:36:25 2022

@author: t1
"""

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import mplfinance as mpf
import pandas_datareader as web

HOSTNAME = 'localhost'
PORT = 3306
USERNAME = 'SW'
PASSWORD = '1234'
DATABASE = 'testdb'
CHARSET1 = 'utf8mb4'
CHARSET2 = 'utf-8'
con_str_fmt='mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'
con_str=con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
pymysql.install_as_MySQLdb()
import MySQLdb
engine=create_engine(con_str, encoding=CHARSET2);
conn=engine.connect();

df = web.naver.NaverDailyReader('066570', start='20200101', end='20211231').read()

df = df.astype(int)
df['Ticker']='066570'
news_df.to_sql(name ='lg',con=engine, if_exists='append',index=False)