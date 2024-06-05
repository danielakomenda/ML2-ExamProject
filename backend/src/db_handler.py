import os
import datetime

import dotenv
import pymongo
from bson import ObjectId



def serialize_obj(obj):
    """Recursively convert ObjectId to str and prepare for JSON serialization."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, list):
        return [serialize_obj(item) for item in obj]
    if isinstance(obj, dict):
        return {key: serialize_obj(value) for key, value in obj.items()}
    return obj


def connect_to_db(collection):
    dotenv.load_dotenv()
    mongodb_uri = os.getenv("MONGODB_URI")
    DBclient = pymongo.MongoClient(mongodb_uri)
    db = DBclient["ML2-Abschlussprojekt"]
    return db[collection]

#################################### BASEDATA ####################################

def insert_base(data):
    collection = connect_to_db("Base_Data")
    result = collection.find_one({
        "firstname": data["firstname"],
        "lastname": data["lastname"],
        "birthday": data["birthday"],
    })
    if result is None:
        entry = collection.insert_one(data)
        result = dict(data)
        result["_id"] = entry.inserted_id
    return serialize_obj(result)

################################# SEMESTERDATA #################################

def get_all_pupils():
    results = []
    collection = connect_to_db("Base_Data")
    cursor = collection.find({})
    for document in cursor:
          results.append(document)
    return serialize_obj(results)


def get_pupil(student_id):
    collection = connect_to_db("Base_Data")
    results = collection.find_one({"_id":ObjectId(student_id)})
    return serialize_obj(results)


def insert_semester(data):
    collection = connect_to_db("Semester_Data")
    data["student_id"]=ObjectId(data["student_id"])
    filter = {
        "student_id":data["student_id"],
        "semester_name":data["semester_name"],
    }
    entry = {"$set":data}
    collection.update_one(filter, entry, upsert=True)
    data = dict(data)
    return serialize_obj(data)

################################# ASSESSMENT #################################

def get_all_semesters(student_id):
    results = []
    collection = connect_to_db("Semester_Data")
    cursor = collection.find({
        "student_id":ObjectId(student_id),
    })
    for document in cursor:
          results.append(document)
    return serialize_obj(results)


def get_semester(semester_id):
    collection = connect_to_db("Semester_Data")
    results = collection.find_one({"_id":ObjectId(semester_id),})    
    return serialize_obj(results)


def insert_assessement(data):
    print("Checkpoint: ", data)
    
    collection = connect_to_db("Assessment_Data")
    data["student_id"]=ObjectId(data["student_id"])
    data["semester_id"]=ObjectId(data["semester_id"])
    filter = {
        "student_id": data["student_id"],
        "semester_id": data["semester_id"],
        "author": data["author"],
    }
    data = dict(data)
    data["date"] = datetime.datetime.today()
    entry = {"$set":data}
    collection.update_one(filter, entry, upsert=True)
    return serialize_obj(data)

################################# COMBINE #################################
    
def get_all_assessments(semester_id):
    results = []
    collection = connect_to_db("Assessment_Data")
    cursor = collection.find({
        "semester_id":ObjectId(semester_id),
    })
    for document in cursor:
          results.append(document)
    return serialize_obj(results)


def insert_final_assessment(semester_id, data):
    collection = connect_to_db("Semester_Data")
    filter = {
        "_id":ObjectId(semester_id),
    }
    entry = {"$set": {"final_assessment": data}}
    collection.update_one(filter, entry, upsert=True)
    return serialize_obj(data)
    
################################# CREATE-TEXT #################################

def get_semesters_with_final_assessments(student_id):
    results = []
    collection = connect_to_db("Semester_Data")
    cursor = collection.find({
        "student_id":ObjectId(student_id),
    })
    for document in cursor:
        if document["final_assessment"]:
            results.append(document)
    return serialize_obj(results)


def insert_final_text(semester_id, data):
    collection = connect_to_db("Semester_Data")    
    filter = {
        "_id":ObjectId(semester_id),
    }
    entry = {"$set": {"final_text": data}}
    collection.update_one(filter, entry, upsert=True)
    return serialize_obj(data)