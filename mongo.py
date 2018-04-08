from pymongo import MongoClient

client = MongoClient("mongodb://anyone:anyone@ds113958.mlab.com:13958/project_panorama")
db = client['project_panorama']
facultyCollection = db["Faculty"]
studentCollection = db["Student"]
projectCollection = db["Project"]