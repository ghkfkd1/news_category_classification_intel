import pandas as pd
from bs4 import BeautifulSoup  #pip install bs4
import requests
import re
import pandas as ps
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'


#headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"} #네이버가 크롤링 막았을 때 대처법.
#resp = requests.get(url, headers=headers) # 요청하는건 클라이언트 요청하면 응답하는게 서버


#print(resp)
#print(type(resp))
#print(list(resp))

#soup = BeautifulSoup(resp.text, 'html.parser') #html 형태로 바꿔줌
#print(soup)
#title_tags = soup.select('.sh_text_headline') #sh_text_headline클래스를 가진 애들은 리턴
#print(title_tags)
#print(len(title_tags))
#print(type(title_tags[0]))
#titles = []
#for title_tag in title_tags:
#    titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text)) #^가-힣|a-z|A-Z 한글 영어를 제외한 나머지를 빼고 ' '로 채움
#print(titles)
#
df_titles = pd.DataFrame() #빈 데이터 프레임 생성
re_title = re.compile('[^가-힣|a-z|A-Z]')
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"} #네이버가 크롤링 막았을 때 대처법.

for i in range(6): # 0부터 5까지
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url,headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    for title_tag in title_tags:
        titles.append(re_title.sub(' ', title_tag.text))
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
# 현재시간 받아서 %Y%m%d 연 월 일 붙어서 오늘 날짜 제목에 붙음. strftime:문자열로 변환