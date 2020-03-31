const crypto = require('crypto');

class Article {
  constructor(
    source,
    author,
    title,
    description,
    url,
    urlToImage,
    publishedAt,
    content,
  ) {
    // Roman 27/03/20
    // we will need a unique id for each article, suggest hashing the date,
    // author and title concatenated or similar.
    this.hash = null;
    this.source = source;
    this.author = author;
    this.title = title;
    this.description = description;
    this.url = url;
    this.urlToImage = urlToImage;
    this.publishedAt = publishedAt;
    this.content = content;

    this.makeHashId(`${author} ${publishedAt} ${title}`);
  }

  makeHashId(string) {
    this.hash = crypto.createHash('sha1').update(string).digest('hex');
  }

  get() {
    return {
      hash: this.hash,
      source: this.source,
      author: this.author,
      title: this.title,
      description: this.description,
      url: this.url,
      urlToImage: this.urlToImage,
      publishedAt: this.publishedAt,
      content: this.content,
    };
  }
}

class Articles {
  constructor(articles) {
    if (Array.isArray(articles)) {
      if (articles.every((article) => {
        return article instanceof Article;
      })) {
        this.articles = articles;
      } else {
        const new_articles = articles.map((a) => {
          return new Article(
            a.source,
            a.author,
            a.title,
            a.description,
            a.url,
            a.urlToImage,
            a.publishedAt,
            a.content,
          );
        });
        this.articles = new_articles;
      }
    } else {
      throw new Error(
        'Did not provide an array of items, please check input',
      );
    }
  }

  getAll() {
    return this.articles.map((a) => a.get());
  }
}

module.exports = {
  Article,
  Articles,
};
