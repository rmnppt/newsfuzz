import sys
from getopt import getopt
import logging
from time import time
from utils.database import DocumentDB, StorageDB
from utils.models import TopicModel
from datetime import datetime, timedelta
import re
import json
import pandas as pd

logging.getLogger().setLevel(logging.INFO)

def run():
    last_month = datetime.today() - timedelta(days=30)
    db = DocumentDB()
    articles = db \
        .collection('articles') \
        .query('publishedAt', '>', last_month) \
        .toDf()

    # any articles missing content?
    articles = articles.dropna(subset=['content'])

    # remove the truncation text
    articles.content = articles.content.str.replace(
        r'.[A-z]+. [+[0-9]*\schars]', ''
    )

    # do the analysis
    analysis = TopicModel() \
        .fit_transform(articles.content) \
        .results()

    analysis['article_hashes'] = articles.hash.tolist()

    # sense check: is the analysis the right shape?
    right_shape = len(analysis['article_hashes']) == len(analysis['article_topics']) == len(analysis['sentiment_scores'])
    if (not right_shape):
        raise ValueError('Analysis results are the wrong shape')

    # write it back to the db - this time a cloud storage object
    StorageDB().write('newsfuzz-analysis', json.dumps(analysis), 'daily_analysis.json')

    articles_storage = articles.to_json(orient='records')
    # logging.info(articles_storage)
    StorageDB().write('newsfuzz-analysis', articles_storage, 'articles.json')

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
