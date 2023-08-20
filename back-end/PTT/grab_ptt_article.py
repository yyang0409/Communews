
from http import cookies
import requests 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import datetime
import mysql.connector
#import emotion 

current_dir = os.getcwd()
driver_name = "chromedriver.exe"
driver_path = current_dir+"\\"+driver_name

host = 'communews.ctqdwhl8sobn.us-east-1.rds.amazonaws.com'
user = 'mysqluser'
password = 'mysqluser'
#host = '127.0.0.1'
#user = 'root'
#password = '109403502'
database = 'communews'
charset =  "utf8"


#這一邊要改成輸出到資料庫 需要輸出到 存放ptt內容的資料庫
def transfer_dictionary(sub_topics,titles,content,links,dates,page_indexes,emotion_scores):
   
    data_list = []
    for sub_topic,title,content,link,date,page_index in zip(sub_topics,titles,content,links,dates,page_indexes):
        data_list.append({'subtopic':sub_topic,'title':title,'content':content,'link':link,'date':date,'page':int(page_index)},)
    #print(data_list)
    return data_list

#將ptt網址的字串進行處理
def split_ptt_link(URL,already_get_index):
    split_url = URL.split("index")
    base_url = split_url[0]
    page_index = split_url[1].rstrip(".html")

    print("Base URL:", base_url)  
    print("Page Number:", page_index)  

    if int(page_index)>already_get_index:
        return True,page_index
    else:
        return False,page_index


def renew_ptt_subtopic_table_to_database(ptt_renewed_link_list):
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)
    cursor = connection.cursor()
    for ptt_renewed_link in ptt_renewed_link_list:

        # SQL更新语句
        update_query = "UPDATE tb_ptt_search_link SET page = %s WHERE id_ptt_link = %s"

        # 执行更新
        data = ( ptt_renewed_link['page'],ptt_renewed_link['id_ptt_link'])
        cursor.execute(update_query, data)

        # 提交更改
        connection.commit()

    # 关闭连接
    connection.close()


def transfer_date_type(date_str):
    month, day = map(int, date_str.split('/'))
    current_datetime = datetime.datetime.now()

    # 从当前日期和时间中提取年份信息
    current_year = current_datetime.year
    # 使用指定的年份与月份、日期组合成新的日期
    new_date = datetime.date(current_year, month, day)

    # 将新的日期转换为字符串，格式为'YYYY-MM-DD'
    new_date_str = new_date.strftime('%Y-%m-%d')

    return new_date_str

def renew_ptt_subtopic_table_index(id_ptt_link,id_subtopic,subtopic,URL,page_index):
    dic = {'id_ptt_link':id_ptt_link,'id_subtopic':id_subtopic,'subtopic':subtopic,'ptt_url':URL,'page':page_index}
    return dic

def is_gossiping(id_subtopic):
    if id_subtopic==30:
        return True
    return False



def grab_ptt_article_everyday(df_ptt_subtopic):
    sub_topics=[]
    titles=[]
    links=[]
    dates=[]
    page_indexes=[]
    emotion_scores=[]
    ptt_content=[]

    new_list_ptt_subtopic = []
    
    options = webdriver.ChromeOptions()  
    prefs = {'profile.default_content_setting_values':{'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)
    # 設定Cookie（必要時，用以通過年齡驗證）
    cookies = {'over18': '1'}
    for id_ptt_link, id_subtopic, subtopic, URL, already_get_index in zip (df_ptt_subtopic['id_ptt_link'],df_ptt_subtopic['id_subtopic'],df_ptt_subtopic['subtopic'],df_ptt_subtopic['ptt_url'],df_ptt_subtopic['page']):
        count=1
        driver.get(URL)
        time.sleep(2)
        is_search_next_page = True
        while(is_search_next_page==True):
            if count==1 and is_gossiping(id_subtopic) :
                time.sleep(1)
                elem_yes = (driver.find_element(By.XPATH, '//html/body/div[2]/form/div[1]/button'))
                time.sleep(1)
                ActionChains(driver).click(elem_yes).perform()
                time.sleep(1)

            elem_last_page =  driver.find_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]')
            time.sleep(1)
            ActionChains(driver).click(elem_last_page).perform()
            time.sleep(3)
            current_url =driver.current_url
            is_search_next_page,page_index = split_ptt_link(current_url,already_get_index)

            elem_titles = driver.find_elements(By.CSS_SELECTOR, '#main-container > div> div> div.title >a')
            elem_dates = driver.find_elements(By.CSS_SELECTOR, '#main-container > div > div> div> div.date')
            elem_links = driver.find_elements(By.CSS_SELECTOR, '#main-container > div> div> div.title > a')
            if(count==1):
                new_list_ptt_subtopic.append(renew_ptt_subtopic_table_index(id_ptt_link,id_subtopic,subtopic,URL,page_index))
                count+=1
            print("這是關於"+subtopic+"的新聞：")
            
            if(is_search_next_page==True):
                for title,date,link in zip (elem_titles,elem_dates,elem_links):
                    try :
                        sub_topics.append(subtopic)
                        titles.append(title.text)
                        links.append(link.get_attribute('href'))
                        transfer_date = transfer_date_type(date.text)
                        dates.append(transfer_date)
                        page_indexes.append(page_index)
                        print("標題是"+title.text)
                        # 新增以下程式碼進行內文爬取
                        content_response = requests.get(link.get_attribute('href'), cookies=cookies)
                        content_soup = BeautifulSoup(content_response.text, 'html.parser')
                        content_element = content_soup.find(id='main-content')
                        # 移除掉文章中的推文部分
                        for push in content_element.find_all(class_='push'):
                            push.extract()
                        # 移除掉不是內文的資訊
                        for elem in content_element(['div', 'span']):
                            elem.extract()
                        # 印出內文
                        content = content_element.text.strip()
                        ptt_content.append(content)
                    except:
                        pass
    datalist = transfer_dictionary(sub_topics,titles,ptt_content,links,dates,page_indexes,emotion_scores)
    #將更新到的頁數傳回至資料庫
    return datalist,new_list_ptt_subtopic


def read_ptt_data(index):
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)

    cursor = connection.cursor()

    # SQL查询语句
    select_query = "SELECT * FROM tb_ptt_search_link WHERE id_ptt_link = %s"

    # 执行查询
    
    cursor.execute(select_query,(index,))

    # 获取所有结果
    result = cursor.fetchall()

    # 将结果转换为DataFrame
    ptt_link_df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    print("我從資料庫把ptt_link的資訊抓出來了")

    # 打印DataFrame
    print(ptt_link_df)

    # 关闭连接
    connection.close()

    return ptt_link_df
    

def update_ptt_data():
    index=1
    while (index<=126):
        ptt_link_df = read_ptt_data(index)

        connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)

        cursor = connection.cursor()

        messages,new_list_ptt_subtopic = grab_ptt_article_everyday(ptt_link_df)
        print(messages)
        for message in messages:
            insert_query = '''
                INSERT INTO tb_ptt_data (subtopic, title, content, link, date, page)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            data = (message['subtopic'], message['title'],message['content'], message['link'], message['date'], message['page'])

            cursor.execute(insert_query, data)

        renew_ptt_subtopic_table_to_database(new_list_ptt_subtopic)
        index=index+1
        connection.commit()

    connection.close()




#爬取ptt資料
update_ptt_data()

    


    






