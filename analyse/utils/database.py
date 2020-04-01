import sys
from getopt import getopt
import logging
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

logging.getLogger().setLevel(logging.INFO)

# Use a service account
cred = credentials.Certificate('../gcp_auth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
articles_ref = db.collection(u'articles')

def run():
    last_month = datetime.today() - datetime.timedelta(days=30)
    logging.info(last_month)
    query_ref = articles_ref.where(u'publishedAT', u'>', last_month)


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
