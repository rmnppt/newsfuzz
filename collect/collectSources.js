const NewsAPI = require('newsapi');
const { Sources } = require('./entities');

const auth = require('./auth');
const newsapi = new NewsAPI(auth.key);

function getSources(language = 'en') {
  sources = newsapi.v2.sources({
    language: language,
  })
  return sources;
}

getSources()
  .catch("Failed to get the sources from newsapi.org.")
  .then((response) => {
    console.log(`status: ${response.status}`);
    console.log(`number of sources: ${response.sources.length}`);
    console.log(response.sources[0]);
    sourceObj = new Sources(response.sources);
  });
