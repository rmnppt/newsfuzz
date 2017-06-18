class NewsParser:
    
	# constructor 
	def __init__(self):
		pass

	# Helper function that gets soup for an arbitrary url
	def get_soup(url):
		res = requests.get(url)
		res.raise_for_status()
		return BeautifulSoup(res.text,'lxml')

	# Function that takes a url, fetches the content as soup, works out which news site is being called
	# and then extracts and returns the article text 
	def parse_news(url):
	    # get soup
		s= get_soup(url)

	    # determine which parser to use
		if 'dailymail.co.uk' in url:
			return s.find('div',attrs={"itemprop":"articleBody"}).text
		if 'bbc.co.uk/news' in url:
			return s.find('div',attrs={"class":"story-body__inner"}).text
		if 'abc.net.au' in url:
			return s.find('div',attrs={"class":"article section"}).text
		if 'www.theguardian.com' in url:
			return s.find('div',attrs={"itemprop":"articleBody"}).text
