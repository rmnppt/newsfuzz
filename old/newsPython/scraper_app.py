import NewsAPIScraper as nsapi
import time
import sys

# Gets an instance of the newsapiorg scraper
# Takes command line arguments for credentials as: api_key, db_user, db_pass

args=[]
with open('config.txt', 'r') as file:
	args=file.read().split(',')
scraper=nsapi.NewsAPIorgScraper(args[0],args[1],args[2])
while True:
	try:
		# fetch the news every hour!
		scraper.fetch_news()
	except:
            print('Error, waiting an hour')
	time.sleep(3600)
