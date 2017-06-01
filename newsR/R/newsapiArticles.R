#' newsapiArticles
#'
#' @param source 	(required) - The identifer for the news source or blog you want headlines from.
#'                             Use \code{\link{newsapiSources}} endpoint to locate this or use the sources index.
#' @param key 	(required) - Your API key. Alternatively you can provide this via the X-Api-Key HTTP header.
#' @param sortBy 	(optional) - Specify which type of list you want.
#'                             The possible options are "top", "latest" and "popular".
#'                             Note: not all options are available for all sources. Default: top.
#'
#'                             "top" - Requests a list of the source's headlines sorted in the order they appear on its homepage.
#'
#'                             "latest" - Requests a list of the source's headlines sorted in chronological order, newest first.
#'
#'                             "popular" -	Requests a list of the source's current most popular or currently trending headlines.
#'
#' @keywords news, api
#'
#' @import jsonlite
#' @export
newsapiArticles <- function(
  key = Sys.getenv("NEWSAPI_KEY"),
  source,
  sortBy = ""
) {

  this_url <- paste0("https://newsapi.org/v1/articles?",
                     "source=", source,
                     "&apiKey=", key,
                     "&sortBy=", sortBy)

  cat("dowloading...\n")
  dat <- jsonlite::fromJSON(this_url)

  return(dat)

}
