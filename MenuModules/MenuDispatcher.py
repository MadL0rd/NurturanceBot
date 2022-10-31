import json
from mimetypes import init

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Message, CallbackQuery

import Core.MessageSender as msg
import Core.StorageManager as storage
from Core.StorageManager import UserHistoryEvent as event

from logger import logger as log
from main import bot

async def handleUserStart(ctx: Message):

    log.debug("Did handle UserMessage")

    storage.getUserInfo(ctx.from_user)


async def handleCallback(ctx: CallbackQuery):

    log.debug("Did handle callback")
    
    # ctxData = json.loads(ctx.data)
    # print(ctxData)
    storage.getUserInfo(ctx.from_user)

async def handleUserMessage(ctx: Message):

    user = ctx.from_user
    log.debug(f"Did handle User{user.id} message")
    storage.logToUserHistory(user, event.sendMessage, "Отправил сообщение")

    userInfo = storage.getUserInfo(user)

    if "isAdmin" in userInfo and userInfo["isAdmin"] == True:
        if ctx.text == "kek" or ctx.text == "Данные о пользователях":
            message = await ctx.answer("Подождите, идет подготовка данных\n🔴 Таблица с полной историей\n🔴 Агрегированная таблица")
            storage.generateTotalTable()
            await message.edit_text("Подождите, идет подготовка данных\n🟢 Таблица с полной историей\n🔴 Агрегированная таблица")
            storage.generateStatisticTable()
            await message.edit_text("Данные готовы и уже выгружаются\n🟢 Таблица с полной историей\n🟢 Агрегированная таблица")
            await bot.send_document(chat_id = ctx.chat.id, document = storage.path.totalHistoryTableFile.open("rb"),)
            await bot.send_document(chat_id = ctx.chat.id, document = storage.path.statisticHistoryTableFile.open("rb"),)
            await message.edit_text("Выгрузка завершена")


