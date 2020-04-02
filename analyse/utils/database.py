import sys
from getopt import getopt
import logging
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

logging.getLogger().setLevel(logging.INFO)


def run():
    # Use a service account
    cred = credentials.Certificate('./gcp_auth.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    articles_ref = db.collection(u'articles')

    # analyse articles no more than one month old
    last_month = datetime.today() - timedelta(days=30)
    docs = articles_ref.where('publishedAt', '>', last_month).stream()

    articles_list = [i.to_dict() for i in docs]
    articles = pd.DataFrame(articles_list)
    logging.info(list(articles))

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
