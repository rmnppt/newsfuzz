const NewsAPI = require('newsapi');
const { Firestore } = require('@google-cloud/firestore');
const { Sources, Articles } = require('./entities');
require('dotenv').config();

const newsapi = new NewsAPI(process.env.NEWSAPIKEY);

const firestore = new Firestore();
const sources_collection = firestore.collection('sources');
const articles_collection = firestore.collection('articles');

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
      console.log(`Getting articles for ${sources}.`);
      console.log(`${total_results} Articles found.`);
      // Roman 31/03/20
      // Paging will not work on a free account so we need to only look at
      // the first page, with 250 requests per day, we can collect up to
      // 100 articles every 10 minutes. That's what we'll do.
      // // paging here for multi page results
      // const n_pages = Math.ceil(total_results / pageSize);
      // if (n_pages > 1) {
      //   const results_promises = [];
      //   results_promises.push(response.articles);
      //
      //   for (i = 2; i <= n_pages; i++) {
      //     args.page = i;
      //     const this_page = newsapi.v2.everything(args)
      //       .catch('Failed to get articles from newsapi.org');
      //     results_promises.push(this_page);
      //   }
      //
      //   // flatten the resulting nested array.
      //   return Promise.all(results_promises)
      //     .then((results_pages) => {
      //       let results = [];
      //       results_pages.forEach((result) => {
      //         results = results.concat(result.articles);
      //       });
      //       return results;
      //     });
      // }
      return response;
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
      const sources = [];
      querySnapshot.forEach((s) => sources.push(s.id));
      console.log(`number of sources: ${sources.length}`);

      const sources_groups = [];
      while (sources.length) {
        sources_groups.push(sources.splice(0, 10).join(','));
      }

      // We will collect every 6 or 7 minutes so use 10 to be sure,
      // see note at the top
      const today = new Date();
      const yesterday = today;
      yesterday.setHours(today.getHours() - 1);

      sources_groups.forEach((source, index) => {
        // TODO: make a subset of the sources here to reduce the number of API calls
        // NOTE: this line is for testing to reduce the number of API calls.
        if (index > 0) {
          return;
        }

        getArticles(source, yesterday.toISOString())
          .catch('Failed to get articles from newsapi.org')
          .then((response) => {
            const articlesObj = new Articles(response.articles);
            const articles = articlesObj.getAll();

            articles.forEach((article) => {
              const docRef = articles_collection.doc(article.hash);
              docRef.get().then((doc) => {
                if (doc.exists) {
                  console.log(`Found duplicate hash: ${article.hash}\nNot storing article`);
                } else {
                  console.log(`Storing article with hash: ${article.hash}`);
                  docRef.set(article, { merge: true });
                }
              });
            });
          });
      });
    });
};
