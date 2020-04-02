import sys
from getopt import getopt
import logging
from datetime import datetime, timedelta
from utils.database import DocumentDB

logging.getLogger().setLevel(logging.INFO)

def run():
    last_month = datetime.today() - timedelta(days=30)
    articles = DocumentDB().collection('articles').query('publishedAt', '>', last_month).toDf()
    

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
