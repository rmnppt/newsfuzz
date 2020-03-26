gcloud functions deploy newsapi-collectSources \
  --runtime nodejs10 \
  --trigger-topic weeklyTrigger \
  --entry-point updateSourcesCollection \
  --verbosity debug
