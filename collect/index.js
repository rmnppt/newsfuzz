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

function getArticles(sources, from, to, page = 1, language = 'en') {
  const pagesize = 100;
  const args = {
    sources,
    from,
    to,
    language,
    pageSize: pagesize,
    page: page,
  }
  const articles = newsapi.v2.everything(args);
  // TODO - need to add paging here for the prolific sources
  return articles
    .then((response) => {
      const total_results = response.totalResults;
      const n_pages = Math.ceil(total_results / pagesize);
      if (n_pages > 1) {
        results_promises = [];
        results_promises.push(response.articles);
        for (i = 2; i <= n_pages; i++) {
          args.page = i;
          const articles = newsapi.v2.everything(args);
          results_promises.push(articles);
        }
      }

      return results_promises
      // TODO flatten the resulting nested array.
        // .then((results_pages) => {
        //
        // });
    });
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
      // TODO: concatenate the sources and make a single paginated call
      // to reduce the number of calls.
      querySnapshot.forEach((source) => {
        // doc.data() is never undefined for query doc snapshots
        console.log(source.id);

        const today = new Date();
        const yesterday = today;
        yesterday.setDate(today.getDate() - 1);

        getArticles(source.id, yesterday.toISOString())
          .then((articles) => {
            console.log(articles);
          });
      });
    });
};
