import os
import sys
from getopt import getopt
import logging
import asyncio
from analysis.run import run
from flask import Flask

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

async def async_analysis():
    run()
    return 1

@app.route('/')
def analyse():
    asyncio.run(async_analysis())
    return "analysis started"

def main(arguments):
    level = logging.INFO
    options, arguments = getopt(arguments, "l:")
    for option, argument in options:
        if option == "-l":
            level = getattr(logging, argument.upper())

    logging.basicConfig(
        level=level, format="%(asctime)s:%(levelname)s: %(message)s")
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080))
        )
    except Exception:
        logging.exception('top level catch')
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
