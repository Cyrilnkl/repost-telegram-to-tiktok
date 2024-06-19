import telebot
from telebot import types
import re
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
telegram_key = os.getenv('TOKEN_TELEGRAM')

# Titok regex
tiktok_regex = re.compile(r'https?://(www\.)?tiktok\.com/.+')

# Dictionnary to follow user tasks
user_state = {}

bot = telebot.TeleBot(telegram_key)


@bot.message_handler(commands=['start', 'help'])
def choose_options(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    itembtn1 = types.InlineKeyboardButton("🚀 Donner le lien d'un tiktok", callback_data='link')
    itembtn2 = types.InlineKeyboardButton("🤔 Comment ça marche ?", callback_data='how')
    keyboard.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Faites votre choix :", reply_markup=keyboard)

def give_link(message):
    markup = types.ForceReply(selective=True)
    bot.send_message(message.chat.id, "Ok, donne moi le lien de la video tiktok :", reply_markup=markup)
    user_state[message.chat.id] = 'awaiting_link'
    
@bot.callback_query_handler(func=lambda call:True)
def answer(callback):
    if callback.message:
        if callback.data == "link":
            give_link(callback.message)
        else : 
            choose_options(callback.message)


@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'awaiting_link')
def handle_link_reply(message):
    # Here you can process the link received from the user
    tiktok_link = message.text
    bot.send_message(message.chat.id, f"J'ai bien reçu le lien Tiktok: \n\n-> {tiktok_link}")
    if tiktok_regex.match(tiktok_link):
        bot.send_message(message.chat.id, f"C'est bien un lien tiktok, je passe à l'étape suivante : téléchargement")
    else: 
        bot.send_message(message.chat.id, f"Le lien n'est pas valide, je t'invite à recommencer")
        choose_options(message)


    # Reset the state
    user_state[message.chat.id] = None

bot.infinity_polling()