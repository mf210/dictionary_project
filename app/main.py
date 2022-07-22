import os
from datetime import date
from fastapi import FastAPI, Query
from pymongo import MongoClient, ReturnDocument

from .xfdictionary import get_data



app = FastAPI(docs_url="/translations/docs")

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(
        f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PWD']}@mongo", 27017)
    app.dict_collection = app.mongodb_client.dictionarydb.dictionary
    app.req_collection = app.mongodb_client.dictionarydb.requests

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get('/translations')
async def get_word_definitions(word: str = Query(max_length=60)):
    # check if the word already exists in the database
    result = app.dict_collection.find_one({'word': word})
    if not result:
        # update and check the today's request limit
        today_req_count = app.req_collection.find_one_and_update(
            { 'date': date.today().isoformat()},
            { "$inc": { 'count': 1 }},
            upsert=True,
            return_document=ReturnDocument.AFTER)['count']

        result = get_data(word) if today_req_count <= 10_000 else {'msg': "Today's capacity is completed"}
        app.dict_collection.insert_one(result)

    result.pop('_id', None)
    result.pop('word', None)
    return result