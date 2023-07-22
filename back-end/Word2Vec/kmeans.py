from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
kw_list = ['統一獅','統一獅隊', '獅隊', '悍將', '猛獅', '蘇智傑', '陳傑憲', '樂天桃猿隊', '林岳平', '勝騎士', '胡金龍']  # 以您的關鍵字為例
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(kw_list)
k = 5  # 根據您提供的例子，這裡將分為3個群組
kmeans = KMeans(n_clusters=k)
kmeans.fit(X)
labels = kmeans.labels_
representative_keywords = {}
for i, label in enumerate(labels):
    keyword = kw_list[i]
    if label not in representative_keywords:
        representative_keywords[label] = keyword
        
representative_keywords_array = list(representative_keywords.values())
print(representative_keywords_array)