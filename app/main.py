import os

from fastapi import FastAPI
from pymongo import MongoClient

mongo_user = os.environ['MONGO_USER']
mongo_pwd = os.environ['MONGO_PWD']

mongo_client = MongoClient(f'mongodb://{mongo_user}:{mongo_pwd}@mongo', 27017)


app = FastAPI()

@app.get('/')
async def test_view():
    dbs_name = mongo_client.list_database_names()
    return {
        'msg': 'Just a Test',
        'dbs_list': dbs_name
    }