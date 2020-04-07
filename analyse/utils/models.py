import logging
from time import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from afinn import Afinn


class TopicModel:
    def __init__(self):
        self.n_features = 1000
        self.n_components = 20
        self.n_top_words = 10

        self.tfidf_vectorizer = TfidfVectorizer(
            max_df=0.8,
            min_df=2,
            max_features=self.n_features,
            stop_words='english'
        )

        self.topic_model = NMF(
            n_components=self.n_components,
            random_state=1,
            alpha=.1,
            l1_ratio=.5,
            init="nndsvd"
        )

    def fit(self, X):
        self.n_samples = len(X)
        logging.info("Extracting tf-idf features for NMF...")
        t0 = time()
        tfidf = self.tfidf_vectorizer.fit_transform(X)
        logging.info("done in %0.3fs." % (time() - t0))

        # Fit the NMF model
        logging.info("Fitting the NMF model (Frobenius norm) with tf-idf features, "
                     "n_samples=%d and n_features=%d..."
                     % (self.n_samples, self.n_features))
        t0 = time()
        self.topic_model.fit(tfidf)
        logging.info("done in %0.3fs." % (time() - t0))

        self.X = X
        self.tfidf = tfidf
        return self

    def transform(self):
        self.article_topics = self.topic_model.fit_transform(self.tfidf)
        self.sentiment_scores = self.getSentiment(self.X)
        return self

    def fit_transform(self, X):
        self.fit(X).transform()
        return self

    def print_top_words(self, feature_names, n_top_words):
        logging.info("Topics in NMF model (Frobenius norm):")
        topic_descriptions = []
        for topic_idx, topic in enumerate(self.topic_model.components_):
            message = "Topic #%d: " % topic_idx
            top_terms = ", ".join([feature_names[i]
                                   for i in topic.argsort()[:-n_top_words - 1:-1]])
            message += top_terms
            logging.info(message)
            topic_descriptions.append(top_terms)
        logging.info('')
        return topic_descriptions

    def getSentiment(self, text_series):
        afinn = Afinn()
        sentiment = [afinn.score(a) for a in text_series]
        return sentiment

    def results(self):
        tfidf_feature_names = self.tfidf_vectorizer.get_feature_names()
        topic_descriptions = self.print_top_words(tfidf_feature_names, self.n_top_words)

        W = self.article_topics
        H = self.topic_model.components_

        logging.info(f'Shape of document topic matrix: {W.shape}')
        logging.info(f'Shape of topic term matrix: {H.shape}')

        model_results = {
            "terms": tfidf_feature_names,
            "article_topics": W.tolist(),
            "topic_terms": H.tolist(),
            "topic_descriptions": topic_descriptions,
            "sentiment_scores": self.sentiment_scores,
        }

        return model_results
