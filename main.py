import json
import os
from flask import Flask, request
import telegram

TOKEN = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)
DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def is_duplicate(link):
    with open(DATA_FILE, "r") as f:
        links = json.load(f)
    return link in links

def save_link(link):
    with open(DATA_FILE, "r") as f:
        links = json.load(f)
    links.append(link)
    with open(DATA_FILE, "w") as f:
        json.dump(links, f)

@app.route(f"/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message and update.message.text:
        text = update.message.text
        words = text.split()
        for word in words:
            if word.startswith("http"):
                if is_duplicate(word):
                    try:
                        bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                        bot.send_message(chat_id=update.message.chat.id, text="⚠️ Это дубль, удаляю.")
                    except Exception as e:
                        print("Ошибка удаления:", e)
                else:
                    save_link(word)
    return "ok"
