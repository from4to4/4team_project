#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 더보기 계속 클릭하기
def clickMore(driver):
    while True:
        try:
            more_button = driver.find_element_by_css_selector('#comment > div.ft > a')
            more_button.click()
            time.sleep(1)
        except:
            break


# In[14]:


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
    
    # 기사 제목 태그
    a0 = driver.find_elements_by_css_selector('#article_title')
    # print(a0)
    
    if not a0:
        print('댓글없음')
        return False
    
    else:
        # 기사 제목 태그
        data1 = a0[0].text
        # print(data1)
        
        # 날짜
        data2 = driver.find_elements_by_css_selector('div.article_head > div > div.byline')[0].text
        # print(data2)
    
        # 댓글 갯수 확인
        a0 = driver.find_element_by_css_selector('#comment > div.hd > strong > span').text
        # print(a0)
        
        # 댓글 수가 0이면
        if a0 == '0':
            print('댓글 없음')
            return False
        else:
            # 댓글이 담긴 ul 태그 들고오기 
            a1 = driver.find_elements_by_css_selector('#comment > div.bd > div.comment_list > ul > li')
            # print(a1)

            for a2 in a1:

                a22 = a2.find_elements_by_css_selector('div')

                # 제목 & 날짜 저장
                comment_dict['제목'].append(data1) 
                comment_dict['날짜'].append(data2) 

                # 댓글 작성일
                a3 = a2.find_elements_by_css_selector('div > div.cmt_area > dl > dt > span')[0].text
                comment_dict['작성일'].append(a3)
                # print(a3)

                # 댓글 
                a4 = a2.find_elements_by_css_selector('div > div.cmt_area > dl > dd > p')[0].text
                comment_dict['댓글'].append(a4)
                # print(a4)

                # 댓글에 댓글이 있는 경우
                if len(a22) > 5 :

                    # 댓글의 댓글이 담긴 div
                    a5 = a2.find_elements_by_css_selector('div.reply_area > ul > li')
                    # print(len(a5))

                    for a6 in a5:

                        # 제목 & 날짜
                        comment_dict['제목'].append(data1) 
                        comment_dict['날짜'].append(data2) 

                        # 댓글작성일
                        a7 = a6.find_elements_by_css_selector('div > dl > dt > span')[0].text
                        # print(a7)
                        comment_dict['작성일'].append(a7)

                        # 댓글
                        a8 = a6.find_elements_by_css_selector('div > dl > dd > p')[0].text
                        # print(a8)
                        comment_dict['댓글'].append(a8)

            df1 = pd.DataFrame(comment_dict)
            df1['날짜'] = [date.split('입력')[-1].split('수정')[0].split('|')[0].strip()                            for date in df1['날짜']]
            df1['날짜'] = pd.to_datetime(df1['날짜'])
            df1['작성일'] = pd.to_datetime(df1['작성일'])

            display(df1)
            
            FILENAME = 'joongang_comment.csv'
            if os.path.exists(FILENAME) == False:
                # 파일이 없을 경우
                df1.to_csv(FILENAME, encoding='utf-8-sig', index=False)
            else:
                # mode='a' : 기존 것 뒤에다 붙여줌
                df1.to_csv(FILENAME, encoding='utf-8-sig', index=False, header=False, mode='a')

            return True


# In[15]:


# 뉴스 댓글 가져오는 함수
def getJoongangComment(link_df, idx=0):
    
    import pandas as pd
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
        # print(f'chk : {chk}')
        
        # 기사에 댓글 데이터 정상 수집
        if chk:
            print(f'{idx}번째 기사 댓글 정상 수집 완료')
        # 기사에 댓글 데이터가 없으면 다음 페이지로 
        else:
            print(f'{idx}번째 기사 댓글 없음, 다음 기사로~')

        idx = idx + 1

        if idx == num_link :
            break

    print('수집완료')


# In[17]:


test = False
if test:
    import pandas as pd
    from selenium import webdriver as wd
    from IPython.display import clear_output

    df = pd.read_csv('../중앙일보_link.csv')

    driver = wd.Chrome('./chromedriver.exe')
    idx = 0



    driver.implicitly_wait(20)

    clear_output(wait=True)

    driver.get(df.loc[idx].values[0])
    clickMore(driver)
    getComment(driver)


# In[ ]:




