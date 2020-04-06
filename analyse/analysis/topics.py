import sys
from getopt import getopt
import logging
from time import time
from utils.database import DocumentDB
from datetime import datetime, timedelta
import re
import pandas as pd
import jsonpickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from afinn import Afinn

logging.getLogger().setLevel(logging.INFO)

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def print_top_words(model, feature_names, n_top_words):
    topic_descriptions = []
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        top_terms = ", ".join([feature_names[i]
                               for i in topic.argsort()[:-n_top_words - 1:-1]])
        message += top_terms
        logging.info(message)
        topic_descriptions.append(top_terms)
    logging.info('')
    return topic_descriptions


def getSentiment(text_series):
    afinn = Afinn()
    sentiment = [afinn.score(a) for a in text_series]
    return sentiment


def getTopics(ids, text_series):
    n_samples = len(text_series)
    n_features = 1000
    n_components = 20
    n_top_words = 10

    # Use tf-idf features for NMF.
    logging.info("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.8,
        min_df=2,
        max_features=n_features,
        stop_words='english'
    )

    t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(text_series)

    logging.info("done in %0.3fs." % (time() - t0))

    # non-negative matrix factorisation
    # Fit the NMF model
    logging.info("Fitting the NMF model (Frobenius norm) with tf-idf features, "
                 "n_samples=%d and n_features=%d..."
                 % (n_samples, n_features))
    t0 = time()
    nmf = NMF(
        n_components=n_components,
        random_state=1,
        alpha=.1,
        l1_ratio=.5,
        init="nndsvd"
    ).fit(tfidf)
    logging.info("done in %0.3fs." % (time() - t0))

    logging.info("Topics in NMF model (Frobenius norm):")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    topic_descriptions = print_top_words(nmf, tfidf_feature_names, n_top_words)

    W = nmf.fit_transform(tfidf)
    H = nmf.components_

    logging.info(f'Shape of document topic matrix: {W.shape}')
    logging.info(f'Shape of topic term matrix: {H.shape}')

    model_results = {
        "document_ids": ids,
        "terms": tfidf_feature_names,
        "article_topics": W,
        "topic_terms": H,
        "topic_descriptions": topic_descriptions,
    }

    return model_results


def run():
    last_month = datetime.today() - timedelta(days=30)
    db = DocumentDB()
    articles = db \
        .collection('articles') \
        .query('publishedAt', '>', last_month) \
        .toDf()

    articles = articles.dropna(subset=['content'])

    # remove the truncation text
    articles.content = articles.content.str.replace(
        r'.[A-z]+. [+[0-9]*\schars]', ''
    )

    # do the analysis
    topics = getTopics(articles.hash, articles.content)
    sentiment = getSentiment(articles.content)

    # write it back to the db
    analysis_results = db.collection('analysis')

    # TODO figure out all of the serialisation problems for writing back to the document db 

    # analysis_results.document('topics').write(json.dump(topics))
    # analysis_results.document('sentiment').write(json.dumps(sentiment))


def main(arguments):
    level = logging.INFO
    options, arguments = getopt(arguments, "l:")
    for option, argument in options:
        if option == "-l":
            level = getattr(logging, argument.upper())

    logging.basicConfig(
        level=level, format="%(asctime)s:%(levelname)s: %(message)s")
    try:
        run()
    except Exception:
        logging.exception('top level catch')
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
