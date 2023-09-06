
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
from choose_ptt_title import *

import numpy as np
from heapq import nlargest
import ast


myclient = pymongo.MongoClient("mongodb+srv://user2:user2@cluster0.zgtguxv.mongodb.net/?retryWrites=true&w=majority")
# 建立資料庫連接
def connect_db():
    db_settings = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "Jeter#622019",
            "db": "communews",
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor
        }
    connection = pymysql.connect(**db_settings)
    return connection   
def news_score_loader(user_id,news_id):  
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT * FROM tb_news_score WHERE id_user = %s AND id_news= %s"
    cursor.execute(query, (user_id,news_id))
    result = cursor.fetchone()
    if result:
        have ='Y'
        score =result ['score']
        return have,score
    else:
        have ='N'
        score = 0
        return have,score
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
def user_collection_loader():
    db = connect_db()
    cursor = db.cursor()
    query1 = "SELECT * FROM tb_collection_record WHERE id_user=%s AND islike ='Y' "
    cursor.execute(query1, (current_user.user_id))
    results1 = cursor.fetchall()  # 獲取所有結果

    collection_kw_nm = []  # 用於存儲收藏的關鍵字ID

    for index, result in enumerate(results1, start=1):
        kw_id = result['id_keyword']
        query2 = "SELECT * FROM tb_keyword WHERE id_keyword=%s"
        cursor.execute(query2, (kw_id))
        results2 = cursor.fetchone()  
        keyword = results2['value']
        collection_kw_nm.append((index, keyword))

    return collection_kw_nm
def do_like(request):
    db = connect_db()
    cursor = db.cursor()
    data = request.json
    data_id = data.get('data_id')
    ISLIKE = data.get('like_status')
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
        
def do_rating(request):
    record_view(request)

    db = connect_db()
    cursor = db.cursor()
    data = request.json
    news_id = data.get('news_id')
    news_topic = data.get('topic')
    rating = data.get('rating')
    # news_keyword_weight = data.get('keyword')
    have,score=news_score_loader(current_user.user_id,news_id)
    # news_keyword_weight = caculate_rating_weight(news_keyword_weight)
    #如果存在 就改分數
    if have =='Y':
        sql_insert = "UPDATE tb_news_score SET score=%s WHERE id_user =%s AND id_news=%s "
        data = (rating,current_user.user_id,news_id)
        cursor.execute(sql_insert, data)
        # 提交變更
        db.commit()
    #如果不存在 就加入資料
    elif have=='N':
        sql_insert = "INSERT INTO tb_news_score (id_user,id_news,news_topic,score) VALUES (%s,%s,%s,%s)"
        data = (current_user.user_id,news_id,news_topic,rating)
        cursor.execute(sql_insert, data)       
        # 提交變更
        db.commit()

def caculate_rating_weight(rating,news_keyword_weight):
    # 將新聞關鍵字的權重都乘上評分的值
    for key in news_keyword_weight:
        news_keyword_weight[key] = news_keyword_weight[key] * rating

    return news_keyword_weight

def record_view(request):
    mysql_db = connect_db()
    cursor = mysql_db.cursor()
    data = request.json
    action = data.get('action') # 執行的動作
    news_id = data.get('news_id') # 正在觀看的新聞id
    news_keyword  = data.get('keyword_weight') # 新聞關鍵字 & 權重
    mutiple_rate = 1.0

    print(action)

    if action == 'rating':
        rating = str(data.get('rating'))
        match rating:
            case "1": # 權重乘 0.5
                mutiple_rate = 0.5
            case "2": # 權重乘 0.8
                mutiple_rate = 0.8
            case "3": # 權重乘 1
                mutiple_rate = 1.0
            case "4": # 權重乘 1.1
                mutiple_rate = 1.1
            case "5": # 權重乘 1.2
                mutiple_rate = 1.2
    elif action == 'view':
        mutiple_rate = 1.0

    print(type(rating))
    print(mutiple_rate)
    if news_keyword == "nan": # 若沒有關鍵字 & 權重，直接存nan
        json_news_keyword = json.dumps(news_keyword)
        query = "INSERT INTO tb_news_view (id_user,id_news,news_keyword,date) VALUES (%s,%s,%s,%s)"
        insert_data = (current_user.user_id,news_id,json_news_keyword,dt.date.today().strftime("%Y-%m-%d"))
        cursor.execute(query,insert_data)
        mysql_db.commit()
    else:
        dict_news_keyword = eval(news_keyword) # 轉成dict type
        json_news_keyword = json.dumps(dict_news_keyword) # 轉成 JSON strgin 格式
        print(dict_news_keyword)
        print(type(dict_news_keyword))
        query = "INSERT INTO tb_news_view (id_user,id_news,news_keyword,date) VALUES (%s,%s,%s,%s)"
        insert_data = (current_user.user_id,news_id,json_news_keyword,dt.date.today().strftime("%Y-%m-%d"))
        cursor.execute(query,insert_data)
        mysql_db.commit()

        keyword_compare(current_user.user_id,json_news_keyword,mutiple_rate)

# 比對觀看新聞的關鍵字與該user所有看過新聞的關鍵字有無一樣的關鍵字，若有則將權重相加並記錄到tb_user_keyword_weight
def keyword_compare(user_id,json_news_keyword,mutiple_rate):
    mysql_db = connect_db()
    cursor = mysql_db.cursor()
    query = "SELECT * FROM tb_user_keyword_weight WHERE id_user = %s" # 抓取使用者的關鍵字字典
    cursor.execute(query,(user_id))
    result = cursor.fetchone()
    print(result)
    if result['keyword_list'] is None:
        query = "UPDATE tb_user_keyword_weight SET keyword_list = %s WHERE id_user = %s"
        cursor.execute(query,(json_news_keyword,user_id))
        mysql_db.commit()
    else:    
        user_keyword_weight = json.loads(result['keyword_list']) # user 看過新聞的所有關鍵字 型態為dictionary
        user_keyword_weight = calculate_keyword_weight(user_keyword_weight,json_news_keyword,mutiple_rate)
        json_user_keyword_weight = json.dumps(user_keyword_weight)
        # 更新使用者關鍵字字典
        query = "UPDATE tb_user_keyword_weight SET keyword_list = %s WHERE id_user = %s"
        cursor.execute(query,(json_user_keyword_weight,user_id))
        mysql_db.commit()
    
        
def calculate_keyword_weight(user_keyword_weight,json_news_keyword,mutiple_rate):
    news_keyword_weight = json.loads(json_news_keyword) # dict type

    user_keywords = list(user_keyword_weight.keys()) # 使用者關鍵字list (沒有權重
    news_keywords = list(news_keyword_weight.keys()) # 新聞關鍵字list (沒有權重)

    common_keywords = set(user_keywords) & set(news_keywords) # 使用者有看過且該新聞也有的關鍵字
    keywords_only_in_news = set(news_keywords) - set(user_keywords) # 使用者沒看過的關鍵字

    # 將相同關鍵字的權重相加並更新於使用者關鍵字字典
    for com_keyword in common_keywords:
        user_keyword_weight[com_keyword] = user_keyword_weight[com_keyword] + news_keyword_weight[com_keyword] * mutiple_rate

    # 將使用者沒看過得關鍵字新增至使用者關鍵字字典
    for keyword in keywords_only_in_news:
        user_keyword_weight[keyword] = news_keyword_weight[keyword] * mutiple_rate

    # 將使用者關鍵字字典排序
    keys = list(user_keyword_weight.keys())
    values = list(user_keyword_weight.values())

    sorted_values_index = np.argsort(values) # 根據weight大小排序，存weight的index值

    user_keyword_weight = {keys[index]: values[index] for index in sorted_values_index} # dict type

    return user_keyword_weight
    
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
        query = "INSERT INTO tb_user (email, password) VALUES (%s, %s);"
        cursor.execute(query, (input_email, password_hash))
        db.commit()

        # 創建user的keyword_weight_list
        # 先抓id_user
        query = "SELECT LAST_INSERT_ID(id_user) from tb_user order by LAST_INSERT_ID(id_user) desc limit 1;"
        cursor.execute(query)
        result = cursor.fetchone()
        id_user = result['LAST_INSERT_ID(id_user)']
        query = "INSERT INTO tb_user_keyword_weight (id_user) VALUES (%s);"
        cursor.execute(query,(id_user))
        db.commit()

        flash("Thank you for registering.")
        return redirect(url_for('login'))

    return render_template('register.html')


# 建立網站首頁的回應方式
@app.route("/", methods=['GET','POST'])
def index():
    db=myclient['Kmeans新聞']
    collection=db['最新']
    if request.method == 'GET':
        if g.user.is_authenticated:
            result = collection.find_one({'topic':'綜合全部','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            #print(result)
            # 取得當前用戶ID
            current_user_id = g.user.user_id if g.user.is_authenticated else None
            # 逐一查詢每筆新聞的評分分數，並加回到sorted_data中
            for news in result['news_list']:
                if current_user_id:
                    # 從資料庫查詢用戶之前對該新聞的評分
                    have, score = news_score_loader(current_user_id, news['_id'])
                    if have == 'Y':
                        # 如果用戶之前有評分，將評分分數加回到sorted_data中
                        news['rating'] = score
                    else:
                        # 如果用戶之前沒有評分，設置評分為0
                        news['rating'] = 0
                else:
                    # 如果用戶未登入，設置評分為0
                    news['rating'] = 0
            return render_template('newest.html', news_list=result['news_list'],user=g.user)
        else:
            result = collection.find_one({'topic':'運動','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            return render_template('newest.html', news_list=result['news_list'],user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action =='rating':
                do_rating(request)
                return jsonify({'message':"評分成功"})
            elif action =='view':
                record_view(request)
                return jsonify({'message':"觀看成功"})


@app.route("/hot", methods=['GET', 'POST'])
def hot():
    like_status_dict = {}
    stars_count_dict = {}  # 用於存儲每個新聞的星星數量
    data={}
    db=myclient['Kmeans新聞']
    collection=db['當日熱門']
    if request.method == 'GET':
        if g.user.is_authenticated:
            results = collection.find({'topic':'綜合全部','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                like_status_dict.update({result['keyword']:collection_loader(result['keyword'])[0]})
                # 計算每個新聞的星星數量
                for news in result['news_list']:
                    have, score = news_score_loader(g.user.user_id, news['_id'])
                     #print(str_news_id, have, score)
                    if have == 'Y':
                        stars_count_dict[news['_id']] = score
                    else:
                        stars_count_dict[news['_id']] = 0
                data[result['keyword']] = result['news_list'][:4]
            return render_template('hot.html', data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
        else:
            results = collection.find({'topic':'綜合全部','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                data[result['keyword']] = result['news_list'][:4]
            return render_template('hot.html', data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action == 'like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action == 'rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message': '觀看成功'})
    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"


# 熱門頁面-每週
@app.route("/hot/當週熱門", methods=['GET','POST'])
def everyweek():
    like_status_dict={}
    stars_count_dict = {}  # 用於存儲每個新聞的星星數量
    data={}
    db=myclient['Kmeans新聞']
    collection=db['當週熱門']
    if request.method == 'GET':
        if g.user.is_authenticated:
            results = collection.find({'topic':'綜合全部','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                like_status_dict.update({result['keyword']:collection_loader(result['keyword'])[0]})
                # 計算每個新聞的星星數量
                for news in result['news_list']:
                    have, score = news_score_loader(g.user.user_id, news['_id'])
                     #print(str_news_id, have, score)
                    if have == 'Y':
                        stars_count_dict[news['_id']] = score
                    else:
                        stars_count_dict[news['_id']] = 0
                data[result['keyword']] = result['news_list'][:4]
            return render_template('hot_everyweek.html', data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
        else:
            results = collection.find({'topic':'綜合全部','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                data[result['keyword']] = result['news_list'][:4]
            return render_template('hot_everyweek.html', data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)                
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message': '觀看成功'})
    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"

# 熱門頁面-每月
@app.route("/hot/當月熱門", methods=['GET','POST'])
def everymonth():
    like_status_dict={}
    stars_count_dict = {}  # 用於存儲每個新聞的星星數量
    data={}
    db=myclient['Kmeans新聞']
    collection=db['當月熱門']
    if request.method == 'GET':
        if g.user.is_authenticated:
            results = collection.find({'topic':'綜合全部','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                like_status_dict.update({result['keyword']:collection_loader(result['keyword'])[0]})
                # 計算每個新聞的星星數量
                for news in result['news_list']:
                    have, score = news_score_loader(g.user.user_id, news['_id'])
                     #print(str_news_id, have, score)
                    if have == 'Y':
                        stars_count_dict[news['_id']] = score
                    else:
                        stars_count_dict[news['_id']] = 0
                data[result['keyword']] = result['news_list'][:4]
            return render_template('hot_everymonth.html', data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
        else:
            results = collection.find({'topic':'綜合全部','date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                data[result['keyword']] = result['news_list'][:4]
            return render_template('hot_everymonth.html', data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message': '觀看成功'})
    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"

# topic頁面預設是最新新聞
@app.route("/topic/<topicname>", methods=['GET','POST'])
def topic(topicname):
    db=myclient['Kmeans新聞']
    collection=db['最新']
    if request.method == 'GET':
        if g.user.is_authenticated:
            result = collection.find_one({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            #print(result)
            # 取得當前用戶ID
            current_user_id = g.user.user_id if g.user.is_authenticated else None
            # 逐一查詢每筆新聞的評分分數，並加回到sorted_data中
            for news in result['news_list']:
                if current_user_id:
                    # 從資料庫查詢用戶之前對該新聞的評分
                    have, score = news_score_loader(current_user_id, news['_id'])
                    if have == 'Y':
                        # 如果用戶之前有評分，將評分分數加回到sorted_data中
                        news['rating'] = score
                    else:
                        # 如果用戶之前沒有評分，設置評分為0
                        news['rating'] = 0
                else:
                    # 如果用戶未登入，設置評分為0
                    news['rating'] = 0
            return render_template('topic.html', topicname=topicname, news_list=result['news_list'],user=g.user)
        else:
            result = collection.find_one({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            return render_template('topic.html', topicname=topicname, news_list=result['news_list'],user=g.user)
            #print(result)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message': '觀看成功'})
 

# topic的熱門新聞頁面
@app.route("/topic/<topicname>/熱門", methods=['GET','POST'])
def topicHot(topicname):
    like_status_dict={}
    stars_count_dict = {}  # 用於存儲每個新聞的星星數量
    data={}
    db=myclient['Kmeans新聞']
    collection=db['當日熱門']
    if request.method == 'GET':
        if g.user.is_authenticated:
            results = collection.find({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                like_status_dict.update({result['keyword']:collection_loader(result['keyword'])[0]})
                # 計算每個新聞的星星數量
                for news in result['news_list']:
                    have, score = news_score_loader(g.user.user_id, news['_id'])
                     #print(str_news_id, have, score)
                    if have == 'Y':
                        stars_count_dict[news['_id']] = score
                    else:
                        stars_count_dict[news['_id']] = 0
                data[result['keyword']] = result['news_list'][:4]
            return render_template('topic_hot.html', topicname=topicname,data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
        else:
            results = collection.find({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                data[result['keyword']] = result['news_list'][:4]
            return render_template('topic_hot.html', topicname=topicname,data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message': '觀看成功'})

    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"

@app.route("/topic/<topicname>/熱門/當週", methods=['GET','POST'])
def topic_hot_week(topicname):
    like_status_dict={}
    stars_count_dict = {}  # 用於存儲每個新聞的星星數量
    data={}
    db=myclient['Kmeans新聞']
    collection=db['當週熱門']    
    if request.method == 'GET':
        if g.user.is_authenticated:
            results = collection.find({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                like_status_dict.update({result['keyword']:collection_loader(result['keyword'])[0]})
                # 計算每個新聞的星星數量
                for news in result['news_list']:
                    have, score = news_score_loader(g.user.user_id, news['_id'])
                     #print(str_news_id, have, score)
                    if have == 'Y':
                        stars_count_dict[news['_id']] = score
                    else:
                        stars_count_dict[news['_id']] = 0
                data[result['keyword']] = result['news_list'][:4]
            return render_template('topic_hot_week.html', topicname=topicname,data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
        else:
            results = collection.find({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                data[result['keyword']] = result['news_list'][:4]
            return render_template('topic_hot_week.html',topicname=topicname, data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message': '觀看成功'})

    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"

@app.route("/topic/<topicname>/熱門/當月", methods=['GET','POST'])
def topic_hot_month(topicname):
    like_status_dict={}
    stars_count_dict = {}  # 用於存儲每個新聞的星星數量
    data={}
    db=myclient['Kmeans新聞']
    collection=db['當月熱門']
    if request.method == 'GET':
        if g.user.is_authenticated:
            results = collection.find({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                like_status_dict.update({result['keyword']:collection_loader(result['keyword'])[0]})
                # 計算每個新聞的星星數量
                for news in result['news_list']:
                    have, score = news_score_loader(g.user.user_id, news['_id'])
                     #print(str_news_id, have, score)
                    if have == 'Y':
                        stars_count_dict[news['_id']] = score
                    else:
                        stars_count_dict[news['_id']] = 0
                data[result['keyword']] = result['news_list'][:4]
            return render_template('topic_hot_month.html',topicname=topicname, data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
        else:
            results = collection.find({'topic':topicname,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
            for result in results :
                data[result['keyword']] = result['news_list'][:4]
            return render_template('topic_hot_month.html', topicname=topicname,data=data, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict, user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message': '觀看成功'})

    else:
        # 在其他情況下也要處理返回有效的回應
        return "Invalid request method"

@app.route("/recommendation",methods=['GET','POST'])
@login_required
def recommendation():
    mysql_db = connect_db()
    cursor = mysql_db.cursor()

    stars_count_dict = {}
    like_status_dict={}
    combined_data = {}
    
    if request.method == 'GET':
        if g.user.is_authenticated:
            query = ' SELECT * FROM tb_user_keyword_weight WHERE id_user = %s'
            cursor.execute(query,g.user.user_id)
            result = cursor.fetchone()
            keyword_dict = json.loads(result['keyword_list']) # 使用者的關鍵字字典
            # 取前5個 keyword display 在網頁上
            N = 3 # 要取的關鍵字數目 
            top_ten_keywords = nlargest(N,keyword_dict,key=keyword_dict.get) # 型態為list
            print(top_ten_keywords)
            # 根據這10個關鍵字去mongodb撈新聞
            
            data,all_data = recommend_news(top_ten_keywords)
            combined_data.update(data)

            # 判斷有無收藏該關鍵字
            like_status_dict = {keyword: collection_loader(keyword)[0] for keyword in combined_data.keys()}

            for keyword, news_list in data.items():
                for news_dict in news_list:                        
                    news_id = news_dict.get('_id')
                    # 將 ObjectId 轉換成字符串形式
                    str_news_id = str(news_id)
                    have, score = news_score_loader(g.user.user_id, str_news_id)
                    #print(str_news_id, have, score)
                    if have == 'Y':
                        stars_count_dict[news_id] = score
                    else:
                        stars_count_dict[news_id] = 0
                        
            return render_template('recommendation.html',top_ten_keywords=top_ten_keywords, combined_data=combined_data,stars_count_dict = stars_count_dict,like_status_dict = like_status_dict,user = g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action =='view':
                record_view(request)
                return jsonify({'message':"觀看成功"})


@app.route("/collection/", defaults={'keyword': None}, methods=['GET','POST'])
@app.route("/collection/<string:keyword>", methods=['GET','POST'])
@login_required
def collection(keyword):
    stars_count_dict = {}
    collection_kw_nm=user_collection_loader()
    if request.method == 'GET':
        if g.user.is_authenticated:
            if keyword == None :
                data,all_data=gen_kw_search_news(collection_kw_nm[0][1])
            else:
                data,all_data=gen_kw_search_news(keyword)
            # 計算每個新聞的星星數量
            for keyword, news_list in data.items():
                for news_dict in news_list:
                    news_id = news_dict.get('_id')
                    # 將 ObjectId 轉換成字符串形式
                    str_news_id = str(news_id)
                    have, score = news_score_loader(g.user.user_id, str_news_id)
                    #print(str_news_id, have, score)

                    if have == 'Y':
                        stars_count_dict[news_id] = score
                    else:
                        stars_count_dict[news_id] = 0
            #print(data)
            
            return render_template('collection.html',keyword=keyword,collection_kw_nm=collection_kw_nm,all_data=all_data,stars_count_dict=stars_count_dict,user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message':"觀看成功"})
 
@app.route("/show",  methods=['POST'])
def show():
    like_status_dict={}
    stars_count_dict={}
    if request.method == 'POST':
        if g.user.is_authenticated:
            # 判斷是否是 AJAX POST 請求
            if request.is_json:
                data = request.json
                action = data.get('action')
                if action == 'like':
                    do_like(request)
                    # 回傳 JSON 格式的回應給前端
                    return jsonify({'message': '收藏成功！'})
                elif action == 'rating':
                    do_rating(request)
                    return jsonify({'message': "評分成功"})
                elif action == 'view':
                    record_view(request)
                    return jsonify({'message':"觀看成功"})
            else:
                combined_data = {}
                keyword = request.form.get("keyword", "")
                data, all_data = gen_kw_search_news(keyword)
                combined_data.update(data)
                # 初始化 extend_keywords 为空集合
                extend_keywords = []
                for keyword, news_list in data.items():
                    # 调用 word2vec() 函数获取与关键字相似的单词列表
                    similar_words = word2vec(keyword)
                    if isinstance(similar_words, list) and similar_words != "None":
                        for word in similar_words:
                            if word not in extend_keywords:
                                extend_keywords.append(word)

                # 将 extend_keywords 集合转换为列表
                #extend_keywords = list(extend_keywords)
                print("extend_keywords:",extend_keywords)
                if extend_keywords != "None":
                    for extend_keyword in extend_keywords:
                        extend_data, all_extend_data_news = gen_kw_search_news(extend_keyword)
                        combined_data.update(extend_data)

                like_status_dict = {keyword: collection_loader(keyword)[0] for keyword in combined_data.keys()}
                # 計算每個新聞的星星數量
                stars_count_dict = {}
                for keyword, news_list in combined_data.items():
                    news_list=choose_ptt_data("",news_list)
                    for news_dict in news_list:
                        news_id = news_dict.get('_id')
                        # 將 ObjectId 轉換成字符串形式
                        str_news_id = str(news_id)
                        have, score = news_score_loader(g.user.user_id, str_news_id)
                        if have == 'Y':
                            stars_count_dict[news_id] = score
                        else:
                            stars_count_dict[news_id] = 0

                return render_template('show.html', combined_data=combined_data, user=g.user, like_status_dict=like_status_dict, stars_count_dict=stars_count_dict)
        else:
            combined_data = {}
            keyword = request.form.get("keyword", "")
            data,all_data =gen_kw_search_news(keyword)
            combined_data.update(data)
            # 初始化 extend_keywords 为空集合
            extend_keywords = []
            for keyword, news_list in data.items():
                # 调用 word2vec() 函数获取与关键字相似的单词列表
                similar_words = word2vec(keyword)
                if isinstance(similar_words, list) and similar_words != "None":
                    for word in similar_words:
                        if word not in extend_keywords:
                            extend_keywords.append(word)
            # 将 extend_keywords 集合转换为列表
            #extend_keywords = list(extend_keywords)
            print("extend_keywords:",extend_keywords)

            if extend_keywords!="None":
                for extend_keyword in extend_keywords:
                    extend_data,all_extend_data_news=gen_kw_search_news(extend_keyword)
                    combined_data.update(extend_data)
            for keyword, news_list in combined_data.items():
                news_list=choose_ptt_data("",news_list)
            return render_template('show.html',combined_data=combined_data, user=g.user,like_status_dict=like_status_dict,stars_count_dict=stars_count_dict)
    return redirect(url_for('index'))   

@app.route("/hashtag/<type>/<topicname>/<keyword>", methods=['GET','POST'])
def hashtag(type,keyword,topicname):
    stars_count_dict = {}
    like_status_dict={}
    
    if request.method == 'GET':
        if g.user.is_authenticated:
            if type!='搜尋':
                db=myclient['Kmeans新聞']
                collection=db[type]
                result = collection.find_one({'topic':topicname,'keyword':keyword,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
                like_status_dict = {keyword: collection_loader(result['keyword'])[0]}
                # 取得當前用戶ID
                current_user_id = g.user.user_id if g.user.is_authenticated else None
                # 逐一查詢每筆新聞的評分分數，並加回到sorted_data中
                for news in result['news_list']:
                    if current_user_id:
                        # 從資料庫查詢用戶之前對該新聞的評分
                        have, score = news_score_loader(current_user_id, news['_id'])
                        if have == 'Y':
                            # 如果用戶之前有評分，將評分分數加回到sorted_data中
                            stars_count_dict[news['_id']] = score
                        else:
                            # 如果用戶之前沒有評分，設置評分為0
                            stars_count_dict[news['_id']] = 0
                    else:
                        # 如果用戶未登入，設置評分為0
                        stars_count_dict[news['_id']] = 0
                #print(result['keyword'])
                return render_template('hashtag.html',type=type,topicname=topicname,keyword=result['keyword'],news_list=result['news_list'],like_status_dict=like_status_dict,stars_count_dict=stars_count_dict,user=g.user)
            else:
                data,all_data =gen_kw_search_news(keyword)
                like_status_dict = {keyword: collection_loader(keyword)[0]}
                # 計算每個新聞的星星數量
                for keyword, news_list in all_data.items():
                    news_list=choose_ptt_data("",news_list)
                    for news_dict in news_list:
                        news_id = news_dict.get('_id')
                        # 將 ObjectId 轉換成字符串形式
                        str_news_id = str(news_id)
                        have, score = news_score_loader(g.user.user_id, str_news_id)
                        #print(str_news_id, have, score)

                        if have == 'Y':
                            stars_count_dict[news_id] = score
                        else:
                            stars_count_dict[news_id] = 0
                return render_template('hashtag.html',type=type,topicname=topicname,keyword=keyword,news_list=news_list,like_status_dict=like_status_dict,stars_count_dict=stars_count_dict,user=g.user)
        else:
            if type!='搜尋':
                db=myclient['Kmeans新聞']
                collection=db[type]
                result = collection.find_one({'topic':topicname,'keyword':keyword,'date':(datetime.now()- timedelta(days=1)).strftime("%Y-%m-%d")})
                return render_template('hashtag.html',type=type,topicname=topicname,keyword=result['keyword'],news_list=result['news_list'],like_status_dict=like_status_dict,stars_count_dict=stars_count_dict,user=g.user)
            else:
                data,all_data =gen_kw_search_news(keyword)
                for keyword, news_list in all_data.items():
                    news_list=choose_ptt_data("",news_list)
                return render_template('hashtag.html',type=type,topicname=topicname,keyword=keyword,news_list=all_data.get(keyword),user=g.user)
    elif request.method == 'POST':
        if g.user.is_authenticated:
            data = request.json
            action = data.get('action')
            if action=='like':
                do_like(request)
                # 回傳JSON格式的回應給前端
                return jsonify({'message': '收藏成功！'})
            elif action =='rating':
                do_rating(request)
                return jsonify({'message': "評分成功"})
            elif action == 'view':
                record_view(request)
                return jsonify({'message':"觀看成功"})
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




# 啟動網站伺服器
if __name__ == '__main__':
    app.run(debug=True)