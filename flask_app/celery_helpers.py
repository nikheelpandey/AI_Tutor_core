# my_celery_app.py
from celery import Celery
from application.lessonGen import contentCreator
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#connect to db
uri = "mongodb+srv://nikhil:sZYen1RzqzNB11zG@cluster0.g4lkqmc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi("1"))
course_db = client["cluster0"]['courses']

# Create a Celery app
app = Celery('my_celery_app', broker='amqp://tutor:nIkhil@23@localhost/myvhost', backend='rpc://')


'''
db.collection.update(
     {_id:ObjectId("1")},
     { $set: { "occurrences.12": "3", "occurrences.17": "2" }})
'''


# Define a task
@app.task
def lessonMaker(course_id):
    course = course_db.find_one({"cid": course_id})

    for chapter in course['content']:
        for lesson in course['content'][chapter]:
            lesson_content = contentCreator(f'{lesson} ({chapter})')

            course_db.update_one({'cid':course['cid']},
                                 { '$set': { f"content.{chapter}.{lesson}": lesson_content}})
            print(f'upserting {lesson} in {chapter} for ID: {course_id}')
    
    course_db.update_one({'cid':course['cid']},
                        { '$set': { f"complete": True}})
    
    return True



    
