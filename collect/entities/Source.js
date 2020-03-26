class Source {
  constructor(
    id,
    name,
    description,
    url,
    category,
    language,
    country
  ) {
    this.id = id;
    this.name = name;
    this.url = url;
    this.category = category;
    this.language = language;
    this.country = country;
  }

  get() {
    return {
      id: this.id,
      name: this.name,
      url: this.url,
      category: this.category,
      language: this.language,
      country: this.country,
    }
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
          return new Source(
            s.id,
            s.name,
            s.description,
            s.url,
            s.category,
            s.language,
            s.country,
          );
        });
        this.sources = sources
      }} else {
        throw new Error(
          'Did not provide and array of items, please check input'
        );
      }
  }

  getAll() {
    return this.sources.map((s) => s.get())
  }
}

module.exports = {
  Source,
  Sources,
}
