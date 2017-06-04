from newsapi.articles import Articles
from newsapi.sources import Sources

a = Articles(API_KEY="36cf62c1562241d4be124d5bcd5660b1")
s = Sources(API_KEY="36cf62c1562241d4be124d5bcd5660b1")

all_sources = s.get()

if all_sources.status == 'ok':
    print(len(all_sources.sources),'sources loaded')
    for i in all_sources.sources:
        print(i)
        print('trying to load source:', i['name'])
        try:
            i_articles = a.get(source=i['id'])
            print(i_articles.articles)
        except:
            print('no articles loaded for', i['name'])



