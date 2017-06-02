if(!require(RMySQL)) install.packages("RMySQL")
if(!require(tidyverse)) install.packages("tidyverse")
if(!require(devtools)) install.packages("devtools")
if(!require(newsR)) {
  devtools::install_github("rmnppt/newsfuzz/newsR")
  library(newsR)
}

sources <- newsapiSources("en", "gb")
saveRDS(sources, "data/sources.rds")

articles <- sources$sources$id %>%
  lapply(function(s) newsapiArticles(source = s)) %>%
  lapply(function(s) jsonlite::flatten(as.data.frame(s))) %>%
  do.call(rbind, .)

names(articles) <- sub("articles.", "", names(articles))

timelast <- readRDS("data/lastdownloaded.rds")
if(exists(timelast)) {
  articles <- articles %>%
    filter(publishedAt > timelast)
}

con <- dbConnect(RMySQL::MySQL(), 
                 host = "", 
                 port = 3306,
                 dbname = "newsfuzz",
                 user = , 
                 password = )
dbWriteTable(con, "articles", d_small, append = TRUE)
dbDisconnect(con)

timenow <- print(Sys.time())
saveRDS(timenow, "data/lastdownload.rds")
