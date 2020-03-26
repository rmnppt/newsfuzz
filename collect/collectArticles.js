const NewsAPI = require('newsapi');

const auth = require('./auth');
const newsapi = new NewsAPI(auth.key);

function getSources(language = 'en') {
  sources = newsapi.v2.sources({
    language: language,
  })
  return sources;
}

function getArticles(sources, from, to, language = 'en') {
  articles = newsapi.v2.everything({
    sources: sources,
    from: from,
    to: to,
    language: language,
    pageSize: 100,
    page: 1
  })
  // TODO - need to add paging here for the prolific sources
  return articles;
}

getSources()
  .then((response) => {
    console.log(`status: ${response.status}`);
    console.log(`number of sources: ${response.sources.length}`)

    source_names = response.sources.map((r) => r.id);

    today = new Date();
    console.log(today);
    yesterday = today
    yesterday.setDate(today.getDate() - 1);
    console.log(yesterday);

    collections = source_names.slice(0, 1).map((source) => {
      getArticles(source, from = yesterday, to = today)
        .then((response) => {
          console.log(`status: ${response.status}`);
          console.log(`number of articles: ${response.totalResults}`);
          console.log(response.articles[0]);
        });
    })
  });
