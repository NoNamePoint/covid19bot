
import sys
sys.path.append("D:\\projects_python\\COVIDBOT\\venv\\Lib\\site-packages")

from config import TOKEN
from config import COUNTRIES
from datetime import datetime
from covid import Covid
import telebot
from telebot import types


bot = telebot.TeleBot(TOKEN)
covid = Covid()

# print(covid.get_status_by_country_name(COUNTRIES["Россия"]))
#
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Россия')
    btn2 = types.KeyboardButton('США')
    btn3 = types.KeyboardButton('Франция')
    btn4 = types.KeyboardButton('Италия')
    btn5 = types.KeyboardButton('Германия')
    btn6 = types.KeyboardButton('Китай')
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)
    greet_message = f'<b>Приветствую {message.from_user.first_name}!</b> \nВведите страну'
    bot.send_message(message.chat.id, greet_message, parse_mode="html", reply_markup = keyboard)

@bot.message_handler(content_types=['text'])
def get_data(message):
    normalize_mess = message.text.strip().lower().capitalize()
    bot_response = ""
    if normalize_mess not in COUNTRIES:
        all_cases = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()
        bot_response = f"<u><b>Подтвержденные случаи:</b></u> {all_cases}\n <u><b>Поправилось:</b></u> {recovered}\n <u><b>Умерло:</b></u> {deaths}"
    else:
        try:
            data = covid.get_status_by_country_name(COUNTRIES[normalize_mess])
        except:
            bot_response = "Такой страны не нашел"
        all_cases = f'<u><b>Подтвержденные случаи:</b></u> {data["confirmed"]}'
        time = int(str(data["last_update"])[:10])
        date = datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        last_update =  f"Последнее обновление данных: {date}"
        recovered = f'<b>Поправилось:</b> {data["recovered"]}'
        deaths = f'<b>Умерло:</b> {data["deaths"]}'
        bot_response = f"{all_cases}\n {recovered}\n {deaths}\n {last_update}"
    bot.send_message(message.chat.id, bot_response, parse_mode="html")



bot.polling(none_stop=True)


# if normalize_mess == "россия":
#     data = covid.get_status_by_country_name(COUNTRIES['Россия'])
# elif normalize_mess == "сша":
#     data = covid.get_status_by_country_name(COUNTRIES['США'])
# elif normalize_mess == "франция":
#     data = covid.get_status_by_country_name(COUNTRIES['Франция'])
# elif normalize_mess == "италия":
#     data = covid.get_status_by_country_name(COUNTRIES['Италия'])
# elif normalize_mess == "германия":
#     data = covid.get_status_by_country_name(COUNTRIES['Германия'])
# elif normalize_mess == "китай":
#     data = covid.get_status_by_country_name(COUNTRIES['Китай'])
