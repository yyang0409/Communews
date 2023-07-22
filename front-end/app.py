
from concurrent.futures import ThreadPoolExecutor
import datetime as dt  # 將 datetime 模組重新命名為 'dt' 來避免衝突
from flask import Flask,render_template,url_for,redirect,request, flash,session,g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from flask import jsonify
import pymysql
from authlib.integrations.flask_client import OAuth
from search_news import *
from word2vec import *

myclient = pymongo.MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")
# 建立資料庫連接
def connect_db():
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
    return connection


app = Flask( 
    __name__,
    static_folder='static',
    static_url_path='/'
)
#  會使用到session，故為必設
app.secret_key = 'NCUMIS' 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self,user_id, email, password):
        self.user_id = user_id
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return self.user_id

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader  
def user_loader(user_id):  
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM tb_user WHERE id_user = %s"
    cursor.execute(query, (user_id))
    result = cursor.fetchone()
    if result:
        user_id = result['id_user']
        email = result['email']
        password = result['password']
        user = User(user_id,email, password)
        return user
    return None

@app.route("/login",methods=['GET','POST'])
def login():
    db = connect_db()
    if request.method == 'POST':
        # 获取表单数据
        input_email = request.form['email']
        input_password = request.form['password']

        # 查询数据库以获取用户
        cursor = db.cursor()
        query = "SELECT * FROM tb_user WHERE email = %s"
        cursor.execute(query, (input_email))
        result = cursor.fetchone()

        # 验证邮箱和密码
        if result and check_password_hash(result['password'], input_password):
            # 构造 User 对象
            user = User(result['id_user'],result['email'], result['password'])
            login_user(user)  # 登录用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页
        else:
            flash('Invalid email or password.')  # 如果验证失败，显示错误消息
            return redirect(url_for('login'))  # 重定向回登录页

    return render_template('login.html')


@app.route("/register",methods=['GET','POST'])
def register():
    db = connect_db()
    if request.method == 'POST':
        # 获取表单数据
        input_email = request.form['email']
        input_password = request.form['password']
        input_repeat_password = request.form['password-repeat']

        # 验证输入
        if input_password != input_repeat_password:
            flash('Two passwords are different.')
            return redirect(url_for('register'))

        # 检查是否已注册
        cursor = db.cursor()
        query = "SELECT * FROM tb_user WHERE email = %s"
        cursor.execute(query, (input_email,))
        result = cursor.fetchone()
        if result:
            flash('Email has already been registered.')
            return redirect(url_for('register'))

        # 生成密码哈希值
        password_hash = generate_password_hash(input_password)

        # 执行插入操作
        query = "INSERT INTO tb_user (email, password) VALUES (%s, %s)"
        cursor.execute(query, (input_email, password_hash))
        db.commit()

        flash("Thank you for registering.")
        return redirect(url_for('login'))

    return render_template('register.html')


# 建立網站首頁的回應方式
@app.route("/")
def index():
    topics=["運動","生活","國際","娛樂","社會地方","科技","健康","財經"]

    combined_data = []
    # 使用线程池并行处理获取数据
    with ThreadPoolExecutor() as executor:
        # 并行获取各个主题的数据
        futures = [executor.submit(get_DB_News_data, topic,50) for topic in topics]

        # 收集各个主题的数据
        for future in futures:
            combined_data.extend(future.result())

    # 按照timestamp字段排序
    sorted_data = sorted(combined_data, key=lambda x: x['timestamp'], reverse=True)

    return render_template('newest.html', news_list=sorted_data,user=g.user)

def kw_loader(kw):  
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM tb_keyword WHERE value = %s"
    cursor.execute(query, kw)
    result = cursor.fetchone()
    if result:
        kw_id = result['id_keyword']
        return kw_id
    else:
        sql_insert = "INSERT INTO tb_keyword (value) VALUES (%s)"
        data = (kw)
        cursor.execute(sql_insert, data)
        # 提交變更
        db.commit()
        return kw_loader(kw)
    
def collection_loader(kw):  
    id_keyword=kw_loader(kw)
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM tb_collection_record WHERE id_keyword = %s AND id_user=%s"
    cursor.execute(query, (id_keyword,current_user.user_id))
    result = cursor.fetchone()
    if result:
        have = 'Y'
        ISLIKE = result['islike']
        return ISLIKE,have
    else:
        have = 'N'
        ISLIKE = 'N'
        return ISLIKE,have

@app.route("/hot", methods=['GET','POST'])
def hot():
    like_status_dict={}
    if request.method == 'GET':
        data =hot_all_search_news("daily")
        like_status_dict = {keyword: collection_loader(keyword)[0] for keyword in data.keys()}
        return render_template('hot.html', data=data,like_status_dict=like_status_dict,user=g.user)
    elif request.method == 'POST':
        db = connect_db()
        cursor = db.cursor()
        data_id = request.form.get('data_id')
        ISLIKE = request.form.get('like_status')
        if ISLIKE == 'Y' :
            if collection_loader(data_id)[1] =="Y":
                sql_insert = "UPDATE tb_collection_record SET islike =%s ,date=%s WHERE id_user = %s AND id_keyword=%s "
                data = (ISLIKE,(dt.date.today().strftime("%Y-%m-%d")),current_user.user_id, kw_loader(data_id))
            else:
                sql_insert = "INSERT INTO tb_collection_record (id_user,id_keyword,islike,rating,date) VALUES (%s,%s,%s,%s,%s)"
                data = (current_user.user_id, kw_loader(data_id), ISLIKE, 5, (dt.date.today().strftime("%Y-%m-%d")))

            cursor.execute(sql_insert, data)
            # 提交變更
            db.commit()
        elif ISLIKE == 'N' :
            sql_insert = "UPDATE tb_collection_record SET islike =%s ,date=%s WHERE id_user = %s AND id_keyword=%s "
            data = (ISLIKE,(dt.date.today().strftime("%Y-%m-%d")),current_user.user_id, kw_loader(data_id))
            cursor.execute(sql_insert, data)
            # 提交變更
            db.commit()
        # 回傳JSON格式的回應給前端
        return jsonify({'message': '成功接收data_id！', 'data_id': data_id,'ISLIKE':ISLIKE})
    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"

# 熱門頁面-每週
@app.route("/hot/evevyweek", methods=['GET','POST'])
def evevyweek():
    like_status_dict={}
    if request.method == 'GET':
        data =hot_all_search_news("weekly")
        like_status_dict = {keyword: collection_loader(keyword)[0] for keyword in data.keys()}
        return render_template('hot_everyweek.html', data=data,like_status_dict=like_status_dict,user=g.user)
    elif request.method == 'POST':
        db = connect_db()
        cursor = db.cursor()
        data_id = request.form.get('data_id')
        ISLIKE = request.form.get('like_status')
        if ISLIKE == 'Y' :
            if collection_loader(data_id)[1] =="Y":
                sql_insert = "UPDATE tb_collection_record SET islike =%s ,date=%s WHERE id_user = %s AND id_keyword=%s "
                data = (ISLIKE,(dt.date.today().strftime("%Y-%m-%d")),current_user.user_id, kw_loader(data_id))
            else:
                sql_insert = "INSERT INTO tb_collection_record (id_user,id_keyword,islike,rating,date) VALUES (%s,%s,%s,%s,%s)"
                data = (current_user.user_id, kw_loader(data_id), ISLIKE, 5, (dt.date.today().strftime("%Y-%m-%d")))

            cursor.execute(sql_insert, data)
            # 提交變更
            db.commit()
        elif ISLIKE == 'N' :
            sql_insert = "UPDATE tb_collection_record SET islike =%s ,date=%s WHERE id_user = %s AND id_keyword=%s "
            data = (ISLIKE,(dt.date.today().strftime("%Y-%m-%d")),current_user.user_id, kw_loader(data_id))
            cursor.execute(sql_insert, data)
            # 提交變更
            db.commit()
        # 回傳JSON格式的回應給前端
        return jsonify({'message': '成功接收data_id！', 'data_id': data_id,'ISLIKE':ISLIKE})
    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"

# 熱門頁面-每月
@app.route("/hot/evevymonth", methods=['GET','POST'])
def evevymonth():
    like_status_dict={}
    if request.method == 'GET':
        data =hot_all_search_news("monthly")
        like_status_dict = {keyword: collection_loader(keyword)[0] for keyword in data.keys()}
        return render_template('hot_everymonth.html', data=data,like_status_dict=like_status_dict,user=g.user)
    elif request.method == 'POST':
        db = connect_db()
        cursor = db.cursor()
        data_id = request.form.get('data_id')
        ISLIKE = request.form.get('like_status')
        if ISLIKE == 'Y' :
            if collection_loader(data_id)[1] =="Y":
                sql_insert = "UPDATE tb_collection_record SET islike =%s ,date=%s WHERE id_user = %s AND id_keyword=%s "
                data = (ISLIKE,(dt.date.today().strftime("%Y-%m-%d")),current_user.user_id, kw_loader(data_id))
            else:
                sql_insert = "INSERT INTO tb_collection_record (id_user,id_keyword,islike,rating,date) VALUES (%s,%s,%s,%s,%s)"
                data = (current_user.user_id, kw_loader(data_id), ISLIKE, 5, (dt.date.today().strftime("%Y-%m-%d")))

            cursor.execute(sql_insert, data)
            # 提交變更
            db.commit()
        elif ISLIKE == 'N' :
            sql_insert = "UPDATE tb_collection_record SET islike =%s ,date=%s WHERE id_user = %s AND id_keyword=%s "
            data = (ISLIKE,(dt.date.today().strftime("%Y-%m-%d")),current_user.user_id, kw_loader(data_id))
            cursor.execute(sql_insert, data)
            # 提交變更
            db.commit()
        # 回傳JSON格式的回應給前端
        return jsonify({'message': '成功接收data_id！', 'data_id': data_id,'ISLIKE':ISLIKE})
    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"


@app.route("/show",  methods=['POST'])
def show():
    if request.method == 'POST':
        combined_data = {}
        keyword = request.form.get("keyword", "")
        data =kw_search_news(keyword)
        combined_data.update(data)
        extend_keywords=word2vec(keyword)
        if extend_keywords!="None":
            for extend_keyword in extend_keywords:
                extend_data=kw_search_news(extend_keyword)
                combined_data.update(extend_data)
        return render_template('show.html',combined_data=combined_data,user=g.user)
    
    return redirect(url_for('index'))  


# topic頁面預設是最新新聞
@app.route("/topic/<topicname>")
def topic(topicname):
    news_list=get_DB_News_data(topicname,100)
    return render_template('topic.html',topicname=topicname,news_list=news_list,user=g.user)

# topic的熱門新聞頁面
@app.route("/topic/<topicname>/熱門")
def topicHot(topicname):
    return render_template('topic_hot.html',topicname=topicname,user=g.user)

@app.route("/topic/<topicname>/熱門/當週")
def topic_hot_week(topicname):
    return render_template('topic_hot_week.html',topicname=topicname,user=g.user)

@app.route("/topic/<topicname>/熱門/當月")
def topic_hot_month(topicname):
    return render_template('topic_hot_month.html',topicname=topicname,user=g.user)

@app.route("/recommendation")
#@login_required
def recommendation():
    return render_template('recommendation.html',user=g.user)


@app.route("/collection")
# @login_required
def collection():
    return render_template('collection.html',user=g.user)


@app.route("/logout")
@login_required
def logout():
    # 登出用户
    logout_user()

    # 移除会话的持久性
    session.permanent = False

    # 移除会话数据
    session.clear()

    # 重定向到登录页或其他页面
    return redirect(url_for('login'))

# 處理收藏關鍵字的下拉式選單
@app.route("/process_value", methods=["POST"])
def process_value():
    selected_value = request.form.get("selectedValue")
    # Do whatever processing you need with the selected_value
    # For example, you can perform database operations or business logic.
    # Replace the following line with the desired processing.
    result = f"Received selected value: {selected_value}"
    return jsonify(result)


# 啟動網站伺服器
if __name__ == '__main__':
    app.run(debug=True)
