#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 더보기 계속 클릭하기
def clickMore(driver):
    import time 
    
    while True:
        try:
            more_button = driver.find_element_by_css_selector('#spinTopLayerCommentListMore')
            more_button.click()
            time.sleep(1)
        except:
            break


# In[3]:


# 한 기사의 댓글 추출
def getComment(driver):
    
    import os
    import time
    import pandas as pd
    
    # 데이터를 담을 딕셔너리
    comment_dict = {
        '제목' : [],
        '날짜' : [],
        '작성일' : [],
        '댓글' : []
    }
    
    # 기사 제목 태그
    a0 = driver.find_elements_by_css_selector('#container > div.article_title')[0]
    
    # 기사 제목
    data1 = a0.find_elements_by_css_selector('h1')[0].text
    # print(data1)
    
    # 날짜 
    data2 = a0.find_elements_by_css_selector('div.title_foot > span.date01')[0].text
    # print(data2)
    
    # 댓글 태그
    a3 = driver.find_elements_by_css_selector('#content > div > div.reply_box > div.reply_top')[0]
    
    # 댓글 수
    a4 = a3.find_elements_by_css_selector('#replyCnt2')[0].text
    # print(a4)
    
    # 댓글 수가 0이면 False 반환
    if not a4:
        print('댓글 없음')
        return False
    
    # 댓글 수가 0이 아니면
    else:
        # 댓글 태그들
        a5 = driver.find_elements_by_css_selector('#spinTopLayerCommentList > li')
        
        # 댓글 수만큼 반복
        for a6 in a5:
            
            # 댓글 내용이 든 태그
            a7 = a6.find_elements_by_css_selector('div.module')[0]
            
            # 작성일 
            data3 = a7.find_elements_by_css_selector('div.createdate')[0].text
            # print(a8)
            
            # 내용
            data4 = a7.find_elements_by_css_selector('div.comment')[0].text
            # print(a9)
            
            comment_dict['제목'].append(data1)
            comment_dict['날짜'].append(data2)
            comment_dict['작성일'].append(data3)
            comment_dict['댓글'].append(data4)
            
            # 댓글달기 답글 수
            a10 = a7.find_elements_by_css_selector('div.reply')[0].text[1]
            # print(a10)
            
            # 답글 유무 확인
            if int(a10) > 0:
                
                # 댓글 보기 클릭
                more_button = a7.find_elements_by_css_selector('div.operation > div.notify > a')[0]
                more_button.send_keys('\n')
                time.sleep(1)
                
                # 대댓글 리스트
                a11 = a7.find_elements_by_css_selector('div.etc > div.spinTopLayerReplyList > ul > li')
                # print(a11)
                
                for a12 in a11:
                    
                    # 작성일
                    data3 = a12.find_elements_by_css_selector('div.module > div.createdate')[0].text
                    # print(data3)
                    
                    # 댓글 
                    data4 = a12.find_elements_by_css_selector('div.module > div.comment')[0].text
                    # print(data4)                    
                    
                    comment_dict['제목'].append(data1)
                    comment_dict['날짜'].append(data2)
                    comment_dict['작성일'].append(data3)
                    comment_dict['댓글'].append(data4)
                   
        df1 = pd.DataFrame(comment_dict)
        df1['날짜'] = [date.split('입력')[-1].split('수정')[0].strip()                        for date in df1['날짜']]
        df1['날짜'] = pd.to_datetime(df1['날짜'])
        df1['작성일'] = pd.to_datetime(df1['작성일'])
        display(df1)

        FILENAME = 'donga_comment.csv'
        if os.path.exists(FILENAME) == False:
            # 파일이 없을 경우
            df1.to_csv(FILENAME, encoding='utf-8-sig', index=False)
        else:
            # mode='a' : 기존 것 뒤에다 붙여줌
            df1.to_csv(FILENAME, encoding='utf-8-sig', index=False, header=False, mode='a')
 
        return True


# In[ ]:


def getDongaComment(link_df):
    
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
        driver.refresh()
        clickMore(driver)

        print(f'{idx}번째 기사 댓글 수집 중')

        chk = getComment(driver)

        # 기사에 댓글 데이터 정상 수집
        if chk:
            print(f'{idx}번째 기사 댓글 정상 수집 완료')
        # 기사에 댓글 데이터가 없으면 다음 페이지로 
        else:
            print(f'{idx}번째 기사 댓글 없음, 다음 기사로~')

        idx = idx + 1

        if idx == num_link :
            break

    print('수집 테스트 완료')

