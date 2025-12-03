import os
import logging
from flask import Flask, request
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.constants import ParseMode

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["bot_users_db"]
users_collection = db["user_data"]

# Flask App
app = Flask(__name__)

# Telegram Bot Application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    users_collection.update_one(
        {"_id": user.id},
        {"$set": {
            "username": user.username,
            "first_name": user.first_name,
            "status": "Active"
        }},
        upsert=True
    )

    await update.message.reply_text(
        "👋 እንኳን ደህና መጡ!\n\nዳታዎትን በMongoDB ውስጥ አስቀምጥቻለሁ 🚀"
    )

# Register handler
application.add_handler(
    application.handler_types.MessageHandler(
        application.filters.Command("/start"),
        start
    )
)

# Webhook Receiver
@app.route("/", methods=["POST"])
def webhook():
    update_data = request.get_json(force=True)
    update = Update.de_json(update_data, application.bot)
    application.update_queue.put_nowait(update)
    return "OK"
