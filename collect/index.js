const NewsAPI = require('newsapi');
const { Firestore } = require('@google-cloud/firestore');
const { Sources } = require('./entities');
require('dotenv').config();

const newsapi = new NewsAPI(process.env.NEWSAPIKEY);

const firestore = new Firestore();
const sources_collection = firestore.collection('sources');

function getSources(language = 'en') {
  const sources = newsapi.v2.sources({
    language,
  });
  return sources;
}

function getArticles(sources, from, to, language = 'en') {
  const articles = newsapi.v2.everything({
    sources,
    from,
    to,
    language,
    pageSize: 100,
    page: 1,
  });
  // TODO - need to add paging here for the prolific sources
  return articles;
}

exports.updateSourcesCollection = function updateSourcesCollection() {
  getSources()
    .catch('Failed to get the sources from newsapi.org.')
    .then((response) => {
      console.log(`response status: ${response.status}`);
      console.log(`number of sources: ${response.sources.length}`);

      // Roman 27/03/20
      // Im putting them into an explicit data model, #
      // will possibly bundle some QC in there.
      const sourceObj = new Sources(response.sources);
      const sources = sourceObj.getAll();

      sources.forEach((source) => {
        const doc = sources_collection.doc(source.id);
        doc.set(source, { merge: true });
      });
    });
};

exports.updateArticlesCollection = function updateArticlesCollection() {
  sources_collection.get()
    .then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        // doc.data() is never undefined for query doc snapshots
        console.log(doc.id, ' => ', doc.data());
      });
    });
};
