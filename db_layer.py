from pymongo import MongoClient
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

# Load .env
load_dotenv()

# Connection
username = os.getenv("MONGO_USER")
password = quote_plus(os.getenv("MONGO_PASS"))
cluster  = os.getenv("MONGO_CLUSTER")
mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client["workflowDB"]

# 1. Fetch field names (from one sample document)
def fetch_fields(workflow_id):
    coll = db[f"workflow_{workflow_id}"]
    doc = coll.find_one()
    if doc:
        return list(doc.keys())
    return []

# 2. Fetch logs (selected fields only)
def fetch_logs(workflow_id, limit=10):
    coll = db[f"workflow_{workflow_id}"]
    projection = {
        "run_id": 1,
        "user_id": 1,
        "status": 1,
        "response_time": 1,
        "created_at": 1,
        "_id": 0
    }
    return list(coll.find({}, projection).sort("created_at", -1).limit(limit))

# 3. Fetch full or filtered data
def fetch_data(workflow_id, filters=None):
    coll = db[f"workflow_{workflow_id}"]
    if filters is None:
        filters = {}
    return list(coll.find(filters))
