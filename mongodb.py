from pymongo import MongoClient
from dotenv import load_dotenv
from faker import Faker
import random, os
from datetime import datetime
from urllib.parse import quote_plus

# Load environment variables from .env
load_dotenv()

# ---------------------------
# Get connection string from .env
# ---------------------------
# Safely encode special characters in password
#username = os.getenv("MONGO_USER")
#password = os.getenv("MONGO_PASS")
#cluster  = os.getenv("MONGO_CLUSTER")  # e.g. cluster0.hu19paz.mongodb.net

# Final MongoDB URI
mongo_uri = os.getenv("mongo_uri")
# ?retryWrites=true&w=majority
# ---------------------------
# Connect to MongoDB Atlas
# ---------------------------
try:
    client = MongoClient(mongo_uri, tls=True)
    client.admin.command("ping")  # test connection
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    raise SystemExit(f"❌ Cannot connect to MongoDB Atlas: {e}")

# ---------------------------
# Insert dummy data
# ---------------------------
db = client["workflowDB"]
faker = Faker()

NUM_WORKFLOWS = 2
RECORDS_EACH  = 5

for wf in range(1, NUM_WORKFLOWS + 1):
    coll = db[f"workflow_{wf}"]
    docs = [ {
        "workflow_id": wf,
        "run_id": f"run_{wf}_{i+1}",
        "user_id": f"user_{random.randint(100, 999)}",
        "lead_name": faker.name(),
        "lead_score": random.randint(50, 100),
        "lead_type": random.choice(["hot", "warm", "cold"]),
        "no_of_sms_sent": random.randint(0, 5),
        "no_of_emails_sent": random.randint(0, 5),
        "response_time": f"{random.randint(1, 10)}s",
        "status": random.choice(["success", "failed", "pending"]),
        "created_at": datetime.utcnow()
    } for i in range(RECORDS_EACH)]

    result = coll.insert_many(docs, ordered=False)
    print(f"✅ Inserted {len(result.inserted_ids)} docs into '{coll.name}'")
