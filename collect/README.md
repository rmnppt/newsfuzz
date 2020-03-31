# Collect
### Data collection for news fuzz

This part of the project will collect data from the newsapi.org using a server-less function in nodejs and store it in google firebase. The server-less function will be deployable to google cloud functions.

I will collect english news in the first instance.

## Data Model

There is an explicit data model in /entities. This might be overkill initially but could come in useful later when we want to add more sophistication to the incoming data.


## De-duplication

To avoid duplication of articles in the firestore database I will hash the concatenated date + author + title or something similar and check that the hash does not exist before inserting the record.


## Authentication

You need to obtain a service account json key from google and place it in the root directory and also create a .env file with the parameters `NEWSAPIKEY` which is the key supplied by newsapi.org and `GOOGLE_APPLICATION_CREDENTIALS` which is the path to the google service account json file.
