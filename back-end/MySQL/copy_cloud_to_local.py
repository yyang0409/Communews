import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

def copy():
    # 雲端資料庫連接設定
    cloud_db_config = {
        'user': 'mysqluser',
        'password': 'mysqluser',
        'host': 'communews.ctqdwhl8sobn.us-east-1.rds.amazonaws.com',
        'database': 'communews'
    }

    # 本地資料庫連接設定
    local_db_config = {
        'user': 'root',
        'password': '109403502',
        'host': '127.0.0.1',
        'database': 'communews'
    }

    # 連接到雲端資料庫
    cloud_db_conn = mysql.connector.connect(**cloud_db_config)

    # 使用 SQLAlchemy 建立本地資料庫連接
    local_db_engine = create_engine(f"mysql+mysqlconnector://{local_db_config['user']}:{local_db_config['password']}@{local_db_config['host']}/{local_db_config['database']}")

    # 列出你要複製的表格名稱
    tables_to_copy = ['tb_collection_record', 'tb_keyword', 'tb_news_score','tb_news_view','tb_ptt_search_link','tb_subtopic','tb_user','tb_user_keyword_weight','tb_ptt_data']

    for table_name in tables_to_copy:
        # 设定分页参数
        page_size = 1000  # 每页数据量
        page = 1

        while True:
            # 计算偏移量
            offset = (page - 1) * page_size
            
            # 构建查询语句
            query = f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}"
            
            # 读取数据
            data = pd.read_sql(query, con=cloud_db_conn)

            # 如果获取的数据为空，说明已经读取完毕
            if data.empty:
                break

            # 寫入數據到本地資料庫
            data.to_sql(name=table_name, con=local_db_engine, if_exists='replace', index=False)
            
            # 增加页数，继续下一页的数据
            page += 1

    # 關閉雲端資料庫連接
    cloud_db_conn.close()

#copy()