import re
import urllib.request
import zipfile
from lxml import etree
from nltk.tokenize import word_tokenize, sent_tokenize

targetXML = open('ted_en-20160408.xml', 'r', encoding='UTF8')
target_text = etree.parse(targetXML)
parse_text = '\n'.join(target_text.xpath('//content/text()'))
content_text = re.sub(r'\([^)]*\)', '', parse_text)
sent_text = sent_tokenize(content_text)
normalized_text = []
for string in sent_text:
     tokens = re.sub(r"[^a-z0-9]+", " ", string.lower())
     normalized_text.append(tokens)
result = [word_tokenize(sentence) for sentence in normalized_text]
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
model = Word2Vec(sentences=result, window=5, min_count=5, workers=4, sg=0)
model_result = model.wv.most_similar("man")
model.wv.save_word2vec_format('eng_w2v')