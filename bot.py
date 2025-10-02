import telebot
import json
import random
import string
import threading
from telebot import types

API_KEY = "8448172296:AAH2gsYUvkdnCcDSYC26zqeJDTwhLQuhzOw"  # your bot token
bot = telebot.TeleBot(API_KEY)
bot.delete_webhook()

bot_id = 'DEVSUDIPX'
admin_ids = [7728041999]  # add your Telegram ID here
private_group_invite = "https://t.me/+vsySMDsO6zQ3Yzk1"  # private group invite link
database_channel_id = -1003124005319  # your hidden database channel id

admin_uploads = {}
user_last_code = {}  # store last used code per user

# ----------------- Helpers -----------------

def get_data(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(file_name, data):
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

def generate_random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ----------------- Admin Upload -----------------

@bot.message_handler(commands=['admin'])
def start_admin_upload(message):
    if message.from_user.id not in admin_ids:
        return
    admin_uploads[message.from_user.id] = []
    bot.send_message(message.chat.id (http://message.chat.id/), "✅ Send up to 25 files now. After that, send /done to generate a link.")

@bot.message_handler(commands=['done'])
def finish_upload(message):
    if message.from_user.id not in admin_ids:
        return
    uploaded = admin_uploads.get(message.from_user.id, [])
    if not uploaded:
        bot.send_message(message.chat.id (http://message.chat.id/), "❌ You didn't upload any files.")
        return
    code = generate_random_id()
    all_links = get_data(f"{bot_id}-files.json")
    all_links[code] = uploaded
    save_data(f"{bot_id}-files.json", all_links)
    bot.send_message(message.chat.id (http://message.chat.id/), f"✅ Your link is ready:\nhttps://t.me/{bot.get_me().username}?start={code}")
    admin_uploads[message.from_user.id] = []

# ----------------- User Start -----------------

@bot.message_handler(commands=['start'])
def handle_start(message):
    text = message.text
    if text == "/start":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📥 Request to Join Group", url=private_group_invite))
        markup.add(types.InlineKeyboardButton("✅ I Sent Request", callback_data='join'))
        bot.send_photo(message.chat.id (http://message.chat.id/), photo='https://t.me/botpostingx/12',
                       caption="👋 Hey! You must request to join our private group before accessing files.",
                       reply_markup=markup, parse_mode='HTML')
        return

    # handle file access after start link
    user_id = message.from_user.id
    code = text.split("/start ")[-1]
    user_last_code[user_id] = code

    all_links = get_data(f"{bot_id}-files.json")
    if code in all_links:
        # show request/join panel
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📥 Request to Join Group", url=private_group_invite))
        markup.add(types.InlineKeyboardButton("✅ I Sent Request", callback_data='join'))
        bot.send_photo(message.chat.id (http://message.chat.id/), photo='https://t.me/botpostingx/12',
                       caption="👋 You must request to join our private group to unlock files.",
                       reply_markup=markup, parse_mode='HTML')

# ----------------- Media Handling -----------------

@bot.message_handler(content_types=['document', 'video', 'photo', 'audio'])
def handle_media(message):
    if message.from_user.id in admin_ids:
        uploads = admin_uploads.get(message.from_user.id, [])
        if len(uploads) >= 25:
            bot.send_message(message.chat.id (http://message.chat.id/), "⚠ You already uploaded 25 files. Send /done to get the link.")
            return
        msg = bot.copy_message(chat_id=database_channel_id,
