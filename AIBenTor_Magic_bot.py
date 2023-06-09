import telebot
import openai
from mtgsdk import Card
from config import BOT_TOKEN, ALLOWED_CHATS, OPENAI_API_KEY
from telebot import custom_filters


# Bot
bot = telebot.TeleBot(BOT_TOKEN)


# Save the OpenAI API key
openai.api_key = OPENAI_API_KEY


# Admin commands
# All admin actions must have the 'is_admin' filter
@bot.message_handler(chat_id=ALLOWED_CHATS, is_admin=True, commands=['admingetchatid'])
def admin_get_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, chat_id)


# Start, hello
@bot.message_handler(chat_id=ALLOWED_CHATS, commands=['start', 'hello'])
def send_start(message):
    reply_message = "Hola, soy AIBenTor Magic Bot!!!\n\nDe momento solo puedes usar los comando /start, /hello, /getCardRules y /getCardBestStrategy"
    bot.reply_to(message, reply_message)


# Find a card by foreign name
""" @bot.message_handler(chat_id=ALLOWED_CHATS, commands=['findByForeignName'])
def find_by_foreign_name(message):
    card_name = message.text[19:]
    if (card_name.replace(' ', '') == ''):
        bot.reply_to(
            message,
            "Ups, necesito que escribas el nombre de una carta"
        )
    else:
        try:
            card_info = Card.where(name=card_name).where(
                language='spanish').all()
            # Check if card exists
            if len(card_info) > 0:
                # Get the Spanish card
                foreign_names = card_info[0].foreign_names
                card_info = dict(list(filter(
                    lambda card: card['language'] == 'Spanish',
                    foreign_names))[0])
                card_info = "**Descripción:**\n\n" + card_info['text']
            else:
                card_info = 'Ups, parece que la carta no existe'

            # return card information
            bot.reply_to(message, card_info)
        except Exception as err:
            bot.reply_to(message, "Ups, ha ocurrido un error :(")
"""


# Get the card rules
@bot.message_handler(chat_id=ALLOWED_CHATS, commands=['getCardRules'])
def get_card_rules(message):
    card_name = message.text[14:]
    if (card_name.replace(' ', '') == ''):
        bot.reply_to(
            message,
            "Ups, necesito que escribas el nombre de una carta"
        )
    else:
        try:
            promp_message = "A partir del juego de cartas Magic The Gathering, explica como jugar la carta de nombre \"" + card_name + "\""
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": promp_message}
                ]
            )
            response_message = response.choices[0].message.content
            bot.reply_to(message, response_message)
        except Exception as err:
            bot.reply_to(message, "Ups, ha ocurrido un error :(")


# Get the card rules
@bot.message_handler(chat_id=ALLOWED_CHATS, commands=['getCardBestStrategy'])
def get_card_best_strategy(message):
    card_name = message.text[21:]
    if (card_name.replace(' ', '') == ''):
        bot.reply_to(
            message,
            "Ups, necesito que escribas el nombre de una carta"
        )
    else:
        try:
            promp_message = "A partir del juego de cartas Magic The Gathering, explica la mejor estrategia ganadora para jugar la carta de nombre \"" + card_name + "\""
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": promp_message}
                ]
            )
            response_message = response.choices[0].message.content
            bot.reply_to(message, response_message)
        except Exception as err:
            bot.reply_to(message, "Ups, ha ocurrido un error :(")


# Custom filters
# Check if user is an admin or cretor of a group
class IsAdmin(custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message: telebot.types.Message):
        status = bot.get_chat_member(
            message.chat.id, message.from_user.id).status
        return status in ['administrator', 'creator']


# Register chat filters
bot.add_custom_filter(custom_filters.ChatFilter())
bot.add_custom_filter(IsAdmin())
# bot in loop
bot.infinity_polling()
