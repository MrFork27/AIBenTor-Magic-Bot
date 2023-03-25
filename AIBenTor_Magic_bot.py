import telebot
from config import BOT_TOKEN, ALLOWED_CHATS, OPENAI_API_KEY
from telebot import custom_filters


# Bot
bot = telebot.TeleBot(BOT_TOKEN)


# Admin commands
# All admin actions must have the 'is_admin' filter
@bot.message_handler(chat_id=ALLOWED_CHATS, is_admin=True, commands=['admingetchatid'])
def admin_get_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, chat_id)


# Start, hello
@bot.message_handler(chat_id=ALLOWED_CHATS, commands=['start', 'hello'])
def send_start(message):
    reply_message = "Hola, soy AIBenTor Magic Bot!!!"
    bot.reply_to(message, reply_message)


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
