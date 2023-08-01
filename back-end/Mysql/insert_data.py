import pymysql
from werkzeug.security import generate_password_hash


# 建立 MySQL 連接
db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "109403502",
        "db": "communews",
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor
    }
connection = pymysql.connect(**db_settings)

def hash(password):
    # 產生密碼的哈希值
    hashed_password = generate_password_hash(password)
    print(hashed_password)
    return hashed_password

# 建立資料庫游標
cursor = connection.cursor()

##USER TABLE#################################################################################

# 執行 SQL INSERT 語句插入資料
sql_insert = "INSERT INTO tb_user (email,password) VALUES (%s, %s)"
data = ('109403516@gmail.com', hash('109403516'))
cursor.execute(sql_insert, data)
# 提交變更
connection.commit()

#############################################################################################



# 關閉游標和連接
cursor.close()
connection.close()