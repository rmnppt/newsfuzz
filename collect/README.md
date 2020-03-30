# Collect
### Data collection for news fuzz

This part of the project will collect data from the newsapi.org using a server-less function in nodejs and store it in google firebase. The server-less function will be deployable to google cloud functions.

I will collect english news in the first instance.

There is an explicit data model in /entities. This might be overkill initially but could come in useful later when we want to add more sophistication to the incoming data.

To avoid duplication of articles in the firestore database I will hash the concatenated date + author + title or something similar and check that the hash does not exist before inserting the record.
