from pymongo import MongoClient
import json

from bson.json_util import dumps

def connect():
        #connect to crafs db using mongo client
        client = MongoClient()
        db = client.crafs
        connect.cursor = db.productdetails.find()

def query():
        response = [] 
        for i in connect.cursor:
            print "#",i
            response.append(i)
            
        
        #print response
        return dumps(response)
        