# 導入 模組(module) 

from datetime import datetime, timedelta
from pymongo import MongoClient
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
from gensim.models import Word2Vec
import jieba
import mysql.connector
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch



current_dir = os.getcwd()
driver_name = "chromedriver.exe"
driver_path = current_dir+"\\"+driver_name

def search_ptt_by_kw(user_keyword,news_datetime):
    host = '127.0.0.1'
    user = 'root'
    password = '109403502'
    database = 'communews'
    charset =  "utf8"
    
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)
    
    cursor = connection.cursor()
    start_date = (news_datetime - timedelta(days=1)).date()
    end_date = (news_datetime + timedelta(days=1)).date()
    # 使用參數化的方式傳遞變數
    select_query = "SELECT * FROM tb_ptt_data WHERE title LIKE %s AND date BETWEEN %s AND %s"
    # 傳遞變數給SQL查詢
    cursor.execute(select_query, (('%' + user_keyword + '%',),start_date,end_date))

    # 结果
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    
    return df



def open_ptt_url_fillter_subtopic(sub_topic,news_datetime):

    host = '127.0.0.1'
    user = 'root'
    password = '109403502'
    database = 'communews'
    charset =  "utf8"
    
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)
    
    cursor = connection.cursor()
    start_date = (news_datetime - timedelta(days=1)).date()
    end_date = (news_datetime + timedelta(days=1)).date()
    # SQL查询语句
    select_query = "SELECT * FROM tb_ptt_data WHERE subtopic = %s AND date BETWEEN %s AND %s"
    # 执行查询
    cursor.execute(select_query,(sub_topic,start_date,end_date))
    # 获取所有结果
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    #print(df)

    return df


def time_sort(df):
    df_sorted = df.sort_values(by='date', ascending=False)

    return df_sorted


model_name = "bert-base-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
def calculate_bert_similarity(summary, title):
    try:
        inputs = tokenizer(summary, title, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
            news_embeddings = outputs.last_hidden_state[:, 0, :]  
            keyword_embedding = outputs.last_hidden_state[:, 1, :]  

        cosine_similarity_scores = cosine_similarity(news_embeddings, keyword_embedding)
        
        return cosine_similarity_scores.flatten()
    except ValueError:
        print("ValueError: The documents only contain stop words or have no content.")
        return None

from concurrent.futures import ThreadPoolExecutor

def compute_similarity(df_ptt, yahoo_news_summary):
    ptt_title_list = [] 

    print("\n進入PTT篩選的摘要如下："+ yahoo_news_summary['title'])
        
    # 計算摘要與每個PTT標題之間的相似度
    title_similarities = {}
    with ThreadPoolExecutor() as executor:
        similarity_scores = executor.map(
            lambda title: calculate_bert_similarity(yahoo_news_summary['title'], title),
            df_ptt['title']
        )
    title_similarities = dict(zip(df_ptt['title'], similarity_scores))

    
    # 找出相似度前三高的標題
    sorted_titles = sorted(title_similarities, key=title_similarities.get, reverse=True)
    most_similar_titles = sorted_titles[:3]
    
    print("相似度前三高的標題：")
    for idx, title in enumerate(most_similar_titles, start=1):
        similarity_score = title_similarities[title]
        url = df_ptt[df_ptt['title'] == title]['link'].values[0]  # Assuming 'url' is the column name
        print(f"{idx}. 標題：{title}，網址：{url}，相似度分數：{similarity_score}")
        ptt_title_list.append({'title': title, 'url': url})
    
    return ptt_title_list



def choose_ptt_data(news_type,hashtag_keyword,news_list):
    if news_type =='最新':
        for yahoo_news_summary in news_list:
            df_ptt = open_ptt_url_fillter_subtopic(yahoo_news_summary['subtopic'],yahoo_news_summary['timestamp'])
            df_ptt = time_sort(df_ptt)
            select_ptt = compute_similarity(df_ptt,yahoo_news_summary)
            #print(select_ptt)
            for ptt in select_ptt:
                # 將選擇的PTT資訊加入yahoo_news_summary
                yahoo_news_summary[ptt['title']] = ptt['url']
    else:
        for yahoo_news_summary in news_list:
            df_ptt=search_ptt_by_kw(hashtag_keyword,yahoo_news_summary['timestamp'])
            df_ptt = time_sort(df_ptt)
            select_ptt = compute_similarity(df_ptt,yahoo_news_summary)
            #print(select_ptt)
            i=1
            for ptt in select_ptt:
                # 將選擇的 PTT 資訊加入 yahoo_news_summary
                yahoo_news_summary[f'ptt_title_{i}'] = ptt['title']
                yahoo_news_summary[f'ptt_url_{i}'] = ptt['url']
                i += 1
    
    return news_list

#client = MongoClient("mongodb+srv://user2:user2@cluster0.zgtguxv.mongodb.net/?retryWrites=true&w=majority")
#db = client['Kmeans新聞']
#collection=db['當日熱門']
#cursor =collection.find({'topic':"運動",'date':"2023-08-11"})
#document = cursor.next()
#choose_ptt_data(document ['news_list'],'運動','nba')

# 熱門的部分
# 在選取新聞後，將新聞字典（關鍵字:新聞串列）傳入進行PTT比對
# 進入PTT比對的流程
# 先取出新聞串列
# 對於每篇新聞，取得其摘要，然後呼叫一個函數來尋找3個相關的PTT討論串
# 將這3個PTT討論串的標題與連結存入新聞串列中
# 最後的輸出將會是一個新聞字典，其中包含{關鍵字:新聞串列}的對應關係
# 在每個新聞串列內部，除了原本的id、主題、標題等資訊外，
# 也會有3個PTT討論串的詳細資料，每個PTT討論串都是一個字典

# 最新的部分
# 在選取新聞後，將新聞串列傳入進行PTT比對
# 進入PTT比對的流程
# 對於每篇新聞，取得其摘要，然後呼叫一個函數來尋找3個相關的PTT討論串
# 將這3個PTT討論串的標題與連結存入新聞串列中
# 最後的輸出將會是一個新聞串列
# 在每個新聞串列內部，除了原本的id、主題、標題等資訊外，
# 也會有3個PTT討論串的詳細資訊，每個PTT討論串都是一個字典

