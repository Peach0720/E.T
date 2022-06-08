#!/usr/bin/env python
# coding: utf-8

# In[18]:


#크롤링시 필요한 라이브러리 불러오기
import time
from bs4 import BeautifulSoup
import requests
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# In[19]:


# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
  #입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num+1
    else:
        return num+9*(num-1)


# In[20]:


# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
def makeUrl(search,start_pg,end_pg):
    if start_pg == end_pg:
        url = "https://finance.naver.com/item/board.naver?code=" + search +"&page="+ str(start_pg)
     #   print("생성url: ",url) 
        return url
    else:
        urls= []
        for i in range(start_pg,end_pg+1):
            url = "https://finance.naver.com/item/board.naver?code=" + search +"&page="+ str(i)
            urls.append(url)
      #  print("생성url: ",urls)
        return urls


# In[21]:


# html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)
def news_attrs_crawler(articles,attrs):
    attrs_content=[]
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content


# In[22]:


#뉴스기사 내용 크롤링하는 함수 만들기(각 뉴스의 url)
def news_contents_crawler(news_url):
    contents=[]
    for i in news_url:
        #각 종목토론실 html get하기
        news = requests.get(i,headers = headers)
        news_html = BeautifulSoup(news.text,"html.parser")
            #종목토론실 내용 가져오기 (p태그의 내용 모두 가져오기) 
        contents.append(news_html.select('#content > div.section.inner_sub > table.view > tbody > tr:nth-child(1) > th:nth-child(1) > strong'))
    return contents


# In[23]:


#html생성해서 기사크롤링하는 함수 만들기(제목,url): 4개의 값을 반환함(제목, 링크, 내용, 날짜)
def articles_crawler(url):
    #html 불러오기
    original_html = requests.get(i,headers = headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    # 검색결과
    articles = html.select("td.title > a")
    date = html.select(' tr > th.gray03.p9.tah')
    title = news_attrs_crawler(articles,'title')
    url = news_attrs_crawler(articles,'href')
    content = news_contents_crawler(url)
    
   
    return title, url, content, date #4개의 값을 반환 


# In[ ]:


#####뉴스크롤링 시작#####

#검색어 입력
search = input("검색할 키워드를 입력해주세요:")

#검색 시작할 페이지 입력
page = int(input("\n크롤링할 시작 페이지를 입력해주세요. ex)1(숫자만입력):")) # ex)1 =1페이지,2=2페이지...
print("\n크롤링할 시작 페이지: ",page,"페이지")   
#검색 종료할 페이지 입력
page2 = int(input("\n크롤링할 종료 페이지를 입력해주세요. ex)1(숫자만입력):")) # ex)1 =1페이지,2=2페이지...
print("\n크롤링할 종료 페이지: ",page2,"페이지")   

# naver url 생성
url = makeUrl(search,page,page2)

#뉴스 크롤러 실행
news_titles = []
news_url =[]
news_contents =[]
news_date = []
for i in url:
    title, url,content ,date= articles_crawler(url)
    news_titles.append(title)
    news_url.append(url)
    news_contents.append(content)
    news_date.append(date)

# print("검색된 기사 갯수: 총 ",(page2+1-page)*10,'개')
# print("\n[뉴스 제목]")
# print(news_titles)
# print("\n[뉴스 링크]")
# print(news_url)
# print("\n[뉴스 내용]")
# print(news_contents)
# print("\n뉴스 날짜")
# print(news_date)

# In[ ]:


###데이터 프레임으로 만들기###
import pandas as pd

#제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
def makeList(newlist, content):
    for i in content:
        for j in i:
            newlist.append(j)
    return newlist
    
#제목, 링크, 내용 담을 리스트 생성
news_titles_1, news_url_1, news_contents_1, news_date_1 = [],[],[],[]

#1차원 리스트로 만들기(내용 제외)
makeList(news_titles_1,news_titles)
makeList(news_url_1,news_url)
makeList(news_contents_1,news_contents)
makeList(news_date_1,news_date)


#데이터 프레임 만들기
news_df = pd.DataFrame({'title':news_titles_1,'link':news_url_1,'content':news_contents_1,'date':news_date_1})
news_df


# In[ ]:




