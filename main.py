

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Message, CallbackQuery

from logger import logger as log

import MenuModules.MenuDispatcher as dispatcher

# Initialize bot and dispatcher

apiKey = "5507754697:AAFKM_4mwbXkQv1XO0z_WhaCiPzTEoEXM7s"
bot = Bot(token=apiKey)
dp = Dispatcher(bot)

# =====================
# Bot commands
# =====================

@dp.message_handler(commands=['start'])
async def send_welcome_message_handler(message: types.Message):
    await dispatcher.handleUserStart(message)

@dp.message_handler()
async def default_message_handler(message: Message):
    await dispatcher.handleUserMessage(message)

@dp.callback_query_handler()
async def default_callback_handler(ctx: CallbackQuery):
    await dispatcher.handleCallback(ctx)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

log.info("Bot just started")