import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from celery_helpers import lessonMaker


uri = "mongodb+srv://nikhil:sZYen1RzqzNB11zG@cluster0.g4lkqmc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi("1"))
course_db = client["cluster0"]['courses']
user_db = client["cluster0"]['users']


def getCourse(ID):
    course = course_db.find_one({"course_id": ID})
    return course 


def updateUserDatabase(username, courseID):
    
    user_db.update_one({'username':username},
                    { '$push': { "courses": courseID}})

    user_db.update_one({'username':username},
                    { '$set': { "last_course": courseID}})

    return True




def addCourse(ID,name,data, username):
    course = {
        'cid':ID,
        'course_name':name,
        'content':{},
        'summary':None,
        'complete':False
    }

    for chapter in data:
        course['content'][chapter['Chapter']] = {}
        for lesson in chapter['Lessons']:
            course['content'][chapter['Chapter']][lesson] = {}
            

    course_db.insert_one(course)
    lessonMaker.delay(ID)

    updateUserDatabase(username, ID)

    return True

def searchContent(username, user_query):
    pass

# if __name__=='__main__':
#     lessonMaker('8727bae3-6dd2-4d6f-8dcb-215f2ec182c8')