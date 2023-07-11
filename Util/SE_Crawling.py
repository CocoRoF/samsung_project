# Library Import

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time
import datetime

def Crawling(Num_data, Data_length, Save=False, save_name=''):
    
    # 크롤링 시 조절파라미터
    num_data = Num_data # 얼마나 많은 데이터를 가져올지 결정함.
    date_length = Data_length # 현재 시점으로부터 몇 일 전까지의 데이터만 출력할지 결정함.
    Save_ = Save # 엑셀파일로 세이브 여부

    # Set Chrome Driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    print(f'Chrome_Driver Start. 데이터 길이 = {num_data}, 데이터 기간 = {date_length}, 저장여부 = {Save_}')
    
    # Set Url - DataSource.
    url_nodong = 'http://nodong.org/index.php?mid=statement&page='
    url_chosun_politics = 'https://biz.chosun.com/politics/'
    url_chosun_topics = 'https://biz.chosun.com/topics/'
    url_labortoday = 'http://www.labortoday.co.kr/news/articleList.html?page='
    url_newsis = 'https://newsis.com/soci/list/?cid=10200&scid=10221&page='
    url_kcwu = 'https://www.kcwu.or.kr/index.php?mid=statement&page='
    url_krwu = 'http://krwu.nodong.net/bbs/board.php?bo_table=s4_6&page='
    url_unsunozo = 'https://www.unsunozo.org/report?page='

    # 전체 데이터를 종합하는 df 형성.
    df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])

    # Nodong(민노총)기사 제목 크롤링
    print('민노총-성명/보도 데이터 크롤링. Start.')
    for num in range(num_data):
        num_ = num+1
        video_url_Nodong = url_nodong + str(num_)
        driver.get(video_url_Nodong)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        item = soup.select('li.clear')
        for i in item:
            i = str(i)
            title = i.split('"ngeb">')[1]
            title = title.split('</h3')[0]
            date = i.split('Date</span><b>')[1]
            date = date.split('</b></span>')[0]
            url = i.split('data-viewer="')[1]
            url = url.split('&amp;listStyle=viewer"')[0]
            url = 'http://nodong.org' + url
            temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
            temp_df.loc[0, 'Title'] = title
            temp_df.loc[0, 'Date'] = date
            temp_df.loc[0, 'URL'] = url
            temp_df.loc[0, 'Source'] = '전국민주노동조합총연맹'
            df = pd.concat([df, temp_df], ignore_index=True)
    print('민노총 기사데이터 크롤링. End.')

    # 조선일보 정치 기사 제목 크롤링
    print('조선일보-정치 기사데이터 크롤링. Start.')
    driver.get(url_chosun_politics)
    time.sleep(3)
    button = driver.find_element(By.XPATH, '//*[@id="load-more-stories"]')
    for repeat in range(num_data*3):
        button.click()
        time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    item = soup.select("div.grid__col--sm-8.grid__col--md-8.grid__col--lg-8")
    for j, i in enumerate(item):
        i = str(i)
        if j >=3:
            title = i.split('/"><span>')[1]
            title = title.split('</span></a></div><div')[0]
            url = i.split('link--color" href="')[1]
            url = url.split('"><span>')[0]
            url = 'https://biz.chosun.com' + url
            date = i.split('pre">')[1]
            date = date.split('</div></div><span')[0]
            if '시간 전' in date:
                date = str(datetime.datetime.now().strftime("%Y.%m.%d"))
            else:
                date = date.split('(')[0]
            temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
            temp_df.loc[0, 'Title'] = title
            temp_df.loc[0, 'Date'] = date
            temp_df.loc[0, 'URL'] = url
            temp_df.loc[0, 'Source'] = '조선일보_정치'
            df = pd.concat([df, temp_df], ignore_index=True)
    print('조선일보-정치 기사데이터 크롤링. End.')

    # 조선일보 사회 기사 제목 크롤링
    print('조선일보-사회 기사데이터 크롤링. Start.')
    driver.get(url_chosun_topics)
    time.sleep(3)
    button = driver.find_element(By.XPATH, '//*[@id="load-more-stories"]')
    for repeat in range(num_data*3):
        button.click()
        time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    item = soup.select("div.grid__col--sm-8.grid__col--md-8.grid__col--lg-8")
    for j, i in enumerate(item):
        i = str(i)
        if j >=3:
            title = i.split('/"><span>')[1]
            title = title.split('</span></a></div><div')[0]
            url = i.split('link--color" href="')[1]
            url = url.split('"><span>')[0]
            url = 'https://biz.chosun.com' + url
            date = i.split('pre">')[1]
            date = date.split('</div></div><span')[0]
            if '시간 전' in date:
                date = str(datetime.datetime.now().strftime("%Y.%m.%d"))
            else:
                date = date.split('(')[0]
            temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
            temp_df.loc[0, 'Title'] = title
            temp_df.loc[0, 'Date'] = date
            temp_df.loc[0, 'URL'] = url
            temp_df.loc[0, 'Source'] = '조선일보_사회'
            df = pd.concat([df, temp_df], ignore_index=True)
    print('조선일보-사회 기사데이터 크롤링. End.')

    # 매일노동뉴스 노동조합 기사 제목 크롤링
    print('매일노동뉴스-노동조합 기사데이터 크롤링. Start.')
    for num in range(num_data):
        num_ = num+1
        article_url_labortoday = url_labortoday + str(num_) + '&sc_sub_section_code=S2N3&view_type=sm'
        driver.get(article_url_labortoday)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        item = soup.select('ul.type2')
        item = str(item)
        item = item.split('</li>')
        del item[-1]
        for i in item:
            date = i.split('class="byline">\n<em>')[1]
            date = date.split(' ')[0]
            url = i.split('href="')[1]
            url = url.split('" target=')[0]
            url = 'www.labortoday.co.kr' + url
            if '<img alt="" src="' in i:
                title = i.split('target="_top">')[2]
                title = title.split('</a></h4>\n<p')[0]
            else:
                title = i.split('target="_top">')[1]
                title = title.split('</a></h4>\n<p')[0]
            temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
            temp_df.loc[0, 'Title'] = title
            temp_df.loc[0, 'Date'] = date
            temp_df.loc[0, 'URL'] = url
            temp_df.loc[0, 'Source'] = '매일노동뉴스'
            df = pd.concat([df, temp_df], ignore_index=True)
    print('매일노동뉴스-노동조합 기사데이터 크롤링. End.')

    # 뉴시스 사회-노동 기사 제목 크롤링
    print('뉴시스-사회-노동 기사데이터 크롤링. Start.')
    for num in range(num_data):
        num_ = num+1
        video_url_Newsis = url_newsis + str(num_)
        driver.get(video_url_Newsis)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        item = soup.select('div.txtCont')
        for i in item:
            i = str(i)
            if 'class="tit">' and 'class="txt">' and 'class="time">' in i:
                temp_str = i.split('<a href="')[1]
                temp_str = temp_str.split('</a>')[0]
                url = temp_str.split('">')[0]
                url = 'https://newsis.com' + url
                title = temp_str.split('">')[1]
                date = i.split('</span>')[1]
                date = date.split(' ')[0]
                temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
                temp_df.loc[0, 'Title'] = title
                temp_df.loc[0, 'Date'] = date
                temp_df.loc[0, 'URL'] = url
                temp_df.loc[0, 'Source'] = '뉴시스'
                df = pd.concat([df, temp_df], ignore_index=True)
    print('뉴시스-사회-노동 기사데이터 크롤링. End.')

    # 전국건설노조-성명/보도 자료 크롤링
    print('전국건설노조-성명/보도 자료 크롤링. Start.')
    for num in range(num_data):
        num_ = num+1
        article_url_kcwu = url_kcwu + str(num_)
        driver.get(article_url_kcwu)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        item = soup.select('tr')
        for i in item[1:]:
            i = str(i)
            try:
                title = i.split('">')[3].split('</a>')[0]
                date = i.split('class="date">')[1].split('</td')[0]
                url = i.split('href="')[1].split('">')[0].replace('amp;', '')
                temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
                temp_df.loc[0, 'Title'] = title
                temp_df.loc[0, 'Date'] = date
                temp_df.loc[0, 'URL'] = url
                temp_df.loc[0, 'Source'] = '전국건설노동조합'
                df = pd.concat([df, temp_df], ignore_index=True)
            except:
                continue
    print('전국건설노조-성명/보도 자료 크롤링. End.')

    # 전국철도노동조합-성명/보도 자료 크롤링 
    print('전국철도노동조합-성명/보도 자료 크롤링. Start.')
    for num in range(num_data):
        num_ = num+1
        article_url_krwu = url_krwu + str(num_)
        driver.get(article_url_krwu)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        item = soup.select('div.div_tb_tr')
        for i in item[1:]:
            i = str(i)
            try:
                title = i.split('">')[4].split('\n\t\t\t\t\t\t\t\t')[1].split('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')[0]
                date = i.split('col_date">')[1].split('</div>')[0]
                url = i.split('">')[3].split('href="')[1].split('&amp;page')[0].replace('amp;', '')
                temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
                temp_df.loc[0, 'Title'] = title
                temp_df.loc[0, 'Date'] = date
                temp_df.loc[0, 'URL'] = url
                temp_df.loc[0, 'Source'] = '전국철도노동조합'
                df = pd.concat([df, temp_df], ignore_index=True)
            except:
                continue
    print('전국철도노동조합-성명/보도 자료 크롤링. End.')

    # 화물연대본부-성명/보도 자료 크롤링 
    print('화물연대본부-성명/보도 자료 크롤링. Start.')   
    for num in range(num_data):
        num_ = num+1
        article_url_unsunozo = url_unsunozo + str(num_)
        driver.get(article_url_unsunozo)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        item = soup.select('tr.even')
        for i in item[1:]:
            i = str(i)
            try:
                title = i.split('">')[5].split('\n                                                                        ')[1].split('                    </a>')[0]
                date = i.split('td_datetime">')[1].split('</td>')[0]
                url = i.split('href="')[1].split('">')[0]
                temp_df = pd.DataFrame(columns = ['Title', 'Date', 'URL', 'Source'])
                temp_df.loc[0, 'Title'] = title
                temp_df.loc[0, 'Date'] = date
                temp_df.loc[0, 'URL'] = url
                temp_df.loc[0, 'Source'] = '화물연대본부'
                df = pd.concat([df, temp_df], ignore_index=True)
            except:
                continue
    print('화물연대본부-성명/보도 자료 크롤링. End.')   

    # 전체 병합 및 특정 키워드 처리과정
    
    # df['Date'] = pd.to_datetime(df['Date'])
    datetime_now = datetime.datetime.now().strftime("%Y%m%d")
    datetime_before = datetime.datetime.now() - timedelta(date_length)
    datetime_before = datetime_before.strftime("%Y-%m-%d")
    # df = df[df['Date'] >= datetime_before]
    df.reset_index(inplace=True, drop=True)
    df['Marking'] = 0
    df.loc[df['Title'].str.contains('노조|파업'), 'Marking']= 1
    df.loc[df['Title'].str.contains('건설|건설노조|건설파업'), 'Marking']= 2
    df.loc[df['Title'].str.contains('운송|화물연대|운송파업'), 'Marking']= 3
    df.loc[df['Title'].str.contains('철도|철도노조|철도파업'), 'Marking']= 4
    df.loc[df['Title'].str.contains('타워크레인|타워크레인 노조|타워크레인 파업'), 'Marking']= 5
    
    if Save_ == True:
        df.to_excel('./Article_{}_{}.xlsx' .format(datetime_now, save_name), index=False)
        print('Save Success')
        
    print('Crawling End')
    return df