date()

### install / load packages
library(xml2)
library(dplyr)
library(rPython)
# devtools::install_github("rmnppt/newsfuzz/newsR")
library(newsR)
###

### collect source and article information from api
sources <- newsapiSources("en", "gb")
saveRDS(sources, "data/sources.rds")

articles <- lapply(sources$sources$id, function(s) newsapiArticles(source = s))
articles <- articles %>%
  lapply(jsonlite::flatten()) %>%
  do.call(rbind, .)
###

clean_html <- function(url) {
  input <- httr::GET(url) %>% httr::content(as = "text", type = "html")
  python.assign("input", input)
  # python.exec("from stripogram import html2text")
  # python.exec("output = html2text(input.decode('utf8'))")
  # python.get("output")
}
  
clean_html(articles[[1]]$articles$url[1])

a <- 1:4
python.assign( "a", a )
python.exec( "b = len( a )" )
python.get( "b" )
