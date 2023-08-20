from ckiptagger import construct_dictionary, WS
from keybert import KeyBERT
from sklearn.feature_extraction.text import CountVectorizer

kw_list=[]
ws = WS("./data")

def ws_zh(text):
    words = ws([text])
    return words[0]


def get_keyword(title,sum): 
    vectorizer =CountVectorizer()
    all_keywords = {}

    title_text=' '.join(ws_zh(title))
    sum_text=' '.join(ws_zh(sum))

    kw_model = KeyBERT(model='distiluse-base-multilingual-cased-v1')

    title_keywords= kw_model.extract_keywords(title_text,vectorizer=vectorizer, top_n=3)
    title_keyword = [keyword[0] for keyword in title_keywords]
    # 將關鍵字當成key存，權重當value存
    for keyword in title_keywords:
        all_keywords[keyword[0]] = keyword[1]

    sum_keywords= kw_model.extract_keywords(sum_text,vectorizer=vectorizer, top_n=3)
    sum_keyword= [keyword[0] for keyword in sum_keywords]
    # 將關鍵字當成key存，權重當value存
    for keyword in sum_keywords:
        all_keywords[keyword[0]] = keyword[1]

    merged_keywords = title_keyword + sum_keyword
    merged_string = ' '.join(merged_keywords)
    
    return merged_string,all_keywords