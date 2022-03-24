from flask import Flask, request, render_template, abort, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import time
import jwt
from dotenv import load_dotenv
import bson
import os
import requests
import sys
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import  rsa


# Initialize Flask
app = Flask(__name__)
CORS(app)

load_dotenv()

# MongoDB setup
app.config['MONGO_DBNAME'] = 'calendar_micro'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/calendar_micro'
mongo = PyMongo(app)

key = None

def get_public_key() :
    global key
    r = requests.get(os.environ.get("PUBLIC_KEY_URL"))
    data = r.content
    key = load_pem_public_key(data)

get_public_key()

if key is None :
    print('Unable to retireve public key')
    sys.exit()

@app.route('/')
def index():
    return "Testing..."


db_name = os.environ.get("TABLE_NAME")

# If new doctor is added
@app.route('/addDoctor', methods=['POST'])
def addDoctor():
    req = request.get_json()
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    doc_id = req['doc_id'] # 8 digit unique id
    doc = mongo.db[db_name].insert_one({'doc_id': doc_id, 'slots': []})
    return {"_id": str(doc.inserted_id)}

@app.route('/checkAvailable', methods=['GET'])
def checkAvailable():
    req = request.args.to_dict()
    hosp_id = req['hosp_id'] # 6 digit unique id
    doc_id = req['doc_id'] # 8 digit unique id
    start = req['start'] # 10 digit epoch
    dur = req['dur'] # mins
    end = int(start) + int(dur)*60
    doc = mongo.db[db_name].find_one({'doc_id': doc_id})
    for x in doc['slots']:
        if (min(int(x["end"]), int(end))-max(int(x["start"]), int(start))) > 0:
            return {"available": False}
    return {"available": True}

@app.route('/fillSlot', methods=['POST'])
def fillSlot():
    req = request.get_json()
    hosp_id = req['hosp_id'] # 6 digit unique id
    doc_id = req['doc_id'] # 8 digit unique id
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    nhid = decoded['nhid']
    start = req['start'] # 10 digit epoch
    dur = req['dur'] # mins
    end = int(start) + int(dur)*60
    _id = bson.objectid.ObjectId()
    doc = mongo.db[db_name].update_one({'doc_id': doc_id}, {'$push': {'slots': {'start': start, 'end': str(end), 'nhid': nhid, '_id': _id}}})
    return {"id": str(_id)}

@app.route('/removeSlot', methods=['DELETE'])
def removeSlot():
    req = request.args.to_dict()
    hosp_id = req['hosp_id'] # 6 digit unique id
    doc_id = req['doc_id'] # 8 digit unique id
    encoded = requests.cookies.get('PatientAuth')
    decoded = jwt.decode(encoded, key, algorithms=["RS256"])
    nhid = decoded['nhid']
    doc = mongo.db[db_name].update_one({'doc_id': doc_id}, {'$pull': {'slots': {'nhid': nhid}}})
    return {"message": "Successful"}

if __name__ == "__main__":
    app.run()
