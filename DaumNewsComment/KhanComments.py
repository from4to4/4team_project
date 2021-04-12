#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 더보기 계속 클릭하기
def clickMore(driver):
    
    import time
            
   # 댓글 더보기 클릭
    while True :
        try :
            time.sleep(1)
            driver.find_element_by_class_name('more-btn').click()
            # print('클릭')

        except :
            # print('클릭 끝')
            break


# In[3]:


# 댓글 iframe 가져오는 함수
def getCommentIframe(driver):
    
    import time
    
    # 댓글 iframe이 없을 경우 처리가가 복잡해지니 iframe이 나올 때 까지 반복한다.
    chk = True

    while chk :
        time.sleep(1)

        # 원하는 기사를 요청한다.

        # 가장 아래로 스크롤 한다.
        # 스크롤을 해야 댓글이 나옴
        driver.execute_script("window.scrollTo(0, 50000)") 

        # iframe들을 모두 가져온다.
        iframe_list = driver.find_elements_by_tag_name('iframe')

        # iframe의 수 만큼 반복한다.
        for a1 in iframe_list :
            # iframe의 title 속성값을 가져온다.
            title1 = a1.get_attribute('title')

            # title 속성값이 livere-comment 라면 src 속성을 추출한다.
            if title1 == 'livere-comment' :
                src1 = a1.get_attribute('src')
                # print(src1)
                
                # 댓글 iframe을 발견하였으므로 while이 종료될 수 있게 한다.
                chk = False
                
    return src1


# In[4]:


# 정치기사와 경제기사의 기사 제목 id가 다름
# 정치기사인지 확인하는 함수
def isPolitical(driver):
    
    from selenium.common.exceptions import NoSuchElementException
    
    try:
        # 정치기사인 경우
        a1 = driver.find_element_by_css_selector('#article_title')
        # print('정치기사입니다')
        return True
    # 예외가 발생했을 때 실행됨
    except NoSuchElementException:     
        # print('정치기사가 아닙니다')
        return False


# In[5]:


# 뉴스 제목과 날짜를 가져오는 함수
def getTitleDate(driver):
    title = driver.find_element_by_css_selector('#article_title').text
    date = driver.find_element_by_css_selector('#container > div.art_header.borderless > div.function_wrap > div.pagecontrol > div > em').text
    #articleTtitle
    return title, date


# In[6]:


# 댓글 유무를 확인하는 함수
def checkComment(driver):

    from selenium.common.exceptions import NoSuchElementException

    try:
        # 댓글이 없는 경우를 알리는 태그
        a1 = driver.find_element_by_css_selector('#list > div.noreply-wrapper')
        # print(a1.text)
        return False
    # 예외가 발생했을 때 실행됨
    except NoSuchElementException:     
        # print('해당 요소가 없습니다')
        return True


# In[7]:


# 댓글 첫번째에 위치하는 best 댓글이 있는지 여부를 확인하는 함수
def isBestComment(driver):

    from selenium.common.exceptions import NoSuchElementException

    try:
        # 베스트 댓글(댓글 리스트 맨 처음에 존재)이 있으면
        a22 = driver.find_element_by_css_selector('#list > div.reply-wrapper > div.reply-top > div > ul > span').text
        # print('베스트 댓글이 있습니다')
        return True
    except NoSuchElementException:    
        # print('베스트 댓글이 없습니다')
        return False
    


# In[8]:


# 댓글 펼쳐보기 클릭
def clickCommentMore(driver):
    
    import time
    
    while True :
        try :
            time.sleep(1)
            driver.find_element_by_css_selector('#list > div > div.list-reduce > button').click()
            # print('클릭')
        except :
            # print('클릭 끝')
            break


# In[9]:


# 블라인드된 답글 보기
def clickReply(button):
    
    import time
    from selenium.webdriver.common.keys import Keys

    while True :
        try :
            time.sleep(1)
            button.send_keys(Keys.ENTER)
            # print('클릭')
        except :
            # print('클릭 끝')
            break


# In[10]:


def getData(driver):
    
    import os
    import pandas as pd
    
    data1, data2 = getTitleDate(driver)
    # print(title)
    # print(date)

    src = getCommentIframe(driver)
    driver.get(url=src)
    # print('-'*30)

    # 댓글이 있는지 확인
    if not checkComment(driver):
        # 댓글이 없으면
        print('댓글 없음')
        return False
    else:
        # 댓글이 있으면
        # print('댓글이 있습니다.')

        # 댓글을 담을 딕셔너리 생성
        comment_dict = {
            '제목' : [],
            '날짜' : [],
            '작성일' : [],
            '댓글' : []
        }

        # 댓글수
        a1 = driver.find_element_by_css_selector('#wrapper > div.reply-count > div.left > span').text
        # print(a1)

        # 댓글 더보기 클릭 수행
        clickMore(driver)

        # 댓글 펼쳐보기 클릭
        clickCommentMore(driver)

        # 댓글 리스트 가져오기
        a2 = driver.find_elements_by_css_selector('#list > div.reply-wrapper')
        # print(len(a2))

        # 베스트 댓글이 있으면
        if isBestComment(driver):
            # 댓글 리스트의 첫번째 댓글을 제거함
            a2 = a2[1:]

        # 댓글 수만큼 반복
        for i, a3 in enumerate(a2):
            # print(f'{i}번째 댓글 입니다')

            # 답글 문구 확인
            a66 = a3.find_element_by_css_selector('div.reply-bottom > div.reply-content-wrapper > div.reply-btn-group > div.left > button')
            # print(a66)

            # 답글 클릭 문구가 '댓글보기'면
            if a66.text == '댓글보기':
                # 댓글보기 버튼 클릭
                clickReply(a66)

            # 답글 수 확인
            a6 = a3.find_element_by_css_selector('div.reply-bottom > div.reply-content-wrapper > div.reply-btn-group > div.left > button > span.comment-count')

            # 작성자
            data3 = a3.find_element_by_css_selector('div.reply-top > div > ul > li.writer-name > button > span').text    

            # 작성일
            data4 = a3.find_element_by_css_selector('div.reply-top > div > ul > li.reply-history').text
            # print(a4)

            # 댓글 내용
            data5 = a3.find_element_by_css_selector('div.reply-bottom > div.reply-content-wrapper > div.reply-content > p').text
            # print(a5)

            comment_dict['제목'].append(data1)
            comment_dict['날짜'].append(data2)
            # comment_dict['작성자'].append(data3)
            comment_dict['작성일'].append(data4)
            comment_dict['댓글'].append(data5)

            # 답글 유무 확인
            if a6.text:
                # print('답글이 있습니다')

                a7 = a3.find_elements_by_css_selector('div.child-reply > div')
                for a8 in a7:

                    # 작성자
                    data3 = a8.find_element_by_css_selector('div.reply-top > div > ul > li.writer-name > button > span').text    

                    # 작성일
                    data4 = a8.find_element_by_css_selector('div.reply-top > div > ul > li.reply-history').text
                    # print(a9)

                    # 댓글 내용
                    data5 = a8.find_element_by_css_selector('div.reply-bottom > div.reply-content-wrapper > div.reply-content > p').text
                    # print(a10)

                    comment_dict['제목'].append(data1)
                    comment_dict['날짜'].append(data2)
                    # comment_dict['작성자'].append(data3)
                    comment_dict['작성일'].append(data4)
                    comment_dict['댓글'].append(data5)

    #     print('-'*30)
        # 모든 행을 출력한다
        # pd.set_option('display.max_rows', None) 
        df = pd.DataFrame(comment_dict)
        
        df['날짜'] = df['날짜'].str.replace('입력 :', '')
        df['작성일'] = [date.split('·')[0].strip() for date in df['작성일']]
        idx = df[df['작성일'] == '전'].index 
        df.loc[idx, '작성일'] = df.loc[idx, '날짜']
        df['날짜'] = pd.to_datetime(df['날짜'])
        df['작성일'] = pd.to_datetime(df['작성일'])
        display(df)

        FILENAME = 'khan_comment.csv'
        if os.path.exists(FILENAME) == False:
            # 파일이 없을 경우
            df.to_csv(FILENAME, encoding='utf-8-sig', index=False)
        else:
            # mode='a' : 기존 것 뒤에다 붙여줌
            df.to_csv(FILENAME, encoding='utf-8-sig', index=False, header=False, mode='a')

        return True


# In[ ]:


def getKhanComment(url_list):
    
    import time
    from IPython.display import clear_output
    from selenium import webdriver

    num_link = url_list.shape[0]
    idx = 0
    driver = webdriver.Chrome(executable_path='chromedriver')

    while True:

        # 테스트 하기 좋은 URL
        URL = url_list.iloc[idx].values[0]

        time.sleep(1)        
        clear_output(wait=True)

        driver.get(url=URL)

        if isPolitical(driver):
            print(f'{idx} 댓글 수집 중')
            chk = getData(driver)
            if chk:
                print(f'{idx} 댓글 수집 완료')
            else:
                print(f'{idx} 댓글 없음')

        idx = idx + 1
        if idx == num_link:
            break

    print('댓글 수집 완료')

