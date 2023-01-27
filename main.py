import json
from os.path import exists
import telebot 
from telebot import types 

from parsing import main, today

token = '5874004351:AAEdF02jEYH-TLJ2TjB0og-7TQRUWUPtPMw'

bot = telebot.TeleBot(token)

def get_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    with open(f'news_{today}.json','r') as file:
        for number, news in enumerate(json.load(file)):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=news['title'],
                    callback_data=str(number)
                )
            )
    return keyboard
            


@bot.message_handler(commands=['start','hello'])
def start_bot(messege: types.Message):
    if exists(f'news_{today}.json'):
        main()
    bot.send_message(messege.chat.id,f'Hello,{messege.from_user.first_name}!Today News:',reply_markup=get_keyboard())

@bot.callback_query_handler(func=lambda callback: True)
def send_news_detail(callback: types.CallbackQuery):
    with open('news.json','r') as file:
        news = json.load(file)[int(callback.data)]
        text = f"{news['title']}\n{news['description']}\n{news['news_link']}"
        bot.send_message(
            callback.message.chat.id,
            text=text
        )

bot.polling()

# TODO: popravit chtnie failov (for Tima)
# TODO: posledniuye uslovie na knopku Qiut bot Doljen otpravit soobshenie "dosvidaniye" (for Me )