#' newsapiSources
#'
#' @param
#'
#' @keywords SIMD, openSIMD, simdr
#'
#' @export
newsapiSources <- function(
  language = "en",
  category = "",
  country = "gb"
) {

  this_url <- paste0("https://newsapi.org/v1/sources?",
                     "&language=", language,
                     "&category=", category,
                     "&country=", country)

  cat("dowloading...\n")
  dat <- jsonlite::fromJSON(this_url)

  return(dat)

}
