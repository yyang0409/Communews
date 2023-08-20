# 導入 模組(module) 
from datetime import  timedelta
import pandas as pd
import mysql.connector
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

def get_all_ptt(news_datetime):
    host = '127.0.0.1'
    user = 'root'
    password = '109403502'
    database = 'communews'
    charset =  "utf8"
    
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)
    
    cursor = connection.cursor()
    start_date = (news_datetime - timedelta(days=1)).date()
    end_date = (news_datetime + timedelta(days=2)).date()
    # SQL查询语句
    select_query = "SELECT * FROM tb_ptt_data WHERE date BETWEEN %s AND %s"
    # 执行查询
    cursor.execute(select_query,(start_date,end_date))
    # 获取所有结果
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    #print(df)
    return df

import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity

model_name = "hfl/chinese-roberta-wwm-ext"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def calculate_bert_similarity(summary, text):
    try:
        inputs = tokenizer(summary, text, return_tensors="pt", padding=True, truncation="only_first")
        with torch.no_grad():
            outputs = model(**inputs)
            summary_embedding = outputs.last_hidden_state[:, 0, :]  
            text_embedding = outputs.last_hidden_state[:, 1:, :].mean(dim=1) 

        cosine_similarity_scores = cosine_similarity(summary_embedding, text_embedding)
        
        return cosine_similarity_scores.flatten()
    except ValueError:
        print("ValueError: The documents only contain stop words or have no content.")
        return None

def filter_related_ptt(df_ptt, yahoo_news):
    # 將 PTT 的標題和內容結合成一個新的欄位
    df_ptt['combined_text'] = df_ptt['title'] + " " + df_ptt['content']

    news_text = yahoo_news['title']+" "+ yahoo_news['summary']
    
    # 計算相似度分數
    similarity_scores = calculate_bert_similarity(news_text, df_ptt['combined_text'])
    
    if similarity_scores is None:
        return []

    # 取得相似度大於0的索引
    valid_similarity_indices = [idx for idx, score in enumerate(similarity_scores) if score > 0]

    # 取得相似度最高的索引
    max_similarity_indices = sorted(valid_similarity_indices, key=lambda idx: similarity_scores[idx], reverse=True)[:3]

    # 選擇三個不重複的資料
    similar_ptt_list = []
    selected_titles = set()

    for idx in max_similarity_indices:
        title = df_ptt.iloc[idx]['title']
        if title not in selected_titles:
            selected_titles.add(title)
            url = df_ptt.iloc[idx]['link']
            similarity_score = similarity_scores[idx]
            similar_ptt_list.append({'title': title, 'url': url, 'score': similarity_score})
            if len(similar_ptt_list) == 3:
                break

    return similar_ptt_list



def choose_ptt_data(news_type,news_list):
    if news_type =='最新':
        #新聞標題和PTT摘要比較
        for yahoo_news in news_list:
            print("目前執行新聞:",yahoo_news['title'])
            df_ptt = get_all_ptt(yahoo_news['timestamp'])
            #print("要比對的PTT有:",df_ptt)
            filter_ptt_list=filter_related_ptt(df_ptt, yahoo_news)
            for filter_ptt in filter_ptt_list:
                print("配對到的3個PTT:",filter_ptt['title'],filter_ptt['score'])
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
            df_ptt = get_all_ptt(yahoo_news['timestamp'])
            filter_ptt_list=filter_related_ptt(df_ptt, yahoo_news)
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

