const NewsAPI = require('newsapi');
const { Firestore } = require('@google-cloud/firestore');
const { Sources } = require('./entities');

const newsapi = new NewsAPI(process.env.NEWSAPIKEY);

const firestore = new Firestore();
const sources_collection = firestore.collection('sources');

function getSources(language = 'en') {
  const sources = newsapi.v2.sources({
    language,
  });
  return sources;
}

exports.updateSourcesCollection = function updateSourcesCollection() {
  getSources()
    .catch('Failed to get the sources from newsapi.org.')
    .then((response) => {
      console.log(`status: ${response.status}`);
      console.log(`number of sources: ${response.sources.length}`);

      const sourceObj = new Sources(response.sources);
      const sources = sourceObj.getAll();

      sources.forEach((source) => {
        const doc = sources_collection.doc(source.id);
        doc.set(source, { merge: true });
      });
    });
}
