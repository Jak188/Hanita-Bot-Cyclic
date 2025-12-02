# -------------------------------------------
# HANITA BOT — CYCLIC/WEBHOOK VERSION
# -------------------------------------------

import telebot
from telebot import types
import time
import json
import os
import sys
from flask import Flask, request, abort

# Gemini
from google import genai
from google.genai.errors import APIError

# -------------------------------------------
# 1. TOKEN & KEYS and CONFIG
# -------------------------------------------

# የቴሌግራም ቦት ቶኬንዎን ያስገቡ
# ** አስፈላጊ: ይህን ቶኬን በ GitHub ላይ በቀጥታ አናስቀምጥም! **
# ** እዚህ ባዶ ይሁንና በ Cyclic ላይ 'TELEGRAM_TOKEN' የሚል ሚስጥር እንሰጠዋለን **
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN', "YOUR_FALLBACK_TOKEN") 
# የ Gemini API Keyዎን ያስገቡ
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', "YOUR_FALLBACK_KEY")

# !!! የእርስዎ ትክክለኛ Admin ID !!!
ADMIN_ID = 8394878208

# !!! የቦቱ ባለቤት ልዩ ማዕረግ (Title) !!!
OWNER_TITLE = "The Red Penguins Keeper"

# የግዴታ ግሩፕ መረጃ
TELEGRAM_GROUP_ID = -1003390908033 
GROUP_LINK = "https://t.me/hackersuperiors" 

OWNER_PHOTO_PATH = "owner_photo.jpg" 

try:
    bot = telebot.TeleBot(BOT_TOKEN)
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    # በ Cyclic ላይ የ TOKEN ችግር ካለ ኮዱ እንዳይወድቅ
    print(f"❌ BOT ወይም GEMINI Client ሲነሳ ስህተት ተፈጥሯል: {e}")

GEMINI_MODEL = "gemini-2.5-flash"
# Flask App Setup
app = Flask(__name__)


# -------------------------------------------
# 2. TELEGRAM WEBHOOK ROUTE
# -------------------------------------------

@app.route('/', methods=['POST'])
def webhook():
    """ቴሌግራም መልዕክት ሲልክ ይቀበላል"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        # ትክክለኛ ጥያቄ ካልሆነ ችላ ይለዋል
        abort(403)


# -------------------------------------------
# 3. UTILITY FUNCTIONS & HANDLERS (Same as before)
# -------------------------------------------
# ... (እዚህ ጋር የገጽ ገደብ እንዳይኖር ሁሉንም functions እተዋለሁ) ...

# -------------------------------------------
# 9. UTILITY FUNCTIONS (Place the rest of your functions here)
# -------------------------------------------

# def load_json(...): ...
# def save_json(...): ...
# def track_user(...): ...
# def log_chat(...): ...
# def get_user_data(...): ...
# def send_long_message(...): ...
# def check_group_membership(...): ...
# @bot.message_handler(commands=['start']): ...
# @bot.callback_query_handler(func=lambda call: call.data == 'check_join'): ...
# ... (ሁሉም የቀሩት functions እና Handlers እዚህ ጋር ይቀጥላሉ) ...

# -------------------------------------------
# 10. RUNNING THE FLASK APP (For Cyclic)
# -------------------------------------------

# Cyclic በነባሪነት 'app' የሚባል ነገር ይፈልጋል
# ስለዚህ እዚህ ምንም bot.polling() አያስፈልግም


if __name__ == "__main__":
    # ለሙከራ ብቻ እንጂ Cyclic ራሱ ነው የሚያስኬደው
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

# (ከላይ በነጥቦች ምልክት ያደረግኩባቸው functions በሙሉ በቦት ኮድዎ ውስጥ መኖር አለባቸው።)
