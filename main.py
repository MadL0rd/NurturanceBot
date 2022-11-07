import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, CallbackQuery

from logger import logger as log

from Core.NotificationService import NotificationService
import MenuModules.MenuDispatcher as dispatcher

# Initialize bot and dispatcher

# Main token
apiKey = "5659838410:AAEw9C4HuJs5R_wlzFpXeldJPk1N9ELLez4"

# Test token
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

async def on_startup(_):
    notifications = NotificationService(bot)
    notifications.configureNotifications()
    asyncio.create_task(notifications.threadedNotification())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

log.info("Bot just started")