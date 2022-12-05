import asyncio
import sys
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, CallbackQuery

from logger import logger as log

from Core.NotificationService import NotificationService
import MenuModules.MenuDispatcher as dispatcher
from Core.GoogleSheetsServiseFunctions import functions as dataUpdateFunctions

# =====================
# Version 1.2.0
# =====================

# Initialize bot and dispatcher

log.info(sys.argv)

# Main token
apiKey = "5659838410:AAEw9C4HuJs5R_wlzFpXeldJPk1N9ELLez4"

if len(sys.argv) > 1:
    apiKey = sys.argv[1]

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

async def on_startup(_):
    for func in dataUpdateFunctions:
        func()
    notifications = NotificationService(bot)
    notifications.configureNotifications()
    asyncio.create_task(notifications.threadedNotification())
    log.info("Bot just started")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)