from aiogram import Bot, Dispatcher, types, executor
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Привет мир! Привет Гикс")

@dp.message_handler(commands='help')
async def help(message:types.Message):
    await message.answer("Чем могу помочь вам?")

@dp.message_handler(text="Привет")
async def hello(message:types.Message):
    await message.answer("Привет, как дела?")

@dp.message_handler(commands='test')
async def testing(message:types.Message):
    await message.answer("Тест")
    await message.reply("Тест")
    await message.answer_location(40.51932802044946, 72.8030024754967)
    await message.answer_photo('https://vg-stroy.com/wp-content/uploads/2022/01/2022-02-09-14.22.54.jpg')
    with open('C:/Users/admin/Pictures/391299613_852174056560281_796826487165725461_n.jpg', 'rb') as photo:
        await message.answer_photo(photo)
    await message.answer_dice()
    await message.answer_contact('+996772343206', 'Toktorov', 'Kurmanbek')

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply("Я вас не понял, введите /help")

executor.start_polling(dp)