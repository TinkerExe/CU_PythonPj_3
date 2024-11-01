import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from weather import get_weather
# from testApi.test_api import test_get_weather

from const import TOKEN

class WeatherStates(StatesGroup):
    period = State()
    cities = State()

periods = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='2 дня', callback_data='2days')],
    [InlineKeyboardButton(text='3 дня', callback_data='3days')],
    [InlineKeyboardButton(text='4 дня', callback_data='4days')],
    [InlineKeyboardButton(text='5 дней', callback_data='5days')]
])

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(WeatherStates.period)
    await message.answer(
        'Привет! Я бот, который предоставляет прогноз погоды. '
        'Выберите период, на который вы хотите получить прогноз, с помощью команды /weather.'
    )

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        'Что я могу:\n'
        '/weather - Поздароваться.\n'
        '/weather - Получить прогноз погоды.\n'
        '/help - Показать это сообщение.'
    )

@dp.message(Command('weather'))
async def cmd_weather(message: Message, state: FSMContext):
    await message.answer('Выберите, на сколько дней показывать прогноз погоды.', reply_markup=periods)

@dp.callback_query()
async def change_period(callback: CallbackQuery, state: FSMContext):
    days = int(callback.data[0])
    await state.update_data(days=days)
    await callback.message.answer(
        'Введите интересующие вас точки маршрута через запятую (например, "Москва, ..., Казань").'
    )
    await state.set_state(WeatherStates.cities)

@dp.message()
async def process_cities(message: Message, state: FSMContext):
    data = await state.get_data()
    days = data.get('days')

    cities = set(city.strip() for city in message.text.split(', '))
    weather_responses = []

    for city in cities:

        weather_data = get_weather(city, days)
#        weather_data = test_get_weather(city, days)

        if isinstance(weather_data, str) and 'error' in weather_data:
            await message.answer(f'Ошибка: Не удалось получить данные для города "{city}".')
        else:
            response = f'<b>Город:</b> {city}\n'
            for day in weather_data:
                date = day['date']
                min_temp = day['temperature']['min']
                max_temp = day['temperature']['max']
                forecast = day['text'][0]
                humidity = day['humidityAg']
                wind_speed = day['windSpeed'][0]

                response += (
                    f'<b>Дата:</b> {date}\n'
                    f'<b>Прогноз:</b> {forecast}\n'
                    f'<b>Температура:</b> {min_temp} - {max_temp} °C\n'
                    f'<b>Влфжность:</b> {humidity} %\n'
                    f'<b>Скорость ветра:</b> {wind_speed:.1f} м/с\n\n'
                )

            weather_responses.append(response)

    await message.answer('\n'.join(weather_responses), parse_mode='HTML')

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))



