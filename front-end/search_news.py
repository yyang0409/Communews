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
total_subject = ['健康', '國際', '娛樂', '生活', '社會地方', '科技', '財經', '運動']
#用來抓最新新聞的
def get_DB_News_data(topic,num):

    current_datetime = datetime.now()
    end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    start_datetime = end_datetime - timedelta(days=1)

    collection = db[topic]
    pipeline = [
        {'$match': {'timestamp': {"$gte": start_datetime, "$lt": end_datetime}}},
        {"$sort": {"timestamp": -1}},
        {"$limit": num}
    ]

    data = collection.aggregate(pipeline)
    #print("這個是data:",list(data))
    return list(data)
#get_DB_News_data("運動",20)
#print(get_DB_News_data("運動",2))
#計算每周 每月 關鍵字數量
def newest_news_serch(combined_data):
    df = pd.DataFrame(combined_data)
    print(len(df))
    news_list= newest_run_kmeans_from_df(df,int(len(df)/5))
    return news_list
def calculate_keywords(keywords_list):

    keyword_counts = Counter()
    all_keywords = []
    for kw in keywords_list:
        keywords = kw.split(" ")
        keyword_counts.update(keywords)

    top_keywords = keyword_counts.most_common(10)
    for keyword, count in top_keywords:
        all_keywords.append(keyword)
    return all_keywords

#取得某主題的關鍵每一天
def get_subject_col_data(collection_name,option):

    current_datetime = datetime.now()
    
    if option == 'daily':
        end_datetime = current_datetime - timedelta(days=0)
        start_datetime = end_datetime - timedelta(days=1)
    elif option == 'weekly':
        end_datetime = current_datetime - timedelta(days=0)
        start_datetime = end_datetime - timedelta(days=7)
    elif option == 'monthly':
        end_datetime = current_datetime - timedelta(days=0)
        start_datetime = end_datetime - timedelta(days=30)
    else:
      return
    collection = db_daily[collection_name]
    end_datetime=end_datetime.strftime("%Y-%m-%d")
    start_datetime=start_datetime.strftime("%Y-%m-%d")
    print("關鍵字找:大於等於",start_datetime,"小於",end_datetime)
    documents = collection.find({"date": {"$gte": start_datetime, "$lt": end_datetime}})
    
    keywords_list = []
    for document in documents:
        keywords = document.get('keywords')
        if keywords:
            keywords_list.extend(keywords)

    hot_keywords_list=calculate_keywords(keywords_list)

    return hot_keywords_list

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
#熱門頁面比對
def hot_all_search_news(option):
    all_keywords = get_subject_col_data("綜合全部", option)
    selected_news = {}  # 存儲最相似的新聞
    all_selected_news={}
    current_datetime = datetime.now()

    if option == 'daily':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=1)
    elif option == 'weekly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=7)
    elif option == 'monthly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=30)
    print("新聞找:大於等於",start_datetime,"小於",end_datetime)
    for keyword in all_keywords:
        
        # 進行聚合查詢，使用一個關鍵字來查詢新聞
        pipeline = [
            {
                '$match': {
                    'title': {'$regex': f'.*{keyword}.*', '$options': 'i'},
                    'timestamp': {"$gte": start_datetime, "$lt": end_datetime}
                }
            },
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
                
        # 提取新聞標題和摘要文本
        news_text = [news['combined_text'] for news in keyword_news_data]

        # 計算TF-IDF相似性分數
        similarity_scores = calculate_tfidf(news_text, keyword)

        
        # 把相似性分數加回每個新聞的資料中
        for i, news in enumerate(keyword_news_data):
            news['document']['similarity'] = similarity_scores[i]

        df_keyword_news_data = convert_to_dataframe(keyword_news_data)
        
        result = hot_run_kmeans_from_df(df_keyword_news_data,len(df_keyword_news_data)//2)

        # 按照相似度和時間戳排序
        
        result.sort(key=lambda x: (x['similarity'], x['timestamp']), reverse=True)

          
        if keyword_news_data:
            selected_news[keyword] = [news for news in result[:4]]
            all_selected_news[keyword] = [news for news in result]
    return selected_news,all_selected_news


#print(hot_all_search_news("daily"))

def hot_topic_search_news(collection_name,option):
    all_keywords = get_subject_col_data(collection_name, option)
    selected_news = {}  # 存儲最相似的新聞
    all_selected_news={}
    current_datetime = datetime.now()

    if option == 'daily':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=1)
    elif option == 'weekly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=7)
    elif option == 'monthly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=30)
    print("新聞找:大於等於",start_datetime,"小於",end_datetime)
    for keyword in all_keywords:
        
        # 進行聚合查詢，使用一個關鍵字來查詢新聞
        pipeline = [
            {
                '$match': {
                    'title': {'$regex': f'.*{keyword}.*', '$options': 'i'},
                    'timestamp': {"$gte": start_datetime, "$lt": end_datetime}
                }
            },
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
        # 建立一個空的列表來保存查詢結果
        keyword_news_data = []

       
        news_data = list(db[collection_name].aggregate(pipeline))
        keyword_news_data.extend(news_data)  # 把查詢結果加入列表
                
        # 提取新聞標題和摘要文本
        news_text = [news['combined_text'] for news in keyword_news_data]

        # 計算TF-IDF相似性分數
        similarity_scores = calculate_tfidf(news_text, keyword)

        
        # 把相似性分數加回每個新聞的資料中
        for i, news in enumerate(keyword_news_data):
            news['document']['similarity'] = similarity_scores[i]

        df_keyword_news_data = convert_to_dataframe(keyword_news_data)
        #print(len(df_keyword_news_data))
        result = hot_run_kmeans_from_df(df_keyword_news_data,int(len(df_keyword_news_data)//2))

        # 按照相似度和時間戳排序
        
        #明天要改這個
        result.sort(key=lambda x: (x['similarity'], x['timestamp']), reverse=True)
        if keyword_news_data:
            selected_news[keyword] = [news for news in result[:4]]
            all_selected_news[keyword] = [news for news in result]
    return selected_news,all_selected_news


kw_list=[]
ws = WS("./data")

def ws_zh(text):
    words = ws([text])
    return words[0]

def get_input_keyword(usr_input): 
    vectorizer =CountVectorizer()

    usr_input=' '.join(ws_zh(usr_input))

    kw_model = KeyBERT(model='distiluse-base-multilingual-cased-v1')

    keywords= kw_model.extract_keywords(usr_input,vectorizer=vectorizer, top_n=3)
    keywords = [keyword[0] for keyword in keywords]
    for keyword in keywords:
        print(keyword)
    
    return keywords
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

