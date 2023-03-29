import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

if not firebase_admin._apps:
    cred = credentials.Certificate("./Connection/compilador-e8e86-firebase-adminsdk-ee64z-6686966a8d.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_Data():
    return db.collection('people').get()

def post_Data(data):
    data = data[data.find("{"):].replace("\'", "\"")
    data_js =  json.loads(data)
    db.collection('people').add(data_js)
    return "Already registered in firebase"

def get_search_Data(data):
    return  db.collection('people').document(data).get()

def delete_Data(data):
    db.collection('people').document(data).delete()
    return True


def set_Data(id,data):
    data = data[data.find("{"):].replace("\'", "\"")
    data_js =  json.loads(data)
    db.collection('people').document(id).update(data_js)
    return "The information has already been edited"