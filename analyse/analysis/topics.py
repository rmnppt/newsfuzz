import sys
from getopt import getopt
import logging
from time import time
from utils.database import DocumentDB
from datetime import datetime, timedelta
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

logging.getLogger().setLevel(logging.INFO)


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        logging.info(message)
    logging.info('')

def run():
    last_month = datetime.today() - timedelta(days=30)
    articles = DocumentDB() \
        .collection('articles') \
        .query('publishedAt', '>', last_month) \
        .toDf()

    articles = articles.dropna(subset=['content'])

    # remove the truncation text
    articles.content = articles.content.str.replace(r'.[A-z]+. [+[0-9]*\schars]', '')

    n_samples = len(articles.content)
    n_features = 300
    n_components = 20
    n_top_words = 20

    # Use tf-idf features for NMF.
    logging.info("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.8,
        min_df=2,
        max_features=n_features,
        stop_words='english'
    )

    t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(articles.content)
    logging.info("done in %0.3fs." % (time() - t0))

    # non-negative matrix factorisation
    # Fit the NMF model
    logging.info("Fitting the NMF model (Frobenius norm) with tf-idf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    t0 = time()
    nmf = NMF(n_components=n_components, random_state=1,
              alpha=.1, l1_ratio=.5).fit(tfidf)
    logging.info("done in %0.3fs." % (time() - t0))

    logging.info("Topics in NMF model (Frobenius norm):")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, n_top_words)

    # Fit the NMF model
    logging.info("Fitting the NMF model (generalized Kullback-Leibler divergence) with "
        "tf-idf features, n_samples=%d and n_features=%d..."
        % (n_samples, n_features))
    t0 = time()
    nmf = NMF(n_components=n_components, random_state=1,
              beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
              l1_ratio=.5).fit(tfidf)
    logging.info("done in %0.3fs." % (time() - t0))

    logging.info("Topics in NMF model (generalized Kullback-Leibler divergence):")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, n_top_words)


def main(arguments):
    level = logging.INFO
    options, arguments = getopt(arguments, "l:")
    for option, argument in options:
        if option == "-l":
            level = getattr(logging, argument.upper())

    logging.basicConfig(level=level, format="%(asctime)s:%(levelname)s: %(message)s")
    try:
        run()
    except Exception:
        logging.exception('top level catch')
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
