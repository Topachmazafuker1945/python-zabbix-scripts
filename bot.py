from telebot import TeleBot
import os, json
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent / "env_tokens/tokens.env"
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("TG_BOT_TOKEN")
# print(TOKEN)

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,)