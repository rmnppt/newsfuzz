import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
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
        self.reference = self.db.collection(u'articles')
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
