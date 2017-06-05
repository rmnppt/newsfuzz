date()

### install / load packages
library(tidyverse)
library(RMySQL)
library(tidytext)
library(qdapDictionaries)
# devtools::install_github("rmnppt/newsfuzz/newsR")
library(newsR)
###

### collect source and article information from api
sources <- newsapiSources("en", "gb")
saveRDS(sources, "data/sources.rds")

articles <- sources$sources$id %>%
  lapply(function(s) newsapiArticles(source = s)) %>%
  lapply(function(s) jsonlite::flatten(as.data.frame(s))) %>%
  do.call(rbind, .)

names(articles) <- sub("articles.", "", names(articles))
###

### Clean raw html
input <- httr::GET(articles$url[1]) %>% 
  httr::content(as = "text", type = "html") %>%
  as.data.frame()
names(input) <- "text"
input$text <- as.character(input$text)
token <- unnest_tokens(input, token, text)
token <- token %>%
  filter(token %in% DICTIONARY$word)

### timestamp and filter old articles
timelast <- readRDS("data/lastdownloaded.rds")
if(exists(timelast)) {
  articles <- articles %>%
    filter(publishedAt > timelast)
}
###

### write new data to db
con <- dbConnect(RMySQL::MySQL(), 
                 host = "", 
                 port = 3306,
                 dbname = "newsfuzz",
                 user = , 
                 password = )
dbWriteTable(con, "articles", d_small, append = TRUE)
dbDisconnect(con)
###

### timestamp for next time
timenow <- print(Sys.time())
saveRDS(timenow, "data/lastdownload.rds")
###



