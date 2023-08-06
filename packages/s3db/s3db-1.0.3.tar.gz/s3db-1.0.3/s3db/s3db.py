import json
import os
import asyncio
import boto3
import bson

class s3db:
    encodings = {
        'bson': {
            'loader': bson.loads,
            'dumper': bson.dumps,
        },
        'json': {
            'loader': json.loads,
            'dumper': json.dumps,
        },
    }

    def __init__(self, config):
        configs = {
            'bucket_name': '',
            'collection_files': {},
            'encoding': 'json',
            'cache': True,
            **config,
        }

        self.cache = configs['cache']
        self.bucket_name = configs['bucket_name']
        self.encoding = configs['encoding']
        self.collection_files = {}
        self.collection_files_ref = {}
        self.updated_files = []
        self.cached_files = {}

        self.aws_credentials = {}
        if 'aws_secret_access_key' in configs and \
            configs['aws_secret_access_key'] != '' and \
            'aws_access_key_id' in configs and \
            configs['aws_access_key_id'] != '':
            self.aws_credentials = {
                'aws_secret_access_key': configs['aws_secret_access_key'],
                'aws_access_key_id': configs['aws_access_key_id'],
            }

        self.s3 = boto3.client('s3', **self.aws_credentials)
        collections = self.s3.list_objects(Bucket=self.bucket_name)['Contents']
        collection_names = [os.path.splitext(c['Key'])[0] for c in collections]
        for name in collection_names:
            if name not in configs['collection_files']:
                self.collection_files[name] = [name]

        for name in configs['collection_files']:
            self.collection_files[name] = configs['collection_files'][name]

        for filename, collections in self.collection_files.items():
            for collection_id in collections:
                self.collection_files_ref[collection_id] = filename


    def put_s3_object(self, filename, data):
        data = self.encodings[self.encoding]['dumper'](data)
        self.s3.put_object(Body=data, Bucket=self.bucket_name, Key=filename)


    def get_s3_object(self, filename):
        data = self.s3.get_object(Bucket=self.bucket_name, Key=filename)['Body']
        return self.encodings[self.encoding]['loader'](data.read())


    def get(self, id, c_id):
        try:
            filename = self.collection_files_ref[c_id]
            return self.get_collections(filename)[c_id][id]
        except Exception as e:
            raise e


    def update(self, id, c_id, **data):
        try:
            filename = self.collection_files_ref[c_id]
            collections = self.get_collections(filename)
            if id not in collections[c_id]:
                collections[c_id][id] = { 'id': id }
            items = data.items()
            updated = 0
            for k, v in items:
                entry = collections[c_id][id]
                if k not in entry or v != entry[k]:
                    entry[k] = v
                    updated += 1
            if updated:
                self.store_collections(filename, collections)
        except Exception as e:
            raise e


    def create(self, c_id, **data):
        try:
            id = data.pop('id')
            self.update(id, c_id, **data)
        except Exception as e:
            raise e


    def get_collections(self, filename):
        try:
            filename += f'.{self.encoding}'
            if self.cache:
                if filename not in self.cached_files:
                    self.cached_files[filename] = self.get_s3_object(filename)
                return self.cached_files[filename]
            return self.get_s3_object(filename)
        except Exception as e:
            raise e


    def store_collections(self, filename, data):
        filename += f'.{self.encoding}'
        try:
            asyncio.set_event_loop(asyncio.SelectorEventLoop())
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, self.put_s3_object, filename, data)
        except Exception as e:
            raise e


    def get_one(self, c_id):
        try:
            filename = self.collection_files_ref[c_id]
            documents = self.get_collections(filename)[c_id]
            return list(documents.values())[0]
        except Exception as e:
            raise e


    def get_all(self, c_id):
        try:
            filename = self.collection_files_ref[c_id]
            documents = self.get_collections(filename)[c_id]
            return list(documents.values())
        except Exception as e:
            raise e


    def delete(self, id, c_id):
        try:
            filename = self.collection_files_ref[c_id]
            collections = self.get_collections(filename)
            del collections[c_id][id]
            self.store_collections(filename, collections)
        except Exception as e:
            raise e
