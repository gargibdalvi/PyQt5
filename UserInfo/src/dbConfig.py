from google.cloud import firestore
import json

credentials_path = 'setup\\c2w-demo-7de30-firebase-adminsdk-titm6-d946e66e97.json'

with open(credentials_path) as json_file: credentials_info = json.load(json_file)

db = firestore.Client.from_service_account_info(credentials_info)