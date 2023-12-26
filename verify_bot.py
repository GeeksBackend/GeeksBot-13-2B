from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from logging import basicConfig, INFO
from config import token 
from email.message import EmailMessage
import sqlite3, os, time, smtplib, random

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

connection = sqlite3.connect('verify.db')
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(200),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    created VARCHAR(200),
    verify VARCHAR(10),
    email VARCHAR(255)
);
""")

start_buttons = [
    types.InlineKeyboardButton('Верификация', callback_data='verify_user'),
    types.InlineKeyboardButton('Наш сайт', url='https://geeks.kg')
]
start_keyboard = types.InlineKeyboardMarkup().add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    exists_user = cursor.fetchall()
    if not exists_user:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (message.from_user.id, message.from_user.username, message.from_user.first_name,
                       message.from_user.last_name, time.ctime(), 'False', 'null'))
        cursor.connection.commit()
    await message.answer(f"Привет {message.from_user.full_name}. Для использования бота пройдите верификацию", reply_markup=start_keyboard)

class VerifyState(StatesGroup):
    code = State()
    email = State()
    user_code = State()

@dp.callback_query_handler(lambda call: call.data == 'verify_user')
async def start_verify_user(callback:types.CallbackQuery):
    await callback.message.answer("Введите свою почту для верификации аккаунта:")
    await VerifyState.email.set()

@dp.message_handler(state=VerifyState.email)
async def send_code_and_verify(message:types.Message, state:FSMContext):
    await state.update_data(email=message.text)
    random_code = random.randint(111111, 999999)
    await state.update_data(code=random_code)
    sender = 'toktorovkurmanbek92@gmail.com' #тут пишите свою почту
    password = 'akxhtueaftuiwvwx'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    msg = EmailMessage()
    msg.set_content(f"Ваш код верификации: {random_code}")

    msg['Subject'] = "Код верификации" 
    msg['From'] = sender 
    msg['To'] = message.text

    try:
        server.login(sender, password)
        server.send_message(msg)
        await message.answer("Код успешно отправлен в вашу почту")
    except Exception as error:
        await message.answer(f"Error: {error}")

    await message.answer("Введите код:")
    await VerifyState.user_code.set()

@dp.message_handler(state=VerifyState.user_code)
async def check_code(message:types.Message, state:FSMContext):
    result = await storage.get_data(user=message.from_user.id)
    print(result)
    if result['code'] == int(message.text):
        await message.answer("Вы успешно прошли верификацию")
        await state.finish()
    else:
        await message.answer("Неправильный код. Попробуйте еще")

executor.start_polling(dp, skip_updates=True)