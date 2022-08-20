from gensim.models import Word2Vec
from gensim.models import KeyedVectors

loaded_model = KeyedVectors.load_word2vec_format("eng_w2v") # 모델 로드

model_result = loaded_model.most_similar("service")
for word, per in model_result:
    print(word, per)