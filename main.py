import os
import telegram
from pymongo import MongoClient
import logging
from flask import Flask, request

# Log settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment Variablesን ከ Railway ማንበብ
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

# MongoDB ግንኙነት
if MONGO_URI:
    try:
        client = MongoClient(MONGO_URI)
        db = client["bot_users_db"]
        users_collection = db["user_data"]
        logger.info("MongoDB client initialized for Bot successfully.")
    except Exception as e:
        logger.error(f"MongoDB connection error for Bot: {e}")
        client = None
else:
    logger.error("BOT_TOKEN or MONGO_URI environment variable not found!")
    client = None

# Telegram Bot Client
if BOT_TOKEN:
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        logger.info("Telegram Bot client initialized.")
    except Exception as e:
        logger.error(f"Telegram Bot initialization error: {e}")
        bot = None
else:
    bot = None

# የ Flask App መፍጠር
app = Flask(__name__)


# የ Telegram Webhook Handler
def handle_updates(update):
    # /start commandን በትክክል መፈተሽ
    if update.message and update.message.text and update.message.text.lower().strip() == "/start":
        
        # 1. ዳታቤዝ ውስጥ ማስገባት
        user_id = update.message.from_user.id
        username = update.message.from_user.username or "N/A"
        first_name = update.message.from_user.first_name or "N/A"
        
        if client:
            users_collection.update_one(
                {"_id": user_id},
                {"$set": {
                    "username": username,
                    "first_name": first_name,
                    "last_active": update.message.date,
                    "status": "Active"
                }},
                upsert=True
            )
            response_text = "እንኳን ደህና መጡ! 🚀\nየእርስዎን ዳታ በዳታቤዝ ውስጥ አስመዝግቤያለሁ።"
        else:
            response_text = "እንኳን ደህና መጡ! ⚠️\nዳታቤዝ ግንኙነት አልተሳካም።"
            
        # 2. ለተጠቃሚው መልስ መላክ
        try:
            bot.send_message(chat_id=update.message.chat_id, text=response_text)
            logger.info(f"Sent /start message to user {user_id}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")


# Webhookን ለመቀበል የሚደረግ Flask Route
# ይህ አሁን የ Tokenን ክፍል ተጠቅሞ ጥያቄውን ይቀበላል
@app.route('/<token>', methods=['GET', 'POST']) 
@app.route('/webhook', methods=['POST'])
def webhook_handler(token=None):
    if bot and request.method == "POST":
        # ከ Telegram የመጣውን JSON ዳታ መቀበል
        data = request.get_json(force=True)
        
        # JSONን ወደ Telegram Update object መቀየር
        try:
            update = telegram.Update.de_json(data, bot)
            handle_updates(update)
        except Exception as e:
            logger.error(f"Error processing webhook update: {e}")
    return 'ok'
