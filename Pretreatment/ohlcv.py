# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import warnings
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'NanumGothic'

def graph(Ticker):
    # db 관련 정보
    HOSTNAME = '203.234.62.112'
    PORT = 3306
    USERNAME = 'SW'
    PASSWORD = '1234'
    DATABASE = 'stock'
    CHARSET1 = 'utf8mb4'
    CHARSET2 = 'utf-8'
    con_str_fmt = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'
    con_str = con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
    engine = create_engine(con_str, encoding=CHARSET2)
    conn = engine.connect()

    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table('ohlcv', metadata, autoload=True, autoload_with=engine)

    print(table.columns.keys())
    indata = []
    # query = sqlalchemy.select([table])
    # query = sqlalchemy.select(table.date)
    query = sqlalchemy.select(table)  # 뽑아라
    print(query)
    with engine.connect() as conn:
        for row in conn.execute(query):
            indata.append(row)

    # indata = pd.read_sql_query("select 제목 from news", engine)

    conn.close()
    df = pd.DataFrame(indata)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ticker']
    print(df)
    df = df[df['Ticker'] == Ticker]
    print(df['Ticker'].unique())

def sqldb(code):
    # db 관련 정보
    HOSTNAME = '203.234.62.112'
    PORT = 3306
    USERNAME = 'SW'
    PASSWORD = '1234'
    DATABASE = 'stock'
    CHARSET1 = 'utf8mb4'
    CHARSET2 = 'utf-8'
    con_str_fmt = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'
    con_str = con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
    engine = create_engine(con_str, encoding=CHARSET2)
    conn = engine.connect()

    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table('ohlcv', metadata, autoload=True, autoload_with=engine)

    print(table.columns.keys())
    indata = []
        # query = sqlalchemy.select([table])
        # query = sqlalchemy.select(table.date)
    query = sqlalchemy.select(table).where(table.c.Ticker == code)  # 뽑아라
    print(query)
    with engine.connect() as conn:
        for row in conn.execute(query):
            indata.append(row)

    # indata = pd.read_sql_query("select 제목 from news", engine)

    conn.close()
    df = pd.DataFrame(indata)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ticker']
    print(df)

    stock_close = df['Close']
    stock_close.index = df['Date']

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)

    # 그래프 그려서 확인
    # 실제 데이터 점을 그림

    # 모델을 그림
    ax.plot(stock_close.index, stock_close, label='주가 차트')
    if code == "035720":
        code = "카카오"
    elif code == "005380":
        code = "현대차"
    elif code == "066570":
        code = "LG전자"
    elif code == "035420":
        code = "NAVER"
    plt.title(code)
    plt.legend(loc='upper right')
    plt.show()

def main(Ticker):
    # db 관련 정보
    HOSTNAME = '203.234.62.112'
    PORT = 3306
    USERNAME = 'SW'
    PASSWORD = '1234'
    DATABASE = 'stock'
    CHARSET1 = 'utf8mb4'
    CHARSET2 = 'utf-8'
    con_str_fmt = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'
    con_str = con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
    engine = create_engine(con_str, encoding=CHARSET2)
    conn = engine.connect()

    metadata = sqlalchemy.MetaData()
    table = sqlalchemy.Table('ohlcv', metadata, autoload=True, autoload_with=engine)

    print(table.columns.keys())
    indata = []
    # query = sqlalchemy.select([table])
    # query = sqlalchemy.select(table.date)
    query = sqlalchemy.select(table)  # 뽑아라
    print(query)
    with engine.connect() as conn:
        for row in conn.execute(query):
            indata.append(row)

    # indata = pd.read_sql_query("select 제목 from news", engine)

    conn.close()
    df = pd.DataFrame(indata)
    df.columns= ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ticker']
    print(df)
    df=df[df['Ticker']==Ticker]
#    df=df[df['Ticker'] == Ticker]

#    df.loc[1:,'Change'] = df['Volume']

#    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change']]
    print(df)


sqldb('035420')
# DB에 총 6개 ['005930' '000660' '035420' '005380' '035720' '005490' '066570']
