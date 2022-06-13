# -*- coding: utf-8 -*-
import re
import pandas as pd
import json
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from konlpy.tag import Mecab

filepath="./news_title.csv"           #파일이름

def delete_word(word):
    word=word.replace("&lt;1&gt", "").replace("All rights reserved", "").replace("저작권자", "")
    word=word.replace("파이낸셜뉴스", "").replace("무단전재 재배포 금지", "").replace("Copyright", "")
    word=word.replace("파이낸셜뉴스", "").replace("All rights reserved","").replace("Copyright", "")
    word=word.replace("파이낸셜뉴스", "").replace("무단전재 및 재배포 금지","").replace("한경닷컴","")
    word=word.replace("여러명에게 보낼 경우 콤마 로 구분하세요","").replace("최근 검색어 내역이 없습니다","")
    word=word.replace("본 사이트에 게재되는 정보는 오류 및 지연이 있을 수 있으며 그 이용에 따르는 책임은 이용자 본인에게 있습니다","")
    word=word.replace("인쇄 메일 글씨 크기 선택 가장 작은 크기 글자 한 단계 작은 크기"
                      " 글자 기본 크기 글자 한 단계 큰 크기 글자 가장 큰 크기 글자","")
    word=word.replace("입력       수정       ","")
    temp="동아일보 회사소개 문화스포츠사업 신문박물관 인촌기념회 화정 평화재단 신문광고안내 구독신청 독자서비스 기사제보 정정보도 신청" \
         " 동아닷컴 회사소개 광고 인터넷 전광판 제휴안내 이용약관 개인정보처리방침 청소년보호정책 책임자 구민회 사이트맵  주소 서울특별시" \
         " 서대문구 충정로 등록번호 서울아 발행일자 등록일자 발행 편집인 박원재 서울경제를 팔로우하세요 서울경제신문 텔레그램 뉴스채널" \
         " 서울경제 썸".split(sep=" ",)
    for dels in temp:
        word=word.replace(dels,"")

    word = word.strip()
    return word

def cleansing(text):
    text=str(text)
    text=remove_tag(text)

    return(text)

def remove_tag(sentence):
    text = re.sub('(<([^>]+)>)', '', sentence)

    pattern = '(\[a-zA-Z0-9\_.+-\]+@\[a-zA-Z0-9-\]+.\[a-zA-Z0-9-.\]+)'  # e-mail 주소 제거
    text = re.sub(pattern=pattern, repl=' ', string=text)

    pattern = '(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+'  # url 제거
    text = re.sub(pattern=pattern, repl=' ', string=text)

    pattern = '<[^>]*>'  # html tag 제거
    text = re.sub(pattern=pattern, repl=' ', string=text)

    pattern = '[^\w\s]'  # 특수기호 제거
    text = re.sub(pattern=pattern, repl=' ', string=text)

    pattern = '[\r|\n]'  # \r, \n 제거
    text = re.sub(pattern=pattern, repl=' ', string=text)

    pattern = re.compile(r'\s+')  # 이중 space 제거
    text = re.sub(pattern=pattern, repl=' ', string=text)

    pattern = '[^가-힣\s]'                                          # 한글을 제외한 문자 제거
    text = re.sub(pattern=pattern, repl='', string=text)

    text = delete_word(text)

    return text

def loadjs(json_path='./user_dic.json'):
    with open(json_path,'r',encoding='UTF-8') as file:
        data=json.load(file)
    data = pd.DataFrame(data)
    k_dict={}
    for i in range(len(data)):
        temp=data['word_root'][i]
        temp=cleansing(temp)
        k_dict[temp]=int(data['polarity'][i])
    return k_dict

mecab = Mecab(dicpath=r"C:/mecab/mecab-ko-dic")

file=open('./불용어.txt',encoding='utf-8')
stopwords=file.readlines()
file.close()

#df=pd.read_csv('C:/Users/DILAB/Downloads/nsmc-master/ratings.txt',sep='\t')

HOSTNAME = '203.234.62.112'
PORT = 3306
USERNAME = 'SW'
PASSWORD = '1234'
DATABASE = 'stock'
CHARSET1 = 'utf8mb4'
CHARSET2 = 'utf-8'
con_str_fmt='mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'
con_str=con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
engine=create_engine(con_str, encoding=CHARSET2)
conn=engine.connect()

metadata=sqlalchemy.MetaData()
table = sqlalchemy.Table('news', metadata, autoload=True, autoload_with=engine)          #테이블 명

print(table.columns.keys())
indata=[]
###query = sqlalchemy.select([table])
query = sqlalchemy.select(table.c.content,table.c.date,table.c.Ticker).where(
    table.c.date >= '2021.07.01', table.c.date <= '2021.12.31', table.c.Ticker != '05930', table.c.Ticker != '000660' )
print(query)
with engine.connect() as conn:
        for row in conn.execute(query):
            indata.append(row)
#3indata = pd.read_sql_query("select 제목 from news", engine)

conn.close()

df=pd.DataFrame(indata)
#print(df)
print(df.shape)
print(df.shape[0])
print(df[2].value_counts())
###df=pd.read_csv('C:/Users/DILAB/Downloads/samsung.csv',encoding='UTF-8')

sentences=["한국어자연어처리를위한konlpy설치완료",
           "울면서 손들고 횡단보도 건널때 뛰쳐나올뻔 이범수 연기 드럽게못해",
           "담백하고 깔끔해서 좋다. 신문기사로만 보다 보면 자꾸 잊어버린다. 그들도 사람이었다는 것을."
           "취향은 존중한다지만 진짜 내생에 극장에서 본 영화중 가장 노잼 노감동임 스토리도 어거지고 감동도 어거지"]

data=[] #전처리된 데이터
user_dic=loadjs() #사용자 감성사전 불러오기


for word in df.iloc[:,0]:
    temp=[] #임시 문자 리스트
    sentence=cleansing(word)
    #nouns = mecab.nouns(sentence)
    #print('명사 단위:', nouns)
    pos = mecab.pos(sentence)
    result=[]
    delete=['JKS','JKC','JKG','JKO','JKB','JKV','JKQ','JX','JC','ETM','EC'] #조사와 같은 의미 없는 단어

    score = 0  # 감성점수
    for i in range(len(pos)):
        if pos[i][0] not in stopwords:
            temp.append(pos[i][0])
            if pos[i][1] not in delete:
                result.append(pos[i][0])
        if pos[i][0] in user_dic:
            score+=user_dic[pos[i][0]]
    if score>=3:
        emotion="강한 긍정"
    elif score<=-3:
        emotion="강한 부정"
    elif score>=1:
        emotion="긍정"
    elif score<=-1:
        emotion="부정"
    else:
        emotion="중립"

    word=" ".join(temp)
    word=sentence.strip()

    pattern = re.compile(r'\s+')  # 이중 space 제거
    word = re.sub(pattern=pattern, repl=' ', string=word)

    result=[word,emotion]
    if word!="":
        data.append(result)

data=pd.DataFrame(data)
df.iloc[:,1]=df.iloc[:,1].str.split(' ').str[0]

data=pd.concat([data,df.iloc[:,1],df.iloc[:,2]],axis=1) #합쳐서 X를 만듦 ex) [1,x1,x2]
data.columns=['title','value','date','id']
data=data.dropna(how='any')
#print(data)
print(data['id'].value_counts())
data.to_csv(filepath,encoding="euc-kr")
print("저장 완료")

