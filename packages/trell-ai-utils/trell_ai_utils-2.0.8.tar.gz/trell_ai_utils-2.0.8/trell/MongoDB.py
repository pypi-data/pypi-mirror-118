import time
import logging
import pandas as pd
from pymongo import MongoClient

from trell.exceptions import MongodbConnectionError, MongodbDataFetchError, MongodbGenericError
from trell.utils import LogFormatter
LogFormatter.apply()


class MongoDB:
    
    """
    Class for handling all the mongo related update, delete and fetching
    """
    
    def __init__(self, db=None, uri=None):
        """
        initialisation method for mongo adaptor
        :param str uri: mongo uri string for establishing connection
        """

        self.db = db
        self.uri = uri
        try:
            self.client = MongoClient(self.uri)
            logging.debug("Mongo Connection set successfully ")
        except Exception as err:
            raise MongodbConnectionError(err)

        
        



    def push_data(self, data, collection, db=None):
        """
        Function for inserting data into db
        :param str db : database name
        :param str collection : collection name
        :param list/pd.DataFrame : data to be inserted and it should be either dataframe or list of dictionaries
        """
        
        if db==None:
            db = self.db
        else:
            db = db

        pushed = False
        while not pushed:
            try:
                client_db = self.client[db]
                collection = client_db[collection]
                if isinstance(data, pd.DataFrame):
                    data_dict = data.to_dict("records")
                collection.insert_many(data_dict)
                pushed = True
                logging.debug("data pushed successfully ")
            except Exception as e:
                logging.error("Got Exception.. {}\nReconnecting.. Retrying..".format(str(e)))
                time.sleep(2)
                self.client = MongoClient(self.uri)

    def pull_data(self, list_dict, collection, db=None):
        
        if db==None:
            db = self.db
        else:
            db = db

        pulled = False
        while not pulled:
            try:
                client_db = self.client[db]
                collection = client_db[collection]
                data = []
                if list_dict == [0]:
                    for j in collection.find():
                        data.append(j)
                else:
                    for i in list_dict:
                        for j in collection.find(i):
                            data.append(j)
                pulled = True
                logging.debug("data pulled successfully")
                return pd.DataFrame(data=data)
            except Exception as e:
                logging.error("Got Exception.. {}\nReconnecting.. Retrying..".format(str(e)))
                time.sleep(2)
                self.client = MongoClient(self.uri)
                
    def update_value(self, id_dict, set_dict, collection, db=None, upsert=None):
        
        if db==None:
            db = self.db
        else:
            db = db

        updated = False
        while not updated:
            try:
                client_db = self.client[db]
                client_db[collection].update_many(id_dict, set_dict, upsert=upsert)
                logging.debug("data updated successfully")
                updated = True
            except Exception as e:
                logging.error("Got Exception.. {}\nReconnecting.. Retrying..".format(str(e)))
                time.sleep(1)
                self.client = MongoClient(self.uri)
                
    def upsert_json(self, output_json, upsert_keys, collection, db=None):
        
        if db==None:
            db = self.db
        else:
            db = db
            
        inserted = False
        while not inserted:
            try:
                client_db = self.client[db]
                for record in output_json:
                    filter_query = dict()
                    for filter_key in upsert_keys:
                        filter_query[filter_key] = record[filter_key]
                    client_db[collection].replace_one(filter_query, record, upsert=True)
                logging.debug("data inserted successfully")
                inserted = True
            except Exception as e:
                logging.error("Got Exception.. {}\nReconnecting.. Retrying..".format(str(e)))
                time.sleep(1)
                self.client = MongoClient(self.uri)


    def delete_data(self,collection, db=None, overall=False, condition_dict=None):
        
        if db==None:
            db = self.db
        else:
            db = db

        deleted = False
        while not deleted:
            try:
                client_db = self.client[db]
                if overall:
                    client_db[collection].remove({})
                    print('Overall data deleted.')
                else:
                    client_db[collection].delete_many(condition_dict)
                logging.debug("data deleted successfully")
                deleted = True
            except Exception as e:
                logging.error("Got Exception.. {}\nReconnecting.. Retrying..".format(str(e)))
                time.sleep(1)
                self.client = MongoClient(self.uri)
                
    def fetch_data(self, collection, db=None, query={}, only_include_keys=[]):
        """
        function to fetch data from the given database and collection on given query
        :param db: db_name in mongo
        :param collection: collection name in mongo for database db
        :param query: execution query statement; default is {} which means fetch all without any filters
        :param only_include_keys: list of keys to be included while fetching rows
        :return:
        """
        if db==None:
            db = self.db
        else:
            db = db
            
        fetched = False
        while not fetched:
            try:
                results = list()
                client_db = self.client[db]
                all_collection_names = client_db.collection_names()
                # collection exists
                projections = dict()
                for key in only_include_keys:
                    projections[key] = 1
                projections["_id"] = 0
                if collection in all_collection_names:
                    cursor = client_db[collection]
                    for row in cursor.find(query, projections):
                        results.append(row)
                logging.debug("data fetched successfully")        
                fetched = True
                return results
            except Exception as e:
                logging.error("Got Exception.. {}\nReconnecting.. Retrying..".format(str(e)))
                time.sleep(1)
                self.client = MongoClient(self.uri)

    def fetch_data_sorted(self, collection, db=None, pipeline=[]):
        """
        function to fetch data from the given database and collection on given query
        :param db: db_name in mongo
        :param collection: collection name in mongo for database db
        :param pipeline: pipeline required to aggregate
        :return:
        """
        
        if db==None:
            db = self.db
        else:
            db = db
            
        fetched = False
        while not fetched:
            try:
                results = list()
                client_db = self.client[db]
                all_collection_names = client_db.collection_names()
                # collection exists
                client_collection = client_db[collection]
                results = client_collection.aggregate(pipeline=pipeline)
                fetched = True
                logging.debug("data fetched successfully")
                return results
            except Exception as e:
                logging.error("Got Exception.. {}\nReconnecting.. Retrying..".format(str(e)))
                time.sleep(1)
                self.client = MongoClient(self.uri)