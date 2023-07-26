from kmeans import *
from pymongo import MongoClient
from collections import Counter
from datetime import datetime, timedelta,time
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

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
    news_list=run_kmeans_from_df(df,len(df)//5)
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

        # 按照相似度和時間戳排序
        keyword_news_data.sort(key=lambda x: (x['document']['similarity'], x['timestamp']), reverse=True)
          
        if keyword_news_data:
            keyword_news_data[:] = keyword_news_data[:4]
            # 將相似度最高的前10篇新聞添加到selected_news字典中
            selected_news[keyword] = [news['document'] for news in keyword_news_data]
    return selected_news


#print(hot_all_search_news("daily"))

def hot_topic_search_news(collection_name,option):
    all_keywords = get_subject_col_data(collection_name, option)
    selected_news = {}  # 存儲最相似的新聞

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
    
        news_data = list(db[collection_name].aggregate(pipeline))
        keyword_news_data.extend(news_data)  # 把查詢結果加入列表
        # 提取新聞標題和摘要文本
        news_text = [news['combined_text'] for news in keyword_news_data]

        # 計算TF-IDF相似性分數
        similarity_scores = calculate_tfidf(news_text, keyword)

        # 把相似性分數加回每個新聞的資料中
        for i, news in enumerate(keyword_news_data):
            news['document']['similarity'] = similarity_scores[i]

        # 按照相似度和時間戳排序
        keyword_news_data.sort(key=lambda x: (x['document']['similarity'], x['timestamp']), reverse=True)

        if keyword_news_data:
            keyword_news_data[:] = keyword_news_data[:4]
            # 將相似度最高的前10篇新聞添加到selected_news字典中
            selected_news[keyword] = [news['document'] for news in keyword_news_data]
    return selected_news

#使用者搜尋 比對 
#會再改
def kw_search_news(keyword):
    selected_news = {}  # 以關鍵字為鍵的存儲最相似的新聞字典
    for collection_name in total_subject:
        # 聚合查询，筛选出包含关键字的新闻并计算相似度
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'title': {'$regex': f'.*{keyword}.*', '$options': 'i'}},
                        {'summary': {'$regex': f'.*{keyword}.*', '$options': 'i'}}
                    ]
                }
            },
            {
                '$addFields': {
                    'combined_text': {'$concat': ['$title', ' ', '$summary']}
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'title': 1,
                    'summary': 1,
                    'url': 1,
                    'image': 1,
                    'timestamp': 1,
                    'match_count': {
                        '$size': {
                            '$setIntersection': [
                                {'$split': ['$combined_text', ' ']},
                                [keyword]
                            ]
                        }
                    },
                    'similarity': {
                        '$cond': {
                            'if': {
                                '$and': [
                                    {'$gt': [{'$size': {'$split': ['$combined_text', ' ']}} , 0]},
                                    {'$ne': ['$combined_text', None]}
                                ]
                            },
                            'then': {
                                '$divide': [
                                    {'$ifNull': ['$match_count', 0]},
                                    {'$size': {'$split': ['$combined_text', ' ']}}
                                ]
                            },
                            'else': 0
                        }
                    }
                }
            },
            {
                '$sort': {'timestamp': -1}
            }
        ]

        news_data = list(db[collection_name].aggregate(pipeline))
        # 将结果添加到 selected_news 字典中
        for news in news_data:
            if keyword not in selected_news:
                selected_news[keyword] = []
            selected_news[keyword].append(news)

    # 将全部主题的新闻按照相似度排序
    for news_list in selected_news.values():
        news_list.sort(key=lambda x: x['similarity'], reverse=True)
        news_list[:] = news_list[:4]  

    return selected_news

#print(kw_search_news("執行長"))

