from newsapi.articles import Articles
from newsapi.sources import Sources
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql
from sqlalchemy import create_engine
import string

# prepare newsAPI connection
a = Articles(API_KEY="36cf62c1562241d4be124d5bcd5660b1")
s = Sources(API_KEY="36cf62c1562241d4be124d5bcd5660b1")

# get all sources
all_sources = s.get()

# prepare list to store news article dicts
list_of_dicts = []

def toUtf(col):
    """ takes a column of a dataframe, encodes it as utf-8 and returns it. """
    if col.dtype in ['object', 'str']:
        return col.str.encode('utf-8', 'replace')
    else:
        return col


def modDict(input_dict, prefix):
    """ takes a source, renames its keys, drops 'urlsToLogos' and 'sortBysAvailable' and returns the new dict. """
    droplist = ['urlsToLogos', 'sortBysAvailable']
    output = {}
    for key in input_dict:
        if key in droplist:
            pass
        else:
            output[prefix + str(key)] = input_dict[key]
    return output


if all_sources.status == 'ok':
    print(len(all_sources.sources),'sources loaded')
    for i in all_sources.sources:
        try:
            # sometimes access to the article fails
            i_articles = a.get(source=i['id'])
            source_dict = modDict(i, 'source_')
            for j in i_articles['articles']:
                article_dict = modDict(j, 'article_')
                article_dict.update(source_dict)
                # try to add raw html from url
                try:
                    res = requests.get(j['url'])
                    res.raise_for_status()
                    soup = BeautifulSoup(res.text)
                    [s.decompose() for s in soup(['script', 'iframe', 'style'])]
                    txt = soup.get_text().translate({ord(c): ' ' for c in string.punctuation})
                    txt = ' '.join(txt.split())
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
engine = create_engine('mysql+pymysql://newsfuzz:newsfuzzplease@newsfuzz.cuhvcgseshha.eu-west-2.rds.amazonaws.com:3306/newsfuzz', encoding='utf-8')

# try to read existing table and then merge or write new
try:
    # read existing table
    newsfuzz_db = pd.io.sql.read_sql('SELECT * FROM newsfuzz_db', engine, index_col='index')
    # concat, drop duplicates and write to mysql
    (pd.concat([newsfuzz_db, df])
    .drop_duplicates(subset=['article_url', 'article_title', 'article_publishedAt'])
    .apply(toUtf)
    .to_sql('newsfuzz_db', engine, if_exists='replace'))
    print('Existing table updated.')
except Exception as exc:
    # if no table exists, write df to mysql
    print('Could not read existing table. Now trying to create it. - %s' % (exc))
    df.to_sql('newsfuzz_db', engine)



