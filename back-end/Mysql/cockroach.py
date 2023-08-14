from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, text
from sqlalchemy.orm import sessionmaker
def create():
    # 設定連接URL
    db_url = "cockroachdb://user1:lruGZJphIQEbkKdpcU9GLA@communews-5777.8nk.cockroachlabs.cloud:26257/communews?sslmode=verify-full"
    # 建立資料庫引擎
    engine = create_engine(db_url)
    metadata = MetaData()
    tb_user = Table(
        "tb_user",
        metadata,
        Column("id_user", Integer, primary_key=True),
        Column("email", String(100), unique=True),
        Column("password_hash", String(100))
    )

    # 创建表
    metadata.create_all(engine)
    
def select():
    # 設定連接URL
    db_url = "cockroachdb://user1:lruGZJphIQEbkKdpcU9GLA@communews-5777.8nk.cockroachlabs.cloud:26257/communews?sslmode=verify-full"
    # 建立資料庫引擎
    engine = create_engine(db_url)
    # 建立資料庫連線
    Session = sessionmaker(bind=engine)
    session = Session()
    # 執行查詢
    query = text("SELECT * FROM tb_user")
    result = session.execute(query)
    # 取得查詢結果
    for row in result:
        print(row)
    # 關閉連線
    session.close()

def insert():
    # 設定連接URL
    db_url = "cockroachdb://user1:lruGZJphIQEbkKdpcU9GLA@communews-5777.8nk.cockroachlabs.cloud:26257/communews?sslmode=verify-full"

    # 建立資料庫引擎
    engine = create_engine(db_url)

    # 建立資料庫連線
    Session = sessionmaker(bind=engine)
    session = Session()

    # 插入資料
    insert_query = text(
        "INSERT INTO tb_user (id_user, email, password) "
        "VALUES (:id_user, :email, :password)"
    )

    data_to_insert = [
    {"id_user": 1, "email": "109403541@gmail.com", "password": "pbkdf2:sha256:600000$qTeVnOWhgHjy8hRb$4d90ede8158f862a41f90f58903f4a5db81e879e04cd0981ce6fdcc5868ec3ab"},
    {"id_user": 2, "email": "109403502@gmail.com", "password": "pbkdf2:sha256:600000$q274hsvql7nLi2hQ$ec4f78ea22dfbff48192c7be605913a3aa24b59982b68044ae0071276441925f"},
    {"id_user": 3, "email": "109403503@gmail.com", "password": "pbkdf2:sha256:600000$jRAHxBNiLsakuQrL$965df9563c32d9a3c1f7de47d8a4f295163d08b4fde3ec7c89046072a71fbdf3"},
    {"id_user": 4, "email": "109403025@gmail.com", "password": "pbkdf2:sha256:600000$s8MQ5FzZESVgDeqj$bde6b58e315d390e15f8792a4d11655c9109e97dea6909087c5e342d539d255d"},
    {"id_user": 5, "email": "109403516@gmail.com", "password": "pbkdf2:sha256:600000$dqymVLMaNiJ9BpP4$f7994561d05a06d5c823a05a8646c8140d3104862be336c2343dbe0aebbc4c32"},
    {"id_user": 6, "email": "WAWA@gmail.com", "password": "pbkdf2:sha256:600000$clkPCBaBbD2el3Vu$05a2f622d2e27c0814867b00ca6a0e5176efd7126955ff907bd7719eacdcd4ab"},
    ]

    session.execute(insert_query, data_to_insert)
    session.commit()

    # 關閉連線
    session.close()
select()