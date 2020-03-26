const NewsAPI = require('newsapi');
const { Firestore } = require('@google-cloud/firestore');
const { Sources } = require('./entities');

const newsapi_auth = require('./newsapi_auth');
const newsapi = new NewsAPI(newsapi_auth.key);

const firestore = new Firestore();
const sources_collection = firestore.collection('sources');

function getSources(language = 'en') {
  sources = newsapi.v2.sources({
    language: language,
  })
  return sources;
}

function updateSourcesCollection() {
  getSources()
  .catch("Failed to get the sources from newsapi.org.")
  .then((response) => {

    console.log(`status: ${response.status}`);
    console.log(`number of sources: ${response.sources.length}`);

    sourceObj = new Sources(response.sources);
    sources = sourceObj.getAll();

    sources.forEach((source) => {
      const doc = sources_collection.doc(source.id);
      var setWithMerge = doc.set(source, { merge: true });
    });
  });
}
