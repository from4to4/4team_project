#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 더보기 계속 클릭하기
def clickMore(driver):
    import time
    
    while True:
        try:
            more_button = driver.find_element_by_css_selector('#TCMT_ContBox > div.cmt_add > a')
            # div 태그에 onclick=javascript일 경우
            # [출처] Selenium) click 이 되지 않을때|작성자 데이터공방
            driver.execute_script("arguments[0].click();", more_button)  #자바 명령어 실행
            # more_button.click()
            print('클릭성공')
            time.sleep(1)
        except:
            break


# In[3]:


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
    
    # 기사 제목 & 날짜 태그
    a1 = driver.find_elements_by_css_selector('#articletitle > div')[0]
    
    # 기사 제목
    data1 = a1.find_elements_by_css_selector('h3')[0].text
    # print(data1)
    
    # 날짜 
    data2 = a1.find_elements_by_css_selector('span > span.i_date')[0].text
    # print(data2)
    
    # 댓글 수 
    tCnt = driver.find_elements_by_css_selector('#tCount')[0].text[:-1]
    
    # 댓글 수가 0이면 False 반환
    if int(tCnt) == 0:
        print('댓글 없음')
        return False
    # 0이 아니면 수집 시작
    else:     
        # 댓글 태그들
        a5 = driver.find_elements_by_css_selector('#TCMT_ContBox > div.cmt_sort')
        
        # 댓글 수만큼 반복
        for a6 in a5:
            
            # 댓글 내용이 든 태그
            a7 = a6.find_elements_by_css_selector('div.bd > dl')[0]
            # print(a7)
            
            # 작성자 & 작성일
            data3 = a7.find_elements_by_css_selector('dd.name > span.date')[0].text
            # print(data3)
            
            # 댓글
            data4 = a7.find_elements_by_css_selector('dd.txt > span')[0].text
            # print(data4)
            
            # 답글 수집 제외
            # 쓰여진 답글 찾기 어려움 -> 직접 작성 시도 -> 정상 입력이 되지 않는다는 안내메시지 
            
            comment_dict['제목'].append(data1)
            comment_dict['날짜'].append(data2)
            comment_dict['작성일'].append(data3)
            comment_dict['댓글'].append(data4)
                   
        df1 = pd.DataFrame(comment_dict)
        df1['날짜'] = [date.split('입력')[-1].split('수정')[0].strip()                        for date in df1['날짜']]
        # 작성일 - 오전/오후 텍스트 AM/PM으로 교체
        df1['작성일'] = df1['작성일'].str.replace('오전','AM').str.replace('오후', 'PM')
        # AM/PM을 문자열 끝에 오도록 재배치
        df1['작성일'] = [date.replace('AM', '') + ' AM' if date.find('AM') != -1                           else date.replace('PM', '') + ' PM'                           for date in df1['작성일']]
        df1['날짜'] = pd.to_datetime(df1['날짜'])
        df1['작성일'] = pd.to_datetime(df1['작성일'])
        display(df1)

        FILENAME = 'jtbc_comment.csv'
        if os.path.exists(FILENAME) == False:
            # 파일이 없을 경우
            df1.to_csv(FILENAME, encoding='utf-8-sig', index=False)
        else:
            # mode='a' : 기존 것 뒤에다 붙여줌
            df1.to_csv(FILENAME, encoding='utf-8-sig', index=False, header=False, mode='a')
 
        return True


# In[ ]:


def getJTBCComment(link_df):
    
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

