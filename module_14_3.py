from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
import asyncio

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text= 'Рассчитать')
button2 = KeyboardButton(text= 'Информация')
button3 = KeyboardButton(text= 'Купить')
kb.add(button1, button2)
kb.add(button3)

kbi = InlineKeyboardMarkup()
ibutton1 = InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data='calories')
ibutton2 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data='formulas')
kbi.add(ibutton1, ibutton2)

kbi2 = InlineKeyboardMarkup()
ibutton3 = InlineKeyboardButton(text= 'Product1', callback_data='product_buying')
ibutton4 = InlineKeyboardButton(text= 'Product2', callback_data='product_buying')
ibutton5 = InlineKeyboardButton(text= 'Product3', callback_data='product_buying')
ibutton6 = InlineKeyboardButton(text= 'Product4', callback_data='product_buying')
kbi2.add(ibutton3, ibutton4, ibutton5, ibutton6)


class UserState(StatesGroup):
    age, growth, weight = State(), State(), State()

@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer(f'Для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x 1.55(Средняя физ.активность)\n')
                              # f'\nДля женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x 1.55')
    await call.answer()

@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    try:
        await message.answer(
            f"Норма калорий: "
            f"{(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5) * 1.55}")
    except ValueError:
        await message.answer('Неверные данные, используйте цифры')
    await state.finish()

@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup= kbi)

@dp.message_handler(text= 'Купить')
async def get_buying_list(message):
    await message.answer('Название: Product1, Описание: описание1, Цена: 100')
    with open('image.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer('Название: Product2, Описание: описание2, Цена: 200')
    with open('image.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer('Название: Product3, Описание: описание3, Цена: 300')
    with open('image.jpg', 'rb') as img:
        await message.answer_photo(img)
    await message.answer('Название: Product4, Описание: описание4, Цена: 400')
    with open('image.jpg', 'rb') as img:
        await message.answer_photo(img)

    await message.answer('Выберите продукт для покупки:', reply_markup= kbi2)

@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(commands= 'start')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup= kb)

@dp.message_handler()
async def all_messages(message):
    await message.answer(f'Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
