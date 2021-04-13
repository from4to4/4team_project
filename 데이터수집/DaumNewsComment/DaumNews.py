#!/usr/bin/env python
# coding: utf-8

# In[1]:


# soup 요청 함수
def getSource(site) :
    
    import requests
    import bs4
    
    # 헤더 정보
    header_info = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb Kit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
    }
    
    # 요청한다.
    response = requests.get(site, headers=header_info)
    
    # bs4 객체 생성
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    
    return soup


# In[2]:


# 한 페이지에 있는 다음 뉴스 링크 수집 함수
def getNewsLink(site, COLOPHON):
    
    import pandas as pd
    import os
    
    soup = getSource(site)

    link_list = []

    # li 태그 가져오기
    a1 = soup.select('#clusterResultUL > li')
    # print(len(a1))
    
    for a2 in a1:
        
        # div 태그 가져오기
        a3 = a2.select_one('div.wrap_cont > div > div > a')
        # print(a3)
        
        # 기사링크 
        data1 = a3.attrs['href']
        # print(data1)
        
        # 기사제목
        data2 = a3.text.strip()
        # print(data2)
    
        # span 태그 가져오기
        a4 = a2.select_one('div.wrap_cont > div > span.f_nb.date')
        a5 = a4.text.strip().split('|')
        
        # 날짜
        data3 = a5[0]
        
        # 언론사
        data4 = a5[1]
        
        # print(data1, data2, data3, data4)
        
        # 기사 링크 리스트에 저장
        link_list.append(data1)
    
    # 데이터프레임 생성
    df1 = pd.DataFrame(link_list)
    # display(df1)
    

    FILENAME = f'{COLOPHON}_link.csv'

    if os.path.exists(FILENAME) == False:
        # 파일이 없을 경우
        df1.to_csv(FILENAME, encoding='utf-8-sig', index=False)
    else:
        # mode='a' : 기존 것 뒤에다 붙여줌
        df1.to_csv(FILENAME, encoding='utf-8-sig', index=False, header=False, mode='a')
    


# In[3]:


# 다음 페이지 존재 여부 확인하는 함수
def getNextPage(site) :
    
    # url에서 p= 값 들고오기
    p = site.split('&')[-1].split('=')[-1]
    
    # p값에 1 더해서 다음 페이지 url 만들기
    nextPage = site[:-len(p)] + str(int(p)+1)
    # print(next_page)

    # 현재 페이지와 다음 페이지 soup 가져오기
    soup1 = getSource(site)
    soup2 = getSource(nextPage)
    # print(soup1)
    # print(soup2)

    # 현재 페이지와 다음 페이지 첫번째 a 태그에서 링크 가져오기
    a1 = soup1.select('#clusterResultUL > li > div.wrap_cont > div > div > a')[0].attrs['href']
    a2 = soup2.select('#clusterResultUL > li > div.wrap_cont > div > div > a')[0].attrs['href']
    # print(a1)
    # print(a2)
   
    # 두 링크가 같지 않으면 다음 페이지가 있다고 간주, 다음 페이지 return 
    if a1 != a2 :
        return True
    # 같으면 다음 페이지 없다고 간주, False return 
    else :
        return False


# In[5]:


def getDaumNewsUrlDF(KEYWORD, COLOPHON, dayStart, dayEnd, page):

    import time
    import pandas as pd
    from IPython.display import clear_output
    import urllib
    
    # 검색어
    KEYWORD = urllib.parse.quote(KEYWORD)
    COLOPHON = COLOPHON
    dayStart = dayStart
    dayEnd = dayEnd
    page=page
    
    # 다음 뉴스 검색 url
    URL = 'https://search.daum.net/search?w=news&enc=utf8&cluster=y&cluster_page=1&'
    
    # url에 들어갈 파라미터
    cp_dict = {'조선일보' : '16d4PV266g2j-N3GYq',
               '중앙일보' : '16Elf9uX5H6T5xXvQV',
               '동아일보' : '16bOiOx4gG2S18EPLj',
               'JTBC'     : '16yZfDfR_rGcw5F-P0',
               '경향신문' : '16akMkKFDu6n8GTzZr',
               '한겨레' : '16nzyJHdH5ORpabfqG'}
    cpName = urllib.parse.quote(COLOPHON)
    cp = cp_dict[COLOPHON]
    
    # 페이지 번호
    page = 1
    
    while True :
        time.sleep(1)

        clear_output(wait=True)

        site = f'{URL}q={KEYWORD}&cpname={cpName}&cp={cp}&period=6m&sd={dayStart}&ed={dayEnd}&DA=PGD&p={page}'

        print(f' 다음 뉴스 - {COLOPHON} : {page} 페이지 수집 중' )

        getNewsLink(site, COLOPHON) 
        chk = getNextPage(site)

        if chk != False:
            page = page + 1
        else: 
            print(f'{COLOPHON}_link.csv 파일 저장 완료')
            break
    
    df = pd.read_csv(f'{COLOPHON}_link.csv', )
    return df


# In[6]:


test = False
if test:
    # 검색어
    KEYWORD = '보궐선거'

    # 언론
    # 조선일보, 중앙일보, 동아일보, JTBC, 경향신문, 한겨레 택1
    COLOPHON = '동아일보'

    # 날짜 (YYYYMMDhhmmss)
    dayStart = '20210407000000'
    dayEnd   = '20210407200000'

    df = getDaumNewsUrlDF(KEYWORD=KEYWORD, COLOPHON=COLOPHON, dayStart=dayStart, dayEnd=dayEnd, page=1)
    display(df)


# In[ ]:




