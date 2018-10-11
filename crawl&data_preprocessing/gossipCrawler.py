# -*- coding: UTF-8 -*-  
import requests
import os
import re
import time
import sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def crawl_articles():
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes' : 'yes'
    }
    rs = requests.session()
    response = rs.post('https://www.ptt.cc/ask/over18', verify = False, data = payload)
    response = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html', verify = False)
    soup = BeautifulSoup(response.text,'html.parser')
    index = soup.find_all('a','btn wide')[1]['href']
    index = index.split('/')[-1]
    index = int(index[5:-5])+1
    f = open('articles_0613.txt','w',encoding = 'utf-8')
    url = 'https://www.ptt.cc/bbs/Gossiping/index'
    all_url = []
    NoneType = type(None)
    for idx in range(5000):
        response = rs.get(url+str(index-idx)+'.html')
        soup = BeautifulSoup(response.text,'html.parser')
        for entry in soup.select('.r-ent'): 
            title = entry.select('.title')[0].find('a')
            if isinstance(title,NoneType):
                continue
            url_ = title['href']
            all_url.append(url_)
        if idx%100 == 0:
            print(index-idx)
    for url_ in all_url:
        f.write(str(url_)+"\n")
    f.close()

def fetch_comments():
    payload = {
    'from': '/bbs/Gossiping/index.html',
    'yes' : 'yes'
    }
    rs = requests.session()
    response = rs.post('https://www.ptt.cc/ask/over18', verify = False, data = payload)
    f = open('articles.txt','r',encoding = 'utf-8')
    file = open('comment.txt','a',encoding = 'utf-8')
    url = 'https://www.ptt.cc'
    all_url=[]
    comment = []
    author = []
    count = 0
    for url_ in f.readlines():
        count = count + 1
        response = rs.get(url+url_.strip('\n'))
        soup = BeautifulSoup(response.text,'html.parser')
        all_author = soup.find_all('span','f3 hl push-userid')
        all_content = soup.find_all('span','f3 push-content')
        for author_,comment_ in zip(all_author,all_content):
            author.append(author_.text)
            comment.append(comment_.text[2:])
            # all_comment.update({author.text:comment.text[2:]})
        if count % 10000 == 0:
            print("No.%d articles:%s"%(count,url+url_))  
            for author_,comment_ in zip(author,comment):
                file.write(author_+":"+comment_+"\n")
            comment = []
            author = []
        else:
            pass
    for author_,comment_ in zip(author,comment):
        file.write(author_+":"+comment_+"\n")
    f.close()
    file.close()

