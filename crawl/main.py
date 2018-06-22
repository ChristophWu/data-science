#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 10:00:17 2018

@author: jason
"""

from bs4 import BeautifulSoup
import requests
import sys
#html = urlopen("https://www.ptt.cc/bbs/Beauty/index.html").read().decode('utf-8')
#another way to get the content of url

deleted_url = BeautifulSoup('<a>本文已被删除<a>','lxml').a
Head_url = 'https://www.ptt.cc'
url_list = list()
not_good = ['https://www.ptt.cc/bbs/Beauty/M.1490936972.A.60D.html',
            'https://www.ptt.cc/bbs/Beauty/M.1494776135.A.50A.html',
            'https://www.ptt.cc/bbs/Beauty/M.1503194519.A.F4C.html',
            'https://www.ptt.cc/bbs/Beauty/M.1504936945.A.313.html',
            'https://www.ptt.cc/bbs/Beauty/M.1505973115.A.732.html',
            'https://www.ptt.cc/bbs/Beauty/M.1507620395.A.27E.html',
            'https://www.ptt.cc/bbs/Beauty/M.1510829546.A.D83.html',
            'https://www.ptt.cc/bbs/Beauty/M.1512141143.A.D31.html',
            ]




# get date,title,url and click number
def crawl():
    link_ = 'https://www.ptt.cc/bbs/Beauty/index' + str(2000) +'.html'
    link = requests.get(link_)
    content = link.text
    soup = BeautifulSoup(content, 'lxml')
    for i in soup.find_all('div','r-ent')[5:]:
        tmp = i.find('div','title').find('a') or deleted_url
        if tmp.get('href') in not_good:
            pass
        else:
            list_tmp={
                'title': tmp.getText().strip(),
                'html': tmp.get('href'),
                'hot': i.find('div','nrec').getText(),
                'date': i.find('div','date').getText(),
                }
            if '10/' in list_tmp['date'] or '11/' in list_tmp['date'] or '12/' in list_tmp['date']:
                pass
            else:
                tmp1 = list_tmp['date'][1:]
                list_tmp['date'] = tmp1
            url_list.append(list_tmp)
    
    ######## crawl the urls ##########    
    
    for it in range(2001,2352):
        link_ = 'https://www.ptt.cc/bbs/Beauty/index' + str(it) +'.html'
    
        link = requests.get(link_)
        content = link.text
        soup = BeautifulSoup(content, 'lxml')
        for i in soup.find_all('div','r-ent'):
            tmp = i.find('div','title').find('a') or deleted_url
            if tmp.get('href') in not_good:
                pass
            else:
                list_tmp={
                    'title': tmp.getText().strip(),
                    'html': tmp.get('href'),
                    'hot': i.find('div','nrec').getText(),
                    'date': i.find('div','date').getText(),
                    }
                if '10/' in list_tmp['date'] or '11/' in list_tmp['date'] or '12/' in list_tmp['date']:
                    pass
                else:
                    tmp1 = list_tmp['date'][1:]
                    list_tmp['date'] = tmp1
                url_list.append(list_tmp)
        #tmp = soup.find('div', 'btn-group-paging').find_all('a', 'btn')
        #next_link = tmp[1].get('href')
    
    ######## crawl the urls ##########   
    
    link_ = 'https://www.ptt.cc/bbs/Beauty/index' + str(2352) +'.html'
    link = requests.get(link_)
    content = link.text
    soup = BeautifulSoup(content, 'lxml')
    for i in soup.find_all('div','r-ent')[:2]:
        tmp = i.find('div','title').find('a') or deleted_url
        if tmp.get('href') in not_good:
            pass
        else:
            list_tmp={
                'title': tmp.getText().strip(),
                'html': tmp.get('href'),
                'hot': i.find('div','nrec').getText(),
                'date': i.find('div','date').getText(),
                }
            if '10/' in list_tmp['date'] or '11/' in list_tmp['date'] or '12/' in list_tmp['date']:
                pass
            else:
                tmp1 = list_tmp['date'][1:]
                list_tmp['date'] = tmp1
            url_list.append(list_tmp)    
        
    ######### write url, date, title into txt #############
    
    f = open('all_articles.txt', 'w', encoding = 'utf-8')
    for tmp in url_list:
        if '公告' in tmp['title']:
            pass
        elif '删除' in tmp['title']:
            pass
        else:
            tmp1 = tmp['date'].split('/')
            f.write(tmp1[0])
            f.write(tmp1[1])
            f.write(',')
            f.write(tmp['title'])
            f.write(',')
            f.write(Head_url)
            f.write(tmp['html'])
            f.write('\n')
    f.close()
    
    f2 = open('all_popular.txt', 'w', encoding = 'utf-8')
    for tmp in url_list:
        if '公告' in tmp['title']:
            pass
        else:
            if '爆' in tmp['hot']:
                tmp1 = tmp['date'].split('/')
                f2.write(tmp1[0])
                f2.write(tmp1[1])
                f2.write(',')
                f2.write(tmp['title'])
                f2.write(',')
                f2.write(Head_url)
                f2.write(tmp['html'])
                f2.write('\n')
    f2.close()
    return 0
########## write url, date, title into txt #############

########## get tui and xu numbers and tui_list, xu_list ###########

def push(start_data,end_data):
    push_list = {}
    f3 = open('all_articles.txt',encoding = 'utf-8')
    push_start_date = int(start_data)
    push_end_date = int(end_data)
    tui = 0
    xu = 0
    while True:
        line = f3.readline()
        if not line:
            break
        line = line.split(',')
        if int(line[0]) in range(push_start_date,push_end_date + 1):      
            a = str(line[2][0:-1])   # [0,-1]let \n be deleted
            try:
                link = requests.get(a)
                content = link.text
                soup = BeautifulSoup(content, 'lxml')
            except:
                pass
            for i in soup.find_all('div','push'):
                try:
                    if '推' in (i.find('span').getText()):
                        name = i.find('span','f3 hl push-userid').getText()
                        tui +=1
                        if i.find('span','f3 hl push-userid').getText() in push_list:
                            push_list[name][0] +=1
                        else:
                            push_list[name] = [1,0]
                    if '噓' in (i.find('span').getText()):
                        name = i.find('span','f3 hl push-userid').getText()
                        xu += 1
                        if i.find('span','f3 hl push-userid').getText() in push_list:
                            push_list[name][1] +=1
                        else:
                            push_list[name] = [0,1]
                except:
                    pass
    f3.close()
    
    ######### get tui and xu numbers and tui_list, xu_list ###########
    
    ######### output top 10 tui and top 10 xu ###############
    s = 'push[' +str(start_data) + ',' + str(end_data) +'].txt'
    f_push = open(s, 'w', encoding = 'utf-8')
    tmp = push_list
    tui_sort = sorted(tmp.items(),key = lambda item:(-item[1][0],item[0]))
    xu_sort = sorted(tmp.items(),key = lambda item:(-item[1][1],item[0]))
    print('all like: {}'.format(tui))
    print('all boo: {}'.format(xu))
    f_push.write('all like: {}'.format(tui))
    f_push.write('\n')
    f_push.write('all boo: {}'.format(xu))
    f_push.write('\n')
    # output top 10 tui 
    j = 0
    for j in range(10):
        str_tmp = 'like #' + str(j+1) +':'
        print(str_tmp,tui_sort[j][0],tui_sort[j][1][0])
        s = str_tmp + ' ' + tui_sort[j][0] + ' ' + str(tui_sort[j][1][0])
        f_push.write(s)
        f_push.write('\n')
    # output top 10 xu 
    j = 0
    for j in range(10):
        str_tmp = 'boo #' + str(j+1) +':'
        print(str_tmp,xu_sort[j][0],xu_sort[j][1][1])
        s = str_tmp + ' ' + xu_sort[j][0] + ' ' + str(xu_sort[j][1][1])
        f_push.write(s)
        f_push.write('\n')
    ########## output top 10 tui and top 10 xu ##############
    f_push.close()
    return 0

########## get the links of images in popular articles ###########

def popular(start_date,end_date):
    f4 = open('all_popular.txt',encoding = 'utf-8')
    populer_start_date = int(start_date)
    populer_end_date = int(end_date)
    tile = ['.jpg', '.png', '.gif', '.jpeg']
    popular_url_list = []
    popular_number = 0
    while True:
        line = f4.readline()
        if not line:
            break
        line = line.split(',')
        if int(line[0]) in range(populer_start_date,populer_end_date + 1):
            popular_number += 1
            try:
                a = str(line[2][0:-1])   # [0,-1]let \n be deleted
                link = requests.get(a)
                content = link.text
                soup = BeautifulSoup(content, 'lxml')
                url = soup.find_all('a')
            except:
                pass
            for tmp in url:
                try:
                    if tmp['href'][-5:] in tile or tmp['href'][-4:] in tile:
                        popular_url_list.append(tmp['href'])
                except:
                    pass
    f4.close()
    s = 'popular[' +str(start_date) + ',' + str(end_date) +'].txt'
    f_popular = open(s,'w',encoding = 'utf-8') 
    s = 'number of popular articles:' + str(popular_number) + '\n'
    f_popular.write(s)
    for i in popular_url_list:
        f_popular.write(i)
        f_popular.write('\n')
    f_popular.close()
    return 0

########## get the links of images in popular articles ###########    
    
########## get the links of images in keyword articles ###########

def keyword(key, start_date, end_date):
    keyword = key
    f5 = open('all_articles.txt',encoding = 'utf-8')
    keyword_start_date = int(start_date)
    keyword_end_date = int(end_date)
    tile = ['.jpg', '.png', '.gif', '.jpeg']
    keyword_url_list = []
    while True:
        line = f5.readline()
        if not line:
            break
        line = line.split(',')
        if int(line[0]) in range(keyword_start_date,keyword_end_date + 1):
            try:
                a = str(line[2][0:-1])   # [0,-1]let \n be deleted
                link = requests.get(a)
                content = link.text
                soup = BeautifulSoup(content, 'lxml')
            except:
                pass
            is_keyword = str(soup).split('發信站')[0]
            if keyword in is_keyword:
                url = soup.find_all('a')
                for tmp in url:
                    try:
                        if tmp['href'][-5:] in tile or tmp['href'][-4:] in tile:
                            keyword_url_list.append(tmp['href'])
                    except:
                        pass
    f5.close()
    s = 'keyword(' + str(key) + ')[' + str(start_date) + ',' + str(end_date) +'].txt'
    f_keyword = open(s,'w',encoding = 'utf-8')
    for i in keyword_url_list:
        f_keyword.write(i)
        f_keyword.write('\n')
    f_keyword.close()
    return 0

########## get the links of images in keyword articles ###########

#crawl_ = crawl()
#push_ = push(101,1231)
#popular_ = popular(101,1231)
#keyword_ = keyword('正妹',101,1231) 

if sys.argv[1] == 'crawl':
    crawl()
if sys.argv[1] == 'push':
    push(sys.argv[2],sys.argv[3])
if sys.argv[1] == 'popular':
    popular(sys.argv[2],sys.argv[3])
if sys.argv[1] == 'keyword':
    keyword(sys.argv[2],sys.argv[3],sys.argv[4])



















