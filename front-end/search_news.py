from kmeans import *
from pymongo import MongoClient
from collections import Counter
from datetime import datetime, timedelta,time
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from ckiptagger import WS
from keybert import KeyBERT

# 在程式中使用TF-IDF需要初始化NLTK
nltk.download('punkt')

client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/TodayNews?retryWrites=true&w=majority")
#db_today = client["TodayNews"]
db_daily = client['關鍵每一天']
db=client['News']
client_2 = MongoClient("mongodb+srv://userdb2:userdb2@cluster0.whf1ljw.mongodb.net/?retryWrites=true&w=majority")
#db_today = client["TodayNews"]
db_daily_2 = client_2['關鍵每一天']
db_2=client_2['News']
total_subject = ['健康', '國際', '娛樂', '生活', '社會地方', '科技', '財經', '運動']


def convert_to_dataframe(keyword_news_data):
    data = []
    for news in keyword_news_data:
        data.append(news['document'])
    return pd.DataFrame(data)

def calculate_tfidf(news_text, keywords):
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(news_text)
        query_vector = vectorizer.transform([keywords])  # 把關鍵字轉換成TF-IDF向量
    except ValueError:
        print("ValueError: The documents only contain stop words or have no content.")
        return None

    # 計算相似性
    similarity_scores = cosine_similarity(tfidf_matrix, query_vector)
    return similarity_scores.flatten()

kw_list=[]
ws = WS("./data")

def ws_zh(text):
    words = ws([text])
    return words[0]

def get_input_keyword(usr_input): 
    usr_input = usr_input.strip()  # 剔除输入字符串的空白字符
    if len(usr_input)>3:
        usr_input = ws_zh(usr_input)
        return usr_input
    else:
         return [usr_input]
#使用者搜尋 比對 
#會再改
def gen_kw_search_news(usr_input):
    all_selected_news = {}  # 以關鍵字為鍵的存儲最相似的新聞字典
    four_selected_news={}

    all_keywords = get_input_keyword(usr_input)


    for keyword in all_keywords:
        # 進行聚合查詢，使用一個關鍵字來查詢新聞
        pipeline = [
            {
                '$match': {
                    'title': {'$regex': f'.*{keyword}.*', '$options': 'i'}
                }
            },
            {"$sort": {"timestamp": -1}},
            {"$limit": 200},
            {
                '$project': {
                    'document': '$$ROOT',  # 將整個文檔添加到document欄位中
                    'combined_text': {'$concat': ['$title', ' ', '$summary']},  # 新增combined_text字段
                    'timestamp': '$timestamp'  # 保存時間戳
                }
            },
            {
                '$match': {
                    'combined_text': {'$exists': True}
                }
            }
        ]

        # 建立一個空的列表來保存查詢結果
        keyword_news_data = []

        for collection_name in total_subject:
                news_data = list(db[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data)  # 把查詢結果加入列表
                news_data_2 = list(db_2[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data_2)  # 把查詢結果加入列表

        if len(keyword_news_data) < 20:
            print("不夠")
            pipeline = [
            {
                '$match': {
                    '$or': [
                        {'title': {'$regex': f'.*{keyword}.*', '$options': 'i'}},
                        {'summary': {'$regex': f'.*{keyword}.*', '$options': 'i'}}
                    ]
                }   
            },
            {"$sort": {"timestamp": -1}},
            {"$limit": 200},
            {
                '$project': {
                    'document': '$$ROOT',  # 將整個文檔添加到document欄位中
                    'combined_text': {'$concat': ['$title', ' ', '$summary']},  # 新增combined_text字段
                    'timestamp': '$timestamp'  # 保存時間戳
                }
            },
            {
                '$match': {
                    'combined_text': {'$exists': True}
                }
            }
        ]        
        # 建立一個空的列表來保存查詢結果
        keyword_news_data = []

        for collection_name in total_subject:
                news_data = list(db[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data)  # 把查詢結果加入列表
                news_data_2 = list(db_2[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data_2)  # 把查詢結果加入列表
                
        # 提取新聞標題和摘要文本
        news_text = [news['combined_text'] for news in keyword_news_data]

        # 計算TF-IDF相似性分數
        similarity_scores = calculate_tfidf(news_text, keyword)

        
        # 把相似性分數加回每個新聞的資料中
        for i, news in enumerate(keyword_news_data):
            news['document']['similarity'] = similarity_scores[i]

        df_keyword_news_data = convert_to_dataframe(keyword_news_data)
        
        result = hot_run_kmeans_from_df(df_keyword_news_data,int(len(df_keyword_news_data)/2))

        # 按照相似度和時間戳排序
        
        result.sort(key=lambda x: (x['similarity'], x['timestamp']), reverse=True)

          
        if keyword_news_data:
            four_selected_news[keyword] = [news for news in result[:4]]
            all_selected_news[keyword] = [news for news in result]
            
    
    return four_selected_news,all_selected_news


def recommend_news(top_ten_keywords):
    all_selected_news = {}  # 以關鍵字為鍵的存儲最相似的新聞字典
    four_selected_news={}

    for keyword in top_ten_keywords:
        # 進行聚合查詢，使用一個關鍵字來查詢新聞
        pipeline = [
            {
                '$match': {
                    'title': {'$regex': f'.*{keyword}.*', '$options': 'i'}
                }
            },
            {"$sort": {"timestamp": -1}},
            {"$limit": 200},
            {
                '$project': {
                    'document': '$$ROOT',  # 將整個文檔添加到document欄位中
                    'combined_text': {'$concat': ['$title', ' ', '$summary']},  # 新增combined_text字段
                    'timestamp': '$timestamp'  # 保存時間戳
                }
            },
            {
                '$match': {
                    'combined_text': {'$exists': True}
                }
            }
        ]

        # 建立一個空的列表來保存查詢結果
        keyword_news_data = []

        for collection_name in total_subject:
                news_data = list(db[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data)  # 把查詢結果加入列表
                news_data_2 = list(db_2[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data_2)  # 把查詢結果加入列表

        if len(keyword_news_data) < 20:
            print("不夠")
            pipeline = [
            {
                '$match': {
                    '$or': [
                        {'title': {'$regex': f'.*{keyword}.*', '$options': 'i'}},
                        {'summary': {'$regex': f'.*{keyword}.*', '$options': 'i'}}
                    ]
                }   
            },
            {"$sort": {"timestamp": -1}},
            {"$limit": 200},
            {
                '$project': {
                    'document': '$$ROOT',  # 將整個文檔添加到document欄位中
                    'combined_text': {'$concat': ['$title', ' ', '$summary']},  # 新增combined_text字段
                    'timestamp': '$timestamp'  # 保存時間戳
                }
            },
            {
                '$match': {
                    'combined_text': {'$exists': True}
                }
            }
        ]        
        # 建立一個空的列表來保存查詢結果
        keyword_news_data = []

        for collection_name in total_subject:
                news_data = list(db[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data)  # 把查詢結果加入列表
                news_data_2 = list(db_2[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data_2)  # 把查詢結果加入列表
                
        # 提取新聞標題和摘要文本
        news_text = [news['combined_text'] for news in keyword_news_data]

        # 計算TF-IDF相似性分數
        similarity_scores = calculate_tfidf(news_text, keyword)

        
        # 把相似性分數加回每個新聞的資料中
        for i, news in enumerate(keyword_news_data):
            news['document']['similarity'] = similarity_scores[i]

        df_keyword_news_data = convert_to_dataframe(keyword_news_data)
        
        result = hot_run_kmeans_from_df(df_keyword_news_data,int(len(df_keyword_news_data)/2))

        # 按照相似度和時間戳排序
        
        result.sort(key=lambda x: (x['similarity'], x['timestamp']), reverse=True)

          
        if keyword_news_data:
            four_selected_news[keyword] = [news for news in result[:4]]
            all_selected_news[keyword] = [news for news in result]
            
    
    return four_selected_news,all_selected_news


#print(kw_search_news("執行長"))

