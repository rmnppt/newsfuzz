class Source {
  constructor(
    id,
    name,
    description,
    url,
    category,
    language,
    country,
  ) {
    this.id = id;
    this.name = name;
    this.url = url;
    this.category = category;
    this.language = language;
    this.country = country;
  }
}

class Sources {
  constructor(sources) {
    if (Array.isArray(sources)) {
      if (sources.every((source) => {
        return source instanceof Source
      })) {
        this.sources = sources
      } else {
        sources = sources.map((s) => {
          return new Source(s);
        });
      }} else {
        throw new Error(
          'Did not provide and array of items, please check input'
        );
      }
  }
}

module.exports = {
  Source,
  Sources,
}
