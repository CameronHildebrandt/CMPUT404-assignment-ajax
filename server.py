#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request, redirect, jsonify
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        self.userNum = 0
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        # print("space:", self.space)
        # print("oh:", self.space.get("0",dict()))

        search = self.space.get("0",dict())

        out = {}
        try:
            out = search[entity]
        except:
            pass

        # return self.space.get(entity,dict())
        return out
    
    def world(self):
        # return self.space
        return self.space.get("0",dict())

    def getWorldMultipleUsers(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    return redirect('/static/index.html', code=302)



@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    userNumber = 0
    data = request.json
    try:
        userNumber = request.json["usrNum"]
        data = request.json["data"]
    except:
        pass
        
    myWorld.update(str(userNumber), entity, data)

    # print("en:", entity)
    # print("wr:", myWorld.world())

    res = myWorld.get(entity)
    return jsonify(res), 200, {'Content-Type': 'application/json'}



@app.route("/world", methods=['POST','GET'])    
def world():
    return jsonify(myWorld.world()), 200, {'Content-Type': 'application/json'}


# I implemented the app such that multiple users have multiple colours.
# This breaks the tests. I've added the auxiliary method to preserve the apps
# ability to have multiple users and also pass the tests assuming one user.
@app.route("/worldMU", methods=['POST','GET'])    
def worldMU():
    return jsonify(myWorld.getWorldMultipleUsers()), 200, {'Content-Type': 'application/json'}



@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    res = myWorld.get(entity)
    return jsonify(res), 200, {'Content-Type': 'application/json'}



@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    myWorld.clear()
    res = {}
    return jsonify(res), 200, {'Content-Type': 'application/json'}



# my multi-user thing also violates srp and uses clear to communicate user numbers.
# the app uses its own clear method to preserve the functionality of the normal one
@app.route("/clearMU", methods=['POST','GET'])
def clearMU():
    '''Clear the world out!'''
    # blatant violation of srp: this also creates the new user - every time someone joins nuke the canvas
    myWorld.userNum += 1
    print("Welcome, user " + str(myWorld.userNum) + "!")
    myWorld.clear()
    res = {"usrNum": myWorld.userNum}
    return jsonify(res), 200, {'Content-Type': 'application/json'}



if __name__ == "__main__":
    app.run(port=8000, debug=True)
    # app.run(host="172.20.10.3", port=8000) # connect using other computers on network
