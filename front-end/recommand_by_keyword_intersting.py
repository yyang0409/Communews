import json
import numpy as np
import pandas as pd
import pymysql
from datetime import datetime, timedelta
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# 建立資料庫連接
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='109403502',
    database='communews',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def create_matrix(df):
    N = len(df['id_user'].unique())
    M = len(df['id_keyword'].unique())

    user_mapper = dict(zip(np.unique(df["id_user"]), list(range(N))))
    keyword_mapper = dict(zip(np.unique(df["id_keyword"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["id_user"])))
    keyword_inv_mapper = dict(zip(list(range(M)), np.unique(df["id_keyword"])))

    user_index = [user_mapper[i] for i in df['id_user']]
    keyword_index = [keyword_mapper[i] for i in df['id_keyword']]

    X = csr_matrix((df["rating"], (keyword_index, user_index)), shape=(M, N))

    return X, user_mapper, keyword_mapper, user_inv_mapper, keyword_inv_mapper

def data_processing():
    query_ratings = "SELECT * FROM tb_collection_record"
    ratings = pd.read_sql(query_ratings, conn)

    query_keyword = "SELECT * FROM tb_keyword"
    keyword = pd.read_sql(query_keyword, conn)

    n_ratings = len(ratings)
    n_keyword = len(ratings['id_keyword'].unique())
    n_users = len(ratings['id_user'].unique())

    user_freq = ratings[['id_user', 'id_keyword']].groupby('id_user').count().reset_index()
    user_freq.columns = ['id_user', 'n_ratings']

    mean_rating = ratings.groupby('id_keyword')[['rating']].mean()
    lowest_rated = mean_rating['rating'].idxmin()
    keyword.loc[keyword['id_keyword'] == lowest_rated]
    highest_rated = mean_rating['rating'].idxmax()
    keyword.loc[keyword['id_keyword'] == highest_rated]
    ratings[ratings['id_keyword'] == highest_rated]
    ratings[ratings['id_keyword'] == lowest_rated]

    keyword_stats = ratings.groupby('id_keyword')[['rating']].agg(['count', 'mean'])
    keyword_stats.columns = keyword_stats.columns.droplevel()

    X, user_mapper, keyword_mapper, user_inv_mapper, keyword_inv_mapper = create_matrix(ratings)

    return X, user_mapper, keyword_mapper, user_inv_mapper, keyword_inv_mapper, keyword, ratings

def find_similar_keywords(keyword_id, X, k, keyword_mapper, keyword_inv_mapper, metric='cosine', show_distance=False):
    neighbour_ids = []
    keyword_ind = keyword_mapper[keyword_id]
    keyword_vec = X[keyword_ind]
    k += 1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    keyword_vec = keyword_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(keyword_vec, return_distance=show_distance)
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(keyword_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids

def generate_today_date():
    now = datetime.now()
    date_string = now.strftime("%Y%m%d")
    return date_string

def generate_previos_date(version):
    if version == "one_week_ago":
        now = datetime.now()
        one_week_ago = now - timedelta(days=7)
        date_string = one_week_ago.strftime("%Y%m%d")

    if version == "one_month_ago":
        now = datetime.now()
        one_month_ago = now - timedelta(days=30)
        date_string = one_month_ago.strftime("%Y%m%d")

    return date_string

def find_user_recent_favorite_keyword(user_id):
    query_ratings = "SELECT * FROM tb_collection_record"
    ratings = pd.read_sql(query_ratings, conn)
    user_rating_all = ratings[ratings['id_user'] == user_id].copy()

    today_date = generate_today_date()
    previous_date = generate_previos_date("one_week_ago")
    user_rating_near = user_rating_all[user_rating_all['date'] >= datetime.strptime(previous_date, "%Y%m%d").date()]
    if user_rating_near.empty:
        previous_date = generate_previos_date("one_month_ago")
        user_rating_near = user_rating_all[user_rating_all['date'] >= int(previous_date)]

    greatest_user_rating_near = user_rating_near[user_rating_near['rating'] >= 9]
    if greatest_user_rating_near.empty:
        greatest_user_rating_near = user_rating_near[user_rating_near['rating'] >= 6]

    if len(greatest_user_rating_near) > 0:
        random_row = greatest_user_rating_near.sample(n=1)
    else:
        random_row = user_rating_near.sample(n=1)

    keyword_id = random_row.loc[:, 'id_keyword'].values[0]


    return keyword_id

def find_recommand(keyword_id):
    X, user_mapper, keyword_mapper, user_inv_mapper, keyword_inv_mapper, keyword, ratings = data_processing()
    all_keyword_titles = dict(zip(keyword['id_keyword'], keyword['value']))
    k = 10
    similar_ids = find_similar_keywords(keyword_id, X, k, keyword_mapper, keyword_inv_mapper)
    keyword_titles = all_keyword_titles[keyword_id]

    print(f"由於您觀看了 {keyword_titles}")
    print("您會觀看以下新聞\n")

    for i in similar_ids:
        print(all_keyword_titles[i])

    return similar_ids

def main():
    keyword_id = find_user_recent_favorite_keyword(2)  # 假設使用者ID為2
    find_recommand(keyword_id)  # 填入您的資料型別

# 執行主函式
main()

# 關閉資料庫連接
conn.close()
