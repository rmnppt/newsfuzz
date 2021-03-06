import requests
from bs4 import BeautifulSoup

class MultiNewsParser:
    
	# constructor 
	def __init__(self):
		pass

	# Helper function that gets soup for an arbitrary url
	def get_soup(self,url):
		res = requests.get(url)
		res.raise_for_status()
		return BeautifulSoup(res.text,'lxml')

	# Function that takes a url, fetches the content as soup, works out which news site is being called
	# and then extracts and returns the article text 
	def parse_news(self,url):
	    # get soup
		s= self.get_soup(url)
		# Get rid of as much inline javascript as possible!
		for script in s(["script", "style"]):
			script.extract()
		text=''
	    # determine which parser to use
		if 'dailymail.co.uk' in url:
			return s.find('div',attrs={"itemprop":"articleBody"}).text
		if 'bbc.co.uk/news' in url:
			return s.find('div',attrs={"class":"story-body__inner"}).text
		if 'abc.net.au' in url:
			return s.find('div',attrs={"class":"article section"}).text
		if 'www.theguardian.com' in url:
			return s.find('div',attrs={"itemprop":"articleBody"}).text
		if 'telegraph.co.uk' in url:
			text=s.find('div',attrs={"class":"article__content js-article"}).text.replace('\n', '')
		if 'mirror.co.uk' in url:
			text=s.find('div',attrs={"class":"article-body"}).text.replace('\n', '')
		if 'reuters.com' in url:
			text=s.find('span',attrs={"id":"article-text"}).text.replace('\n', '')   
		if 'breitbart.com' in url:
			text=s.find('div',attrs={"class":"entry-content"}).text.replace('\n', '')

		return text

	# Returns a list of article texts based on a list of urls of articles, parsing each before returning
	def get_articles(self,url_list):
		articles_text=[]
		count=0
	    # For each url in the list...
		for u in urls:
			count=count+1
			if count % 10 == 0:
				print(str(count)+' articles from a total of '+str(len(url_list)))
	        # Get the article content, parse it and add it to the list to be returned
			articles_text.append(parse_news(u))
		return articles_text
