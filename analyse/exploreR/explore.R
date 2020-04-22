Sys.setenv("GCS_DEFAULT_BUCKET" = "newsfuzz-analysis", "GCS_AUTH_FILE" = "gcp_auth.json")
## GCS_AUTH_FILE set so auto-authentication
library(googleCloudStorageR)
library(jsonlite)
library(dplyr)
library(tidyr)
library(stringr)
library(ggplot2)

gcs_get_bucket()
objects = gcs_list_objects()

analysis = gcs_get_object("daily_analysis.json") %>% fromJSON()
articles = gcs_get_object("articles.json") %>% fromJSON(flatten = TRUE)

topic_names = paste0("topic_", letters[1:20])
colnames(analysis$article_topics) = topic_names

analysis_df = tibble(
  hash = analysis$article_hashes, 
  sentiment = analysis$sentiment_scores
) %>% 
  bind_cols(., as_tibble(analysis$article_topics))

results = articles %>% 
  left_join(analysis_df) %>% 
  pivot_longer(starts_with("topic"),
               names_to = "topic",
               names_prefix = "topic_",
               values_to = "topic_weight") %>% 
  group_by(source.name) %>% 
  # mutate(normalised_topic_weight = topic_weight / sum(topic_weight)) %>% 
  mutate(weighted_sentiment = sentiment * topic_weight)

results_summary = results %>% 
  group_by(source.name, topic) %>% 
  summarise(mean_sentiment = mean(weighted_sentiment),
            total_weight = sum(topic_weight),
            articles = n())

ggplot(results_summary, aes(y = mean_sentiment, x = topic)) +
  geom_point(aes(color = topic)) +
  facet_wrap(~source.name)
