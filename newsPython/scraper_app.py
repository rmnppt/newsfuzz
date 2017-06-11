import NewsAPIScraper as nsapi
import time
import sys

# Gets an instance of the newsapiorg scraper
# Takes command line arguments for credentials as: api_key, db_user, db_pass
scraper=nsapi.NewsAPIorgScraper(sys.argv[0],sys.argv[1],sys.argv[2])

while True:
	try:
		# fetch the news every hour!
		scraper.fetch_news()
		time.sleep(3600)
	except:
            print('Error, waiting an hour')
