# 導入 模組(module) 
from datetime import  timedelta
import pandas as pd
import mysql.connector
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np


def get_all_ptt_by_topic(topic,news_datetime,connection):
 
    cursor = connection.cursor()
    start_date = (news_datetime - timedelta(days=1)).date()
    end_date = (news_datetime + timedelta(days=1)).date()
    # SQL查询语句
    select_query = "SELECT * FROM tb_ptt_data AS a INNER JOIN tb_subtopic AS b ON a.subtopic = b.subtopic_value WHERE b.topic = %s AND date BETWEEN %s AND %s"
    # 执行查询
    cursor.execute(select_query,(topic,start_date,end_date))
    # 获取所有结果
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    #print(df)
    return df

def filter_related_ptt_by_keywords(df_ptt, news_keywords):
    similar_ptt_list = []
    df_ptt['combined_text'] = df_ptt['title'] #+ " " + df_ptt['content']
    selected_titles = set()  # 用於儲存已選擇的標題
    
    for idx, row in df_ptt.iterrows():
        title = row['title']
        content = row['combined_text']
        match_score = sum(keyword in content for keyword in news_keywords)
        
        if match_score > 1 and title not in selected_titles:
            similar_ptt_list.append({
                'title': title,
                'url': row['link'],
                'score': match_score
            })
            selected_titles.add(title)  # 將已選擇的標題加入集合
    
    similar_ptt_list = sorted(similar_ptt_list, key=lambda x: x['score'], reverse=True)[:3]
    
    for ptt in similar_ptt_list:
        print("配對到的PTT:", ptt['title'], "分數:", ptt['score'])

    return similar_ptt_list


def choose_ptt_data(news_type,news_list):
    #host = 'communews.ctqdwhl8sobn.us-east-1.rds.amazonaws.com'
    #user = 'mysqluser'
    #password = 'mysqluser'
    host = '127.0.0.1'
    user = 'root'
    password = '109403502'
    database = 'communews'
    charset =  "utf8mb4"
        
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)
    for yahoo_news in news_list:
        print("目前執行新聞:",yahoo_news['title'])
        news_keywords = yahoo_news['new_keyword'].split(' ')
        # 只取標題關鍵字
        top_three_keywords = news_keywords[:3]
        df_ptt = get_all_ptt_by_topic(yahoo_news['topic'], yahoo_news['timestamp'],connection)
        filter_ptt_list = filter_related_ptt_by_keywords(df_ptt, top_three_keywords)
        
        i = 1
        for ptt in filter_ptt_list:
            # 將選擇的 PTT 資訊加入 yahoo_news
            yahoo_news[f'ptt_title_{i}'] = ptt['title']
            yahoo_news[f'ptt_url_{i}'] = ptt['url']
            i += 1
        print("\n")
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

