from gensim.models import Word2Vec

def word2vec(kw):
  try:
    loaded_model = Word2Vec.load('project_model_0906.model')
    similar_words = loaded_model.wv.most_similar(kw, topn=3)
    filtered_words = [word for word, score in similar_words if score > 0.5]
  except KeyError:
    filtered_words = "None"
  print("延伸:",filtered_words)
  return filtered_words


