import requests
import telebot

from config import tg_bot_token, open_weather_token

bot = telebot.TeleBot(tg_bot_token)


@bot.message_handler(commands=["start"])
def start(message):
    """
    Handles the '/start' command. Sends a welcome message to the user.
    """
    bot.send_message(message.chat.id, f"Привіт,  {message.from_user.full_name}!\nНапиши мені назву міста"
                                      f" і я надішлю зведення погоди!")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    """
    Handles incoming text messages to retrieve and send weather information.
    """
    city = message.text.strip()
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
        data = response.json()
        cur_weather = data['main']['temp']
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        bot.send_message(message.chat.id,f"Погода в місті: {city}\nТемпература: {cur_weather}°C\n"
                         f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nВетер: {wind} м/с\n")
    except Exception as e:
        bot.send_message(message.chat.id, "Місто не знайдено. Спробуйте ще раз.")


bot.polling(none_stop=True)
