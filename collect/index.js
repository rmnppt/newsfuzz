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
  const pageSize = 100;
  const args = {
    sources,
    from,
    to,
    language,
    pageSize,
    page,
  };
  const articles = newsapi.v2.everything(args);
  return articles
    .then((response) => {
      const total_results = response.totalResults;
      console.log(`${total_results} Articles found.`);
      // paging here for multi page results
      const n_pages = Math.ceil(total_results / pageSize);
      if (n_pages > 1) {
        const results_promises = [];
        results_promises.push(response.articles);

        for (i = 2; i <= n_pages; i++) {
          args.page = i;
          const this_page = newsapi.v2.everything(args)
            .catch('Failed to get articles from newsapi.org');
          results_promises.push(this_page);
        }

        // flatten the resulting nested array.
        return Promise.all(results_promises)
          .then((results_pages) => {
            let results = [];
            results_pages.forEach((result) => {
              results = results.concat(result.articles);
            });
            return results;
          });
      }
      return response.articles;
    });
}

exports.updateSourcesCollection = function updateSourcesCollection() {
  getSources()
    .catch('Failed to get sources from newsapi.org.')
    .then((response) => {
      console.log(`response status: ${response.status}`);
      console.log(`number of sources: ${response.sources.length}`);

      // Roman 27/03/20
      // Im putting them into an explicit data model,
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
      querySnapshot.forEach((source, index) => {
        // TODO: make a subset of the sources here to reduce the number of API calls
        // NOTE: this line is for testing to reduce the number of API calls.
        if (index > 1) {
          return;
        }

        // doc.data() is never undefined for query doc snapshots
        console.log(source.id);

        const today = new Date();
        const yesterday = today;
        yesterday.setDate(today.getDate() - 1);

        getArticles(source.id, yesterday.toISOString())
          .catch('Failed to get articles from newsapi.org')
          .then((articles) => {
            console.log(articles.length);
          });
      });
    });
};
