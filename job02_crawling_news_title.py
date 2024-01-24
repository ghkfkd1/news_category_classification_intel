from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException # 주소 안맞을 때 대처?
from selenium.common.exceptions import StaleElementReferenceException #로딩 오래걸리는거 대처
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
pages = [105, 105, 105, 81, 105, 81]

df_titles = pd.DataFrame()
for l in range(1):
    section_url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(l)
    titles = []
    for k in range(1, pages[l]): #(1, 3): 페이지 1부터 2까지
        url = section_url + '#&date=%2000:00:00&page={}'.format(k)
        try:
            driver.get(url)
            time.sleep(0.5)
        except:
            print('driver.get', l, k) # 에러 확인

        for i in range(1, 5):
            for j in range(1, 6):
                try:
                    title = driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i, j)).text
                    title = re.compile('[^가-힣]').sub(' ', title)
                    titles.append(title)
                except:
                    print('find element', l, k, i, j)# 에러 확인. 에러 나도 건너뛰고 계속 크롤링 가능.
        if k % 5 == 0:
            print(l, k)
            #print(titles)
            #print(len(titles))
            df_section_title = pd.DataFrame(titles, columns=['titles'])
            df_section_title['category'] = category[l]
            df_section_title.to_csv('./crawling_data/data_{}_{}.csv'.format(l, k))
        #df_titles = pd.concat([df_titles, df_section_title], axis='row', ignore_index=True)

#df_titles.to_csv()
driver.close() #브라우저 닫음.