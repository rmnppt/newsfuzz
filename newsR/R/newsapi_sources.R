#' newsapiSources
#'
#' @param language (optional) - The 2-letter ISO-639-1 code of the language you would like to get sources for.
#'                 Possible options: "en", "de", "fr." Default: empty (all sources returned)
#' @param country (optional) - The 2-letter ISO 3166-1 code of the country you would like to get sources for.
#'                Possible options: "au", "de", "gb", "in", "it", "us". Default: empty (all sources returned)
#' @param category (optional) - The category you would like to get sources for.
#'                 Possible options: business, entertainment, gaming, general, music, politics, science-and-nature, sport, technology.
#'                 Default: empty (all sources returned)
#'
#' @keywords SIMD, openSIMD, simdr
#'
#' @import jsonlite
#' @export
newsapiSources <- function(
  language = "",
  country = "",
  category = ""
) {

  this_url <- paste0("https://newsapi.org/v1/sources?",
                     "&language=", language,
                     "&category=", category,
                     "&country=", country)

  cat("dowloading...\n")
  dat <- jsonlite::fromJSON(this_url)

  return(dat)

}
