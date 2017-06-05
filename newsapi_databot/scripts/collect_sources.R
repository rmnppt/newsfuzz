if(!require(RMySQL)) install.packages("RMySQL")
if(!require(tidyverse)) install.packages("tidyverse")
if(!require(devtools)) install.packages("devtools")
if(!require(dplyr)) install.packages("dplyr")
if(!require(rPython)) install.packages("rPython"); library(rPython)
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

# clean_html <- function(url) {
#   input <- httr::GET(url) %>% httr::content(as = "text", type = "html")
#   python.assign("input", input)
#   python.exec("from stripogram import html2text")
#   python.exec("output = html2text(input.decode('utf8'))")
#   python.get("output")
# }

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




