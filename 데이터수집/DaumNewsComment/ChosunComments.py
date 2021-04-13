#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 댓글 수집 완료
# 댓글에 답글 수집 실패


# In[2]:


import time
import os

import pandas as pd

import urllib
import platform

from selenium import webdriver as wd

from IPython.display import clear_output


# In[3]:


# 더보기 계속 클릭하기
def clickMore(driver):
    
    import time
    
    while True:
        try:
            more_button = driver.find_element_by_css_selector('#comment-more-id')
            more_button.click()
            time.sleep(1)
        except:
            break


# In[4]:


# 한 기사의 댓글 추출
def getComment(driver):
    
    import os
    import pandas as pd
    
    # 데이터를 담을 딕셔너리
    comment_dict = {
        '제목' : [],
        '날짜' : [],
        '작성일' : [],
        '댓글' : []
    }
    
    # 기사 태그
    a1 = driver.find_elements_by_css_selector('#fusion-app > div.article > div:nth-child(2) > div')[0]
    
    # 기사 제목
    a2 = a1.find_elements_by_css_selector('h1')[0].text
    # print(a2[1:4])
    
    # [김대중 칼럼]으로 시작하는 기사 제목을 가진 기사는 댓글이 없음
    if a2[1:4] == '김대중':
        return False
    else:

        # 기사 날짜
        a3 = a1.find_elements_by_css_selector('div.article-dateline > span')[0].text
        # print(a3)

        # 댓글 태그(div.comment-feed) 들고오기
        a4 = a1.find_elements_by_css_selector('section > article > div:nth-child(14) > section > div > div')[0]
        # print(a4)

        # 댓글 유무 확인을 위한 태그
        a5 = a4.find_elements_by_css_selector('div')
        # print(len(a5))

        if len(a5) < 5 :    
            print('댓글 없음')
            return False
        else:        
            # 댓글이 포함되어 있는 div.comment-card-wrapper 태그 들고오기
            a6 = a4.find_elements_by_css_selector('div.comment-card-wrapper')

            for a7 in a6:

                # 작성시간
                a8 = a7.find_elements_by_css_selector('div.comment-card-daterow')[0].text
                # print(f'작성시간 : {a8}')

                # 댓글내용
                a9 = a7.find_elements_by_css_selector('div.comment-card-contentrow')[0].text
                # 댓글이 있으면
                if a9:
                    #print(f'댓글 내용 : {a9}')

                    # 제목, 날짜, 작성일, 댓글 딕셔너리에 추가
                    comment_dict['제목'].append(a2)
                    comment_dict['날짜'].append(a3)
                    comment_dict['작성일'].append(a8)
                    comment_dict['댓글'].append(a9)

                    # 댓글의 답글
    #                 more_button = a7.find_elements_by_css_selector('div.comment-card-replyrow > button')[0]
    #                 more_button.send_keys('\n')
    #                 time.sleep(1)
    #                 print('클릭')

                    #a10 = a4.find_elements_by_css_selector('div.comment-feed--reply')
                   # print(a10)

       #             # 댓글이 포함되어 있는 div.comment-card-wrapper 태그 들고오기
       #     a6 = a4.find_elements_by_css_selector('div.comment-card-wrapper')
       #             a10 = a7.find_elements_by_css_selector('div.comment-card-replyrow')[0].text
                    #print(f'답글 유무 : {a10}')
       #             if '작성' not in a10:           
       #                 print('답글 있음')

                        # 답글 보기 클릭
        #                more_button = a7.find_elements_by_css_selector('div.comment-card-replyrow')[0]
        #                more_button.send_keys('\n')


            df1 = pd.DataFrame(comment_dict)
            df1['날짜'] = [date.split('입력')[-1].split('| 수정')[0].strip() for date in df1['날짜']]
            df1['날짜'] = pd.to_datetime(df1['날짜'])
            df1['작성일'] = pd.to_datetime(df1['작성일'])
            display(df1)

            FILENAME = 'chosun_comment.csv'
            if os.path.exists(FILENAME) == False:
                # 파일이 없을 경우
                df1.to_csv(FILENAME, encoding='utf-8-sig', index=False)
            else:
                # mode='a' : 기존 것 뒤에다 붙여줌
                df1.to_csv(FILENAME, encoding='utf-8-sig', index=False, header=False, mode='a')

            return 1


# In[ ]:


def getChosunComment(link_df):
    
    from selenium import webdriver as wd
    from IPython.display import clear_output
    
    num_link = link_df.shape[0]
    # print(link_df.loc[0])

    # 웹 드라이버
    driver = wd.Chrome('./chromedriver.exe')
    idx = 0

    while True :

        driver.implicitly_wait(20)

        clear_output(wait=True)

        driver.get(link_df.loc[idx].values[0])
        clickMore(driver)

        print(f'{idx}번째 기사 댓글 수집 중')

        chk = getComment(driver)

        # 기사에 댓글 데이터 정상 수집
        if chk == 1:
            print(f'{idx}번째 기사 댓글 정상 수집 완료')
        # 기사에 댓글 데이터가 없으면 다음 페이지로 
        else:
            print(f'{idx}번째 기사 댓글 없음, 다음 기사로~')

        idx = idx + 1

        if idx == num_link :
            break

    print('수집완료')


# In[ ]:




