import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import pandas as pd

class DocumentDB:
    '''Abstracted connection to document database where articles are stored'''

    def __init__(self):
        '''Authentication and set up'''
        # Use a service account
        self.cred = credentials.Certificate('./gcp_auth.json')
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def collection(self, collection):
        self.reference = self.db.collection(collection)
        return self

    def query(self, field, operator, value):
        self.results = self.reference.where(field, operator, value)
        return self

    def toDf(self):
        docs = self.results.stream()
        docs_list = [i.to_dict() for i in docs]
        logging.info(f'Query returned {len(docs_list)} results.')
        df = pd.DataFrame(docs_list)
        return df

    def document(self, document):
        self.reference = self.reference.document(document)
        return self

    def write(self, data):
        self.reference.set(data)
        return 1


class StorageDB():
    def __init__(self):
        self.client = storage.Client.from_service_account_json('./gcp_auth.json')

    def write(self, bucket_name, data_string, destination_blob_name):
        """Uploads a file to the bucket."""
        # bucket_name = "your-bucket-name"
        # data_string = "{json_data: 'in string format'}"
        # destination_blob_name = "storage-object-name"

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_string(data_string)

        print(
            "String stored in storage bucket: {}.".format(
                 destination_blob_name
            )
        )
