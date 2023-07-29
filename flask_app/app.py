from flask import Flask, request
from authentication import authenticate_user, register_user, verify
from flask import jsonify
import json
import os
from uuid import uuid4
from application.courseGen import CurriculumCreator
from db import addCourse
from application.lessonGen import contentCreator

app = Flask(__name__)


@app.route('/vibecheck', methods=['GET', 'POST'])
def checkvibe():
    return 'I am alive, guis!!!'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            return jsonify({"user":username,"login":True})
        else:
            return jsonify({"user":username,"login":False})


@app.route('/signup', methods=['GET'])
def newuser():

    username = request.form['username']
    password = request.form['password']
    email    = request.form['email']
    age     =   request.form['age']
    phone   =   request.form['phone_no']
    
    status, msg = register_user(email, username, password, age, phone)

    if status:
        return jsonify({"registration":True,"login":False, "username":username, 'msg':msg,'status':True})
    else:
        return jsonify({"registration":False,"login":False, "username":username,'msg':msg, 'status':False})





@app.route('/verify', methods=['GET'])
def verifyCreds():
    if request.method == 'POST':
        otp = request.form['otp']
        username = request.form['username']
        stts = verify(otp,username)
        return  True
        


@app.route('/genCurriculum', methods=['GET'])
def getCurriculum():

    user_input = request.form['user_input']
    username = request.form['username']

    curr = json.loads(CurriculumCreator(user_input=user_input))
    
    name = user_input
    content = curr
    id_ = str(uuid4())

    ret = addCourse(id_,name, content, username)

    return  jsonify(curr)


@app.route('/terms&conditions', methods=['GET'])
def getT&C():
    return jsonify('t&c placeholder')


D
from contentCreation import contentCreator
@app.route('/createContent', methods=['GET'])
def createContent():

    user_input = request.form['input']
    diff_level = request.form['difficulty_level']
    delivery_style = request.form['delivery_style']
    course_id = createContent(user_input, diff_level, delivery_style)
    
    return  jsonify({"course_id":course_id})



@app.route('/search', methods=['GET'])
def search():
    user_input = request.form['input']
    return  jsonify(True)


@app.route('/trending', methods=['GET'])
def trending():
    ret = {
        "course_id":[],
        "course_desc": []
            }
    return  jsonify(ret)



@app.route('/getCourse', methods=['GET'])
def trending():

    course_id = request.form['course_id']
    course_data = getCourse(course_id)

    ret = {
        "course_icon": None,
        "course_name": None,
        "course_desc":None,
        "progress":0,
        "score":0,
        "course_data":course_data
        }


    return  jsonify(ret)






if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5500)
