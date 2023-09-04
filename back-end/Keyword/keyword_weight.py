import pymongo 
from ckiptagger import construct_dictionary, WS
from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer
# from ckiptagger import data_utils
# data_utils.download_data_gdown("./")

myclient = pymongo.MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/?retryWrites=true&w=majority")

kw_list=[]
ws = WS("./data")

def main():
    topics = ['健康','國際','娛樂','生活','社會地方','科技','財經','運動']

    # 連接cluster News
    db = myclient['News']

    for topic in topics:
        # 連接資料庫的collection
        collection = db[topic]

        # 從資料庫取新聞標題和摘要
        result = collection.find({},{'_id':1,'title':1,'summary':1})

        # 印出新聞標題和摘要
        for data in result:
            merged_string,all_keywords = get_keyword_weight(data['title'],data['summary'])
            print(merged_string)
            print(all_keywords)
            # 將mergerd_keywords存進new_keyword 覆蓋掉 避免keybert結果會有不一樣的keyword產生 皆用最新的keyword
            collection.update_one({'_id':data['_id']},{'$set':{'new_keyword':merged_string}})
            # 在資料庫新一欄位 => 字典型態存關鍵字+權重
            collection.update_many({'_id':data['_id']},{'$set':{'keyword_weight':all_keywords}})


def ws_zh(text):
    words = ws([text])
    return words[0]


def get_keyword_weight(title,sum): 
    vectorizer =CountVectorizer()
    all_keywords = {}

    title_text=' '.join(ws_zh(title))
    sum_text=' '.join(ws_zh(sum))

    kw_model = KeyBERT(model='distiluse-base-multilingual-cased-v1')

    # 標題關鍵字and權重    
    title_keywords= kw_model.extract_keywords(title_text,vectorizer=vectorizer, top_n=3)

    for keyword in title_keywords:
        all_keywords[keyword[0]] = keyword[1]  

    # 取標題關鍵字    
    title_keyword = [keyword[0] for keyword in title_keywords]

    # 摘要關鍵字and權重
    sum_keywords= kw_model.extract_keywords(sum_text,vectorizer=vectorizer, top_n=3)

    for keyword in sum_keywords:
        all_keywords[keyword[0]] = keyword[1]  

    # 取摘要關鍵字
    sum_keyword= [keyword[0] for keyword in sum_keywords]

    # 將標題關鍵字和摘要關鍵字合成一個陣列儲存
    merged_keywords = title_keyword + sum_keyword
    merged_string = ' '.join(merged_keywords)
    # 回傳關鍵字字串
    return merged_string , all_keywords


if __name__ == '__main__':
    main()
