import os
from pymongo import MongoClient

# 1. Connection Stringን ከ Railway Environment Variables ማንበብ
# ይህ ኮድ የሚሰራው Railway ውስጥ MONGO_URI ሲቀመጥ ነው
MONGO_URI = os.environ.get("MONGO_URI")

if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI)
        
        # ግንኙነቱን መፈተሽ
        client.admin.command('ping')
        print("✅ MongoDB Atlas connection successful!")
        
        # 2. CRUD ሙከራ (ዳታ ማስገባት)
        # Deployment መሳካቱን የሚያሳይ Document ማስገባት/ማዘመን
        test_db = client["railway_test_db"]
        test_collection = test_db["deploy_status"]
        
        test_collection.update_one(
            {"_id": "deployment_check"},
            {"$set": {"status": "Deployment successful", "timestamp": "2025-12-03"}},
            upsert=True  # Documentው ከሌለ እንዲፈጥረው ያደርጋል
        )
        
        print("✅ Status document updated/inserted successfully in MongoDB.")

    except Exception as e:
        # Railway ላይ ግንኙነት ካልተሳካ የስህተት መልእክት ይሰጣል
        print(f"❌ Deployment connection error: {e}")
        
else:
    # MONGO_URI Variable ከሌለ የሚሰጠው መልእክት
    print("❌ Configuration error: MONGO_URI environment variable not found.")
