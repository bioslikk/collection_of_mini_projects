from bson.json_util import loads, dumps
import json


def bson_to_json(_bson):
    return json.loads(dumps(_bson))


def json_to_bson(_json):
    return loads(_json)


