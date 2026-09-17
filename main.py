import telebot
from secrets import secrets
from telebot import types
import requests
from response_formatting import wind_deg_new,wind_speed_new,summarize
from bot_functions import split_forecast
import json

token = secrets.get('BOT_API_TOKEN')
api_weather=secrets.get('API_WEATHER')
bot = telebot.TeleBot(token)


def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users(users):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

users=load_users()


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    action_button = types.KeyboardButton("Погода сейчас")
    choice_button = types.KeyboardButton("Выбрать город")
    weather_today=types.KeyboardButton("Погода на сегодня")
    weather_tomorrow=types.KeyboardButton("Погода на завтра")
    markup.add(action_button, choice_button, weather_today, weather_tomorrow)
    bot.send_message(message.chat.id, text="Привет, {0.first_name} \nВоспользуйся кнопками".format(message.from_user),
                     reply_markup = markup)

@bot.message_handler(content_types=['text'])
def buttons(message):
    if (message.text == "Выбрать город"):
        bot.send_message(message.chat.id, text="Отправь свой город")
        bot.register_next_step_handler(message, choice_city)
    elif (message.text == "Погода сейчас"):
        weather_new(message)
    elif (message.text == 'Погода на сегодня'):
        weather_selected(message,'today')
    elif (message.text == 'Погода на завтра'):
        weather_selected(message,'tomorrow')
    else:
        bot.send_message(message.chat.id, text="Я могу отвечать только на нажатие кнопок")


def choice_city(message):
    city = message.text.strip()
    users[str(message.from_user.id)] = city
    save_users(users)
    bot.send_message(message.chat.id, f"Город сохранён: {city}")


def weather_new(message):
    user = str(message.from_user.id)
    if user in users:
        user_country=users[user]
        url = f'http://api.openweathermap.org/data/2.5/weather?q={user_country}&APPID={api_weather}&units=metric&lang=ru' 
        weather_data = requests.get(url).json()

        if str(weather_data.get("cod")) != "200":
            bot.send_message(message.chat.id, "Город не найден, попробуй другой")
            return
        
        temperature = weather_data['main']['temp']
        temperature_feels = weather_data['main']['feels_like']
        weather = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        wind_deg = weather_data['wind'].get('deg', 0)
        bot.send_message(message.chat.id,
                         text = f"Сейчас в городе {user_country} {temperature:.1f}°C\nОщущается как {temperature_feels:.1f}°C\nТекущая погода: {weather}\nСкорость ветра: {wind_speed} м/с, {wind_speed_new(wind_speed)}\nНаправление ветра: {wind_deg_new(wind_deg)}")
    else:
        bot.send_message(message.chat.id, text="Отправь мне свой город")
        bot.register_next_step_handler(message, choice_city)


def weather_selected(message,day):
    user = str(message.from_user.id)
    if user not in users:
        msg = bot.send_message(message.chat.id, "Сначала выбери город")
        bot.register_next_step_handler(msg, choice_city)
        return
    
    user_country = users[user]
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={user_country}&appid={api_weather}&units=metric&lang=ru'
    weather_data = requests.get(url).json()

    if str(weather_data.get("cod")) != "200":
        bot.send_message(message.chat.id, "Город не найден, попробуй другой")
        return
    
    today_items, tomorrow_items = split_forecast(weather_data)
    if day == 'today':
        weather=today_items
    elif day == 'tomorrow':
        weather = tomorrow_items
    else:
        bot.send_message(message.chat.id, "Неизвестный период")
        return

    if not weather:
        bot.send_message(message.chat.id, "Нет данных на этот день")
        return
    
    bot.send_message(message.chat.id,text=summarize(weather))
 


bot.polling(none_stop=True, interval=0)