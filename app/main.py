import os
from datetime import date
from fastapi import FastAPI, Query
from pymongo import MongoClient, ReturnDocument

from .xfdictionary import get_data



app = FastAPI(docs_url="/xfdictionary/docs")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(
        f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PWD']}@mongo", 27017)
    app.dict_collection = app.mongodb_client.dictionarydb.dictionary
    app.req_collection = app.mongodb_client.dictionarydb.requests

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get('/xfdictionary')
async def get_phrase_definitions(phrase: str = Query(max_length=60)):
    # check if the phrase already exists in the database
    result = app.dict_collection.find_one({'phrase': phrase})
    if not result:
        # update and check the today's request limit
        today_req_count = app.req_collection.find_one_and_update(
            { 'date': date.today().isoformat()},
            { "$inc": { 'count': 1 }},
            upsert=True,
            return_document=ReturnDocument.AFTER)['count']

        result = get_data(phrase) if today_req_count <= 10_000 else {'msg': "Today's capacity is completed"}
        app.dict_collection.insert_one(result)

    result.pop('_id', None)
    result.pop('phrase', None)
    return result