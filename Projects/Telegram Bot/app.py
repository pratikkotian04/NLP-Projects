
import spacy
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from telebot.credentials import bot_token, URL
import requests
from flask import Flask, request
import re
spacy.load('en_core_web_sm')


global TOKEN
global eliza
TOKEN = bot_token
app = Flask(__name__)
chatbot = ChatBot('Ron Obvious', storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  database_uri='sqlite:///database.db')

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    data = request.get_json()

    chat_id = data["message"]["chat"]["id"]

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = data["message"]["text"]
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        # send the welcoming message
        sendMessage(chat_id=chat_id, text=chatbot.get_response(text), TOKEN=TOKEN)

    else:
        # clear the message we got from any non alphabets
        text = re.sub(r"\W", "_", text)
        sendMessage(
            chat_id=chat_id, text=chatbot.get_response(text), TOKEN=TOKEN)

    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    url = (
        "https://api.telegram.org/bot" + str(TOKEN) + "/setWebhook"
    )
    headers = {"Content-Type": "application/json"}
    tele_url = '{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN)
    res = requests.post(url, headers=headers, json={"url": tele_url}).json()
    if res.get("ok"):
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


def sendMessage(chat_id, text, TOKEN):
    print("Sending Text to Telegram", chat_id, text, TOKEN)
    url = (
        "https://api.telegram.org/bot" + str(TOKEN) + "/sendMessage"
    )
    headers = {"Content-Type": "application/json"}
    data = {
        "chat_id": int(chat_id),
        "text": str(text),
    }
    res = requests.post(url, headers=headers, json=data).json()
    print(res, "Response")
    if res.get("ok"):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(threaded=True)
