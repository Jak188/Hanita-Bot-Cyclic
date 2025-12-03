import os
from flask import Flask, jsonify
from pymongo import MongoClient
import json
from bson.json_util import dumps

app = Flask(__name__)

# MONGO_URIን ከ Railway Variables ማንበብ
MONGO_URI = os.environ.get("MONGO_URI")

if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client["api_test_db"]
    test_collection = db["status_collection"]
    print("MongoDB client initialized successfully.")
else:
    print("FATAL ERROR: MONGO_URI not found!")
    # ለጊዜው ባዶ client እንፈጥራለን
    client = None

# 1. መነሻ ገጽ (Home Route)
@app.route('/')
def home():
    if client:
        try:
            # Deployment መሳካቱን የሚያሳይ document ማስገባት/ማዘመን
            test_collection.update_one(
                {"_id": "api_status_check"},
                {"$set": {"status": "API is LIVE and connected to MongoDB", "timestamp": "2025-12-03"}},
                upsert=True
            )
            
            # የተዘመነውን document ማንበብ
            status_doc = test_collection.find_one({"_id": "api_status_check"})
            
            # ObjectIdን ወደ string መቀየር (JSONify ለማድረግ)
            status_json = json.loads(dumps(status_doc))

            return jsonify(status_json)
        
        except Exception as e:
            return jsonify({"status": "ERROR", "message": f"MongoDB operation failed: {e}"}), 500
    
    return jsonify({"status": "Error", "message": "API is running but MongoDB client failed to initialize."}), 500


# 2. አፕሊኬሽኑን ማስኬድ
if __name__ == '__main__':
    # Railway ፖርትን ከ Environment Variables ያገኛል (በአብዛኛው 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
