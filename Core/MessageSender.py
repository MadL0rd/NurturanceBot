
from mimetypes import init
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Message, CallbackQuery

from main import bot

class MessageKek:

    userId: int

    def __init__(self, userId: int):
        self.userId = userId


async def msg(message: MessageKek):
    print(message.userId)

