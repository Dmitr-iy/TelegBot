import asyncio
import os
import math
import requests
import datetime
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import dotenv

dotenv.load_dotenv()


# Включаем логирование
logging.basicConfig(level=logging.INFO,
                    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')

bot = Bot(token=os.getenv("TOKEN"))

dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start_handler(message: types.Message):
    await message.answer("Привет! Напиши мне название города и я пришлю сводку погоды")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

@dp.message()
async def get_weather(message: types.Message,):

    try:
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&units=metric&appid={os.getenv("ID")}')
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        # продолжительность дня
        length_of_the_day = (datetime.datetime.fromtimestamp(data["sys"]["sunset"]) -
                             datetime.datetime.fromtimestamp(data["sys"]["sunrise"]))
    except:
        await message.reply("Проверьте название города!")

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    weather_description = data["weather"][0]["main"]

    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        # если эмодзи для погоды нет, выводим другое сообщение
        wd = "Посмотри в окно, я не понимаю, что там за погода..."

    await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Погода в городе: {city}\nТемпература: {cur_temp}°C {wd}\n"
        f"Влажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
        f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
        f"Хорошего дня!"
    )

if __name__ == "__main__":
    asyncio.run(main())


