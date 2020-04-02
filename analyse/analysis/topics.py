import sys
from getopt import getopt
import logging
from datetime import datetime, timedelta
import re
from utils.database import DocumentDB

logging.getLogger().setLevel(logging.INFO)


def cleanArticle(article):
    # removes the continuation indicator from the end of the truncated article
    clean_article = re.sub(r'.[A-z]+. [+[0-9]*\schars]', '', article)
    return clean_article


def run():
    last_month = datetime.today() - timedelta(days=30)
    articles = DocumentDB() \
        .collection('articles') \
        .query('publishedAt', '>', last_month) \
        .toDf()

    logging.info(type(articles.content[0]))
    logging.info(articles.content[0])

    ### TODO This is not working yet, possibly due to the argument type?
    # articles['clean_content'] = articles['content'].apply(cleanArticle)
    clean_articles = articles['content'].apply(cleanArticle)


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
