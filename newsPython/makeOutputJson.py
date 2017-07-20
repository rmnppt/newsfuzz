from time import time
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import string
import gensim
from gensim import corpora
import numpy as np
import pprint
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
#nltk.download()
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

def get_topic_word_ids(model, topic_idx):
    topic = model.components_[topic_idx]
    return [i for i in topic.argsort()]

def id_to_word(feature_names, word_ids):
    return [feature_names[i] for i in word_ids]

def get_topic_words(model, feature_names, topic_idx, n_top_words=5):
    print("Topic #%d:" % topic_idx)
    word_ids = get_topic_word_ids(model, topic_idx)
    return id_to_word(feature_names, word_ids)[: - n_top_words - 1:-1]


engine = create_engine('mysql+pymysql://newsfuzz:newsfuzzplease@newsfuzz.cuhvcgseshha.eu-west-2.rds.amazonaws.com:3306/newsfuzz', encoding='utf-8')
newsfuzz_db = pd.io.sql.read_sql('SELECT * FROM newsfuzz_db_test', engine)
print('data was read')

# Take only sources with certain categories
keep = ['politics', 'general']
db_pol = newsfuzz_db.ix[newsfuzz_db['source_category'].isin(keep)]
# and also only english sources
db_pol = db_pol.ix[db_pol['source_language'] == 'en']

X_train, X_test = train_test_split(db_pol, test_size=0.1, random_state=1)

# Prepare LDA
n_features = 10**8
n_topics = 40
n_top_words = 20 

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.25, min_df=20, decode_error='replace', max_features=n_features, stop_words='english', strip_accents=None, ngram_range=(1,1))
lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=10,
                                learning_method='online',
                                learning_offset=10.,
                                random_state=0,
                                verbose=0)

# Pipeline
text_lda = Pipeline([('vect', tf_vectorizer),
                     ('lda', lda),
])
t0 = time()
text_lda.fit(X_train['article_raw'])
print("done in %0.3fs." % (time() - t0))

# show results
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)

wordlist = []
topic_id = []
for news_item_dtd in text_lda.transform(X_test['article_raw']):
    idx = news_item_dtd.argsort()[-1]
    topic_id.append(idx)
    wordlist.append(get_topic_words(model=lda, feature_names=tf_feature_names, topic_idx=idx, n_top_words=5))

X_test = X_test.assign(topic_id=topic_id)
X_test = X_test.assign(topic=wordlist)
X_test.to_json('web_simple/newsfuzz.json')
