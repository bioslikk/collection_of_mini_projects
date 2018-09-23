import os

from bson import ObjectId
from pymongo import MongoClient

from crud.utils.conversion_types import bson_to_json

MONGO_HOST = os.environ.get('MONGO_HOST', "localhost")
MONGO_PORT = os.environ.get('MONGO_PORT', "27017")
mongo = MongoClient('mongodb://{}:{}/vsr'.format(MONGO_HOST, MONGO_PORT))


def find_all_metadata():
    return bson_to_json(list(mongo.db.metadata.find()))


def find_one_metadata(metadata):
    if type(metadata) is str:
        metadata = {'_id': ObjectId(metadata)}
    return bson_to_json(mongo.db.metadata.find_one(metadata))


def delete_one_metadata(metadata):
    if type(metadata) is str:
        metadata = {'_id': ObjectId(metadata)}
    return mongo.db.metadata.delete_one(metadata).deleted_count


def insert_metadata(metadata):
    return mongo.db.metadata.insert_one(metadata).inserted_id


def update_metadata(metadata, _id):
    return mongo.db.metadata.update_one({'_id': _id}, {"$set": metadata}, upsert=True).modified_count
