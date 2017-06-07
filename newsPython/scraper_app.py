import NewsAPIScraper as nsapi
import time

# Get an instance of the newsapiorg scraper
scraper=nsapi.NewsAPIorgScraper('36cf62c1562241d4be124d5bcd5660b1')

while True:
	try:
		# fetch the news every hour!
		scraper.fetch_news()
		time.sleep(600)
	except:
            print('Error, waiting an hour')
