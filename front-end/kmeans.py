# -*- coding: utf-8 -*-
import jieba
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
import random
import pandas as pd
import os
import json
pd.set_option('display.max_columns', None)  # 設定顯示的最大列數，設為 None 表示顯示所有列
pd.set_option('display.expand_frame_repr', False)  # 設定是否展開 DataFrame 的每一列，False 表示不展開
current_dir = os.path.dirname(os.path.abspath(__file__))

data_documentary_name = "data"
data_path = current_dir+"\\"+data_documentary_name+"\\"

stopwords_name = "stop_words.txt"
stopwords_path = data_path+stopwords_name

CLSTER_NUM = 50

class KmeansClustering():
    def __init__(self, stopwords_path=stopwords_path):
        self.stopwords = self.load_stopwords(stopwords_path)
        self.vectorizer = CountVectorizer()
        self.transformer = TfidfTransformer()

    def load_stopwords(self, stopwords=None):
        """
        加载停用词
        :param stopwords:
        :return:
        """
        if stopwords:
            with open(stopwords, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f]
        else:
            return []

    def preprocess_data(self,corpus_path):
        """
        文本预处理，每行一个文本
        :param corpus_path:
        :return:
        """
        
        corpus = []
        
        with open(corpus_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                corpus.append(' '.join([word for word in jieba.lcut(line.strip()) if word not in self.stopwords]))
        
        return corpus
        

    def get_text_tfidf_matrix(self, corpus):
        """
        获取tfidf矩阵
        :param corpus:
        :return:
        """
        tfidf = self.transformer.fit_transform(self.vectorizer.fit_transform(corpus))

        # 获取词袋中所有词语
        # words = self.vectorizer.get_feature_names()

        # 获取tfidf矩阵中权重
        weights = tfidf.toarray()
        return weights

    def kmeans(self, corpus_path, n_clusters=CLSTER_NUM):
        """
        KMeans文本聚类
        :param corpus_path: 语料路径（每行一篇）,文章id从0开始
        :param n_clusters: ：聚类类别数目
        :return: {cluster_id1:[text_id1, text_id2]}
        """
        corpus = self.preprocess_data(corpus_path)
        weights = self.get_text_tfidf_matrix(corpus)

        clf = KMeans(n_clusters=n_clusters)

        # clf.fit(weights)

        y = clf.fit_predict(weights)

        # 中心点
        # centers = clf.cluster_centers_

        # 用来评估簇的个数是否合适,距离约小说明簇分得越好,选取临界点的簇的个数
        # score = clf.inertia_
        # 每个样本所属的簇
        result = {}
        for text_idx, label_idx in enumerate(y):
            key = "cluster_{}".format(label_idx)
            if key not in result:
                result[key] = [text_idx]
            else:
                result[key].append(text_idx)
        return result

def newest_choose_final_news(result, df_news, cluster_num):
    #print("這是result")
    #print(result)
    final_news_index = []
    for i in range(cluster_num):
        cluster = "cluster_" + str(i)
        cluster_content = result[cluster]
        #print(cluster_content)
        #for i in cluster_content:
            #print(df_news.at[i,0])
            
        
        # 對該群集內的新聞進行排序，以取得時間最新的那筆新聞
        sorted_news = df_news.loc[cluster_content].sort_values('timestamp', ascending=False)
        #print(sorted_news.index[0])
        #print(df_news.at[sorted_news.index[0],0])
        # 將時間最新的新聞的索引值加入到結果列表中
        final_news_index.append(sorted_news.index[0])
    #print("最終:",final_news_index)
    return final_news_index

def hot_choose_final_news(result, df_news, cluster_num):
    if not result or cluster_num < 1 or f'cluster_{cluster_num-1}' not in result:
        print("Invalid result or cluster_num.")
        return []
    
    final_news_index = []
    
    for i in range(cluster_num):
        cluster = "cluster_" + str(i)
        try:
            cluster_content = result[cluster]

            # Get the news within the cluster
            news = df_news.loc[cluster_content]

            # Sort the news within the cluster based on the similarity score and timestamp in descending order
            news_sorted = news.sort_values(by=['similarity', 'timestamp'], ascending=[False, False])

            # Get the index of the news article with the highest similarity score from the sorted cluster
            max_similarity_news_index = news_sorted.index[0]

            # Add the index of the news article with the highest similarity to the result list
            final_news_index.append(max_similarity_news_index)
        except KeyError:
            print(f"Cluster {cluster} not found. Skipping.")
            continue

    return final_news_index

def translate_text_to_dataframe(file):
    file = data_path+file
    df = pd.read_csv(file, delimiter='\t', header=None)
    return df


def newest_run_kmeans(news_summary,cluster_num):
    
    with open(data_path+'kmeans.txt', "w",encoding='utf-8') as file:
        # 遍历列表，逐行写入文件
        for item in news_summary:
            file.write(item+"\n")
    CLSTER_NUM = cluster_num

    Kmeans = KmeansClustering(stopwords_path=stopwords_path)
    result = Kmeans.kmeans(data_path+'kmeans.txt', n_clusters=cluster_num)
    
    df_news_summary = translate_text_to_dataframe('kmeans.txt')

    output_news_list = newest_choose_final_news(result,df_news_summary,cluster_num)
    finished_kmeans_summary = []

    for news_index in (output_news_list):
        finished_kmeans_summary.append(news_summary[news_index])
    return finished_kmeans_summary

def hot_run_kmeans(news_summary,cluster_num):
    
    with open(data_path+'kmeans.txt', "w",encoding='utf-8') as file:
        # 遍历列表，逐行写入文件
        for item in news_summary:
            file.write(item+"\n")
    CLSTER_NUM = cluster_num

    Kmeans = KmeansClustering(stopwords_path=stopwords_path)
    result = Kmeans.kmeans(data_path+'kmeans.txt', n_clusters=cluster_num)
    
    df_news_summary = translate_text_to_dataframe('kmeans.txt')

    output_news_list = hot_choose_final_news(result,df_news_summary,cluster_num)
    finished_kmeans_summary = []

    for news_index in (output_news_list):
        finished_kmeans_summary.append(news_summary[news_index])
    return finished_kmeans_summary

def newest_run_kmeans_from_df(df,cluster_num):
    #print(df)
    
    # 提取'id'字段的值并存储在列表中
    news_summary_list = df['summary'].tolist()
    news_id_list = df['_id'].tolist()
    
    
    with open(data_path+'kmeans.txt', "w",encoding='utf-8') as file:
        # 遍历列表，逐行写入文件
        for item in news_summary_list:
            file.write(item+"\n")
    CLSTER_NUM = cluster_num

    Kmeans = KmeansClustering(stopwords_path=stopwords_path)
    result = Kmeans.kmeans(data_path+'kmeans.txt', n_clusters=cluster_num)
    #print(result)
    df_news_summary = translate_text_to_dataframe('kmeans.txt')
    df_news_summary['timestamp'] = df['timestamp'].apply(lambda x: x)
    #print(df_news_summary)
    output_news_list = newest_choose_final_news(result,df_news_summary,cluster_num)
    #print("傳回:",output_news_list)
    finished_kmeans_summary_list = []

    for news_index in (output_news_list):
        finished_kmeans_summary_list.append(news_summary_list[news_index])
        #print(news_summary_list[news_index])
    #print("finished_kmeans_summary_list:",finished_kmeans_summary_list)

    df_return = pd.DataFrame()
    
    for summary in finished_kmeans_summary_list:
        selected_rows = df[df["summary"] == summary]
        #print(len(selected_rows))
        if len(selected_rows)==1:
            df_return = df_return.append(selected_rows, ignore_index=True) 
        if len(selected_rows)>1:
            #print("有兩個以上一樣的")
            selected_rows = selected_rows.iloc[0]
            df_return = df_return.append(selected_rows, ignore_index=True)
    #print(df_return)
    #list_data = df_return.values.tolist()
    result_list = df_return.to_dict(orient='records')
    #print(result_list)
    return result_list

def hot_run_kmeans_from_df(df,cluster_num):
    #print(df)
    #print(df.info())

    # 提取'id'字段的值并存储在列表中
    news_summary_list = df['summary'].tolist()
    news_id_list = df['_id'].tolist()
    
    
    with open(data_path+'kmeans.txt', "w",encoding='utf-8') as file:
        # 遍历列表，逐行写入文件
        for item in news_summary_list:
            file.write(item+"\n")
    CLSTER_NUM = cluster_num

    Kmeans = KmeansClustering(stopwords_path=stopwords_path)
    result = Kmeans.kmeans(data_path+'kmeans.txt', n_clusters=cluster_num)
    #print(result)
    df_news_summary = translate_text_to_dataframe('kmeans.txt')
    df_news_summary['timestamp'] = df['timestamp'].apply(lambda x: x)
    # 添加相似度欄位
    df_news_summary['similarity'] = df['similarity']
    #print(df_news_summary)
    output_news_list = hot_choose_final_news(result,df_news_summary,cluster_num)
    #print("傳回:",output_news_list)
    finished_kmeans_summary_list = []

    for news_index in (output_news_list):
        finished_kmeans_summary_list.append(news_summary_list[news_index])
    #print("finished_kmeans_summary_list:",finished_kmeans_summary_list)

    df_return = pd.DataFrame()
    
    for summary in finished_kmeans_summary_list:
        selected_rows = df[df["summary"] == summary]
        #print(len(selected_rows))
        if len(selected_rows)==1:
            df_return = df_return.append(selected_rows, ignore_index=True) 
        if len(selected_rows)>1:
            #print("有兩個以上一樣的")
            selected_rows = selected_rows.iloc[0]
            df_return = df_return.append(selected_rows, ignore_index=True)
    #print(df_return)
    #list_data = df_return.values.tolist()
    result_list = df_return.to_dict(orient='records')
    #print(result_list)
    return result_list
