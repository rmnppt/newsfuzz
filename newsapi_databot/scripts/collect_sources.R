date()

if(!require(devtools)) install.packages("devtools")
if(!require(newsR)) {
  devtools::install_github("rmnppt/newsfuzz/newsR")
  library(newsR)
}

sources <- newsapiSources("en", "gb")
saveRDS(sources, "data/sources.rds")

articles <- lapply(sources$sources$id, function(s) newsapiArticles(source = s))
