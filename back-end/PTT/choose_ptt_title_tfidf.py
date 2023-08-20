# 導入 模組(module) 
from datetime import  timedelta
import pandas as pd
import mysql.connector
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
host = 'communews.ctqdwhl8sobn.us-east-1.rds.amazonaws.com'
user = 'mysqluser'
password = 'mysqluser'
#host = '127.0.0.1'
#user = 'root'
#password = '109403502'
database = 'communews'
charset =  "utf8"
    
connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)

def get_all_ptt_by_topic(topic,news_datetime):
 
    cursor = connection.cursor()
    start_date = (news_datetime - timedelta(days=1)).date()
    end_date = (news_datetime + timedelta(days=2)).date()
    # SQL查询语句
    select_query = "SELECT * FROM tb_ptt_data AS a INNER JOIN tb_subtopic AS b ON a.subtopic = b.subtopic_value WHERE b.topic = %s AND date BETWEEN %s AND %s"
    # 执行查询
    cursor.execute(select_query,(topic,start_date,end_date))
    # 获取所有结果
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    #print(df)
    return df

def get_all_ptt(news_datetime):

    
    cursor = connection.cursor()
    start_date = (news_datetime - timedelta(days=1)).date()
    end_date = (news_datetime + timedelta(days=3)).date()
    # SQL查询语句
    select_query = "SELECT * FROM tb_ptt_data WHERE date BETWEEN %s AND %s"
    # 执行查询
    cursor.execute(select_query,(start_date,end_date))
    # 获取所有结果
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    #print(df)
    return df

from sklearn.metrics.pairwise import cosine_similarity

def filter_related_ptt(df_ptt, yahoo_news):
    # 將 PTT 的標題和內容結合成一個新的欄位
    df_ptt['combined_text'] = df_ptt['title'] + " " + df_ptt['content']

    # 計算 TF-IDF 向量
    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(df_ptt['combined_text'])

    # 計算相似度
    news_text = yahoo_news['title']+ " "  + yahoo_news['new_keyword']
    news_tfidf = tfidf_vectorizer.transform([news_text])
    cosine_similarities = cosine_similarity(news_tfidf, tfidf_matrix).flatten()

    # 取得相似度大於0的索引
    valid_similarity_indices = [idx for idx, score in enumerate(cosine_similarities) if score > 0]

    # 取得相似度最高的索引
    max_similarity_indices = sorted(valid_similarity_indices, key=lambda idx: cosine_similarities[idx], reverse=True)[:3]

    # 選擇三個不重複的資料
    similar_ptt_list = []
    selected_titles = set()

    for idx in max_similarity_indices:
        title = df_ptt.iloc[idx]['title']
        if title not in selected_titles:
            selected_titles.add(title)
            url = df_ptt.iloc[idx]['link']
            similarity_score = cosine_similarities[idx]
            similar_ptt_list.append({'title': title, 'url': url, 'score': similarity_score})
            if len(similar_ptt_list) == 3:
                break

    return similar_ptt_list


def choose_ptt_data(news_type,news_list):
    filter_ptt_list=[]
    if news_type =='最新':
        #新聞標題和PTT摘要比較
        for yahoo_news in news_list:
            try:
                print("目前執行新聞:",yahoo_news['title'])
                #df_ptt = get_all_ptt(yahoo_news['timestamp'])
                df_ptt = get_all_ptt_by_topic(yahoo_news['topic'],yahoo_news['timestamp'])
                #print("要比對的PTT有:",df_ptt)
                filter_ptt_list=filter_related_ptt(df_ptt, yahoo_news)
                for filter_ptt in filter_ptt_list:
                    print("配對到的3個PTT:",filter_ptt['title'],filter_ptt['score'])
            except :
                pass
            i=1
            for ptt in filter_ptt_list:
                # 將選擇的 PTT 資訊加入 yahoo_news
                yahoo_news[f'ptt_title_{i}'] = ptt['title']
                yahoo_news[f'ptt_url_{i}'] = ptt['url']
                i += 1
            print("\n")
    else:
        #新聞標題和PTT摘要比較
        for yahoo_news in news_list:
            print("目前執行新聞:",yahoo_news['title'])
            df_ptt = get_all_ptt_by_topic(yahoo_news['topic'],yahoo_news['timestamp'])
            filter_ptt_list=filter_related_ptt(df_ptt, yahoo_news)
            for filter_ptt in filter_ptt_list:
                print("配對到的3個PTT:",filter_ptt['title'],filter_ptt['score'])
            i=1
            for ptt in filter_ptt_list:
                # 將選擇的 PTT 資訊加入 yahoo_news
                yahoo_news[f'ptt_title_{i}'] = ptt['title']
                yahoo_news[f'ptt_url_{i}'] = ptt['url']
                i += 1

    return news_list



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

