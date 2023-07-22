from pymongo import MongoClient
from collections import Counter
from datetime import datetime, timedelta

client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/TodayNews?retryWrites=true&w=majority")
db_today = client["TodayNews"]
db_daily = client['關鍵每一天']
db=client['News']
total_subject = ['健康', '國際', '娛樂', '生活', '社會地方', '科技', '財經', '運動']
#用來抓最新新聞的
def get_DB_News_data(topic,num):

    collection = db[topic]

    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$limit": num}
    ]

    data = collection.aggregate(pipeline)
    return list(data)
#計算每周 每月 關鍵字數量
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
        end_datetime = current_datetime - timedelta(days=1)
        start_datetime = end_datetime - timedelta(days=1)
    elif option == 'weekly':
        end_datetime = current_datetime - timedelta(days=1)
        start_datetime = end_datetime - timedelta(days=7)
    elif option == 'monthly':
        end_datetime = current_datetime - timedelta(days=1)
        start_datetime = end_datetime - timedelta(days=30)
    else:
      return
    collection = db_daily[collection_name]
    end_datetime=end_datetime.strftime("%Y-%m-%d")
    start_datetime=start_datetime.strftime("%Y-%m-%d")
    documents = collection.find({"date": {"$gte": start_datetime, "$lt": end_datetime}})
    
    keywords_list = []
    for document in documents:
        keywords = document.get('keywords')
        if keywords:
            keywords_list.extend(keywords)

    hot_keywords_list=calculate_keywords(keywords_list)

    return hot_keywords_list
#熱門頁面比對
def hot_all_search_news(option):
    all_keywords = get_subject_col_data("綜合全部", option)
    selected_news = {}  # 以关键字为键的字典，用于存储最相似的新闻，每个关键字对应一个列表，记录与该关键字相关的新闻
    selected_news_ids = set()
    for collection_name in total_subject:
        # 聚合查询，筛选出包含关键字的新闻并计算相似度，同时考虑时间戳
        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'title': {'$regex': f'.*{kw}.*', '$options': 'i'}} for kw in all_keywords
                    ]
                }
            },
            {
                '$addFields': {
                    'combined_text': {'$concat': ['$title', ' ', '$summary']},
                    'timestamp': {'$toDate': '$timestamp'}  # 将timestamp字段转换为日期类型
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
                                all_keywords
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
                '$sort': {'similarity': -1, 'timestamp': -1}  # 根据相似度降序排序，如果相似度相同则根据时间戳降序排序
            }
        ]

        # 根据选项获取对应时间段的新闻数据
        if option == 'daily':
            news_data = list(db_today[collection_name].aggregate(pipeline))
        elif option == 'weekly':
            news_data = list(db[collection_name].aggregate(pipeline))
        elif option == 'monthly':
            news_data = list(db[collection_name].aggregate(pipeline))
        else:
            return {}

        # 将结果添加到 selected_news 字典中，根据关键字对新闻进行分组
        for news in news_data:
            if news['_id'] not in selected_news_ids:
                selected_news_ids.add(news['_id'])
                matching_keywords = find_matching_keywords(news, all_keywords)
                if matching_keywords:
                    for keyword in matching_keywords:
                        if keyword not in selected_news:
                            selected_news[keyword] = []
                        selected_news[keyword].append(news)

    # 将全部主题的新闻按照相似度排序
    for news_list in selected_news.values():
        news_list.sort(key=lambda x: (x['similarity'], x['timestamp']), reverse=True)
        news_list[:] = news_list[:4] 
    return selected_news




def find_matching_keywords(news, all_keywords):
    # 在新闻标题和摘要中查找匹配的关键字
    matching_keywords = []
    for keyword in all_keywords:
        if keyword.lower() in news['title'].lower() or keyword.lower() in news['summary'].lower():
            matching_keywords.append(keyword)
    return matching_keywords

#print(hot_all_search_news("daily"))



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

