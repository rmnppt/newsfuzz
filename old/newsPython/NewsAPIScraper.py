from newsapi.articles import Articles
from newsapi.sources import Sources
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql
from sqlalchemy import create_engine
import string
import NewsParser as newsp

class NewsAPIorgScraper:
   
	# Setup initial parameters needed for the scraping
	def __init__(self,api_key,db_user,db_pass):
		self.api_key=api_key
		self.db_user=db_user
		self.db_pass=db_pass
		self.parser=newsp.MultiNewsParser()

	def custom_parser_available(self,url):
		custom_parsers=['reuters.com','breitbart.com','mirror.co.uk','dailymail.co.uk','abc.net.au','bbc.co.uk/news','www.theguardian.com','telegraph.co.uk']
		for p in custom_parsers:
			if p in url:
				return True
		return False

	# Function to replace all non-utf8 character	
	def toUtf(self,col):
		""" takes a column of a dataframe, encodes it as utf-8 and returns it. """
		if col.dtype in ['object', 'str']:
			return col.str.encode('utf-8', 'replace')
		else:
			return col

	# takes a source, renames its keys, drops 'urlsToLogos' and 'sortBysAvailable' and returns the new dict. """
	def modDict(self,input_dict, prefix):
		droplist = ['urlsToLogos', 'sortBysAvailable']
		output = {}
		for key in input_dict:
			if key in droplist:
				pass
			else:
				output[prefix + str(key)] = input_dict[key]
		return output

	# Function to fetch the data from the API and send it to a remote mysql database
	def fetch_news(self):
		# get all sources
		a = Articles(API_KEY=self.api_key)
		s = Sources(API_KEY=self.api_key)
		all_sources = s.get()
		# prepare list to store news article dicts
		list_of_dicts = []

		if all_sources.status == 'ok':
			print(len(all_sources.sources),'sources loaded')
			for i in all_sources.sources:
				try:
				# sometimes access to the article fails
					i_articles = a.get(source=i['id'])
					source_dict = self.modDict(i, 'source_')
					for j in i_articles['articles']:
						article_dict = self.modDict(j, 'article_')
						article_dict.update(source_dict)
		                # try to add raw html from url
						try:
							# Custom parser available, extract the text
							if self.custom_parser_available(j['url']):
								txt=self.parser.parse_news(j['url'])

							# No custom parser available, use the older method
							else:
								res = requests.get(j['url'])
								res.raise_for_status()
								soup = BeautifulSoup(res.text,'lxml')
								[t.decompose() for t in soup(['script', 'iframe', 'style'])]
								txt = soup.get_text().translate({ord(c): ' ' for c in string.punctuation})
								txt = ' '.join(txt.split())

							# Add the text to the df
							article_dict['article_raw'] = txt
						except Exception as exc:
							article_dict['article_raw'] = ''
							print('there was a problem: %s' % (exc))
		                # append article
						list_of_dicts.append(article_dict)
					print('added articles from source: %s' % (i['name']))
				except:
					print('no articles loaded for: %s' % (i['name']))


		# transform dict into pandas dataframe
		df = pd.DataFrame(list_of_dicts)

		# prepare mysql connection
		engine = create_engine('mysql+pymysql://'+self.db_user+':'+self.db_pass+'@newsfuzz.cuhvcgseshha.eu-west-2.rds.amazonaws.com:3306/newsfuzz', encoding='utf-8')

		try:
		    # Add the new data to the temp database
			df.apply(self.toUtf).to_sql('newsfuzz_db_temp', engine, if_exists='replace')
			
			# Get a connection
			conn = engine.connect()
			
			# Delete duplicates from the temp DB
			query_delete_dupes='''delete from newsfuzz_db_temp WHERE article_url IN (SELECT * FROM (SELECT article_url FROM newsfuzz_db_temp GROUP BY article_url HAVING (COUNT(*) > 1)) AS a)'''
			conn.execute(query_delete_dupes)

			# Copy the non-duplicate new articles into the working db
			query_insert='''insert into newsfuzz_db_test SELECT * FROM newsfuzz_db_temp WHERE NOT EXISTS(SELECT * FROM newsfuzz_db_test WHERE (newsfuzz_db_temp.article_url=newsfuzz_db_test.article_url))'''
			conn.execute(query_insert)

			conn.close()
			print('New articles added')
			
		except Exception as exc:
		    # if no temp table exists, write df to mysql
			print('Could not read existing table. Now trying to create it. - %s' % (exc))
			df.to_sql('newsfuzz_db_temp', engine)
			
			# Get a connection
			conn = engine.connect()
			
			# Delete duplicates from the temp DB
			query_delete_dupes='''delete from newsfuzz_db_temp WHERE article_url IN (SELECT * FROM (SELECT article_url FROM newsfuzz_db_temp GROUP BY article_url HAVING (COUNT(*) > 1)) AS a)'''
			conn.execute(query_delete_dupes)

			# Copy the non-duplicate new articles into the working db
			query_insert='''insert into newsfuzz_db_test SELECT * FROM newsfuzz_db_temp WHERE NOT EXISTS(SELECT * FROM newsfuzz_db_test WHERE (newsfuzz_db_temp.article_url=newsfuzz_db_test.article_url))'''
			conn.execute(query_insert)

			conn.close()
			print('New articles added')
