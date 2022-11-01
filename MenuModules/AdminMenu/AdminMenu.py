from aiogram.types import Message, CallbackQuery
from main import bot
import Core.StorageManager.StorageManager as storage
from logger import logger as log
import Core.GoogleSheetsService as sheets

async def handleUserMessage(ctx: Message):
    if ctx.text == "UserData" or ctx.text == "Данные о пользователях":

        log.info("Tables creation start")

        message = await ctx.answer("Подождите, идет подготовка данных\n🔴 Таблица с полной историей\n🔴 Агрегированная таблица")
        storage.generateTotalTable()
        await message.edit_text("Подождите, идет подготовка данных\n🟢 Таблица с полной историей\n🔴 Агрегированная таблица")
        storage.generateStatisticTable()
        await message.edit_text("Данные готовы и уже выгружаются\n🟢 Таблица с полной историей\n🟢 Агрегированная таблица")
        await bot.send_document(chat_id = ctx.chat.id, document = storage.path.totalHistoryTableFile.open("rb"),)
        await bot.send_document(chat_id = ctx.chat.id, document = storage.path.statisticHistoryTableFile.open("rb"),)
        await message.edit_text("Выгрузка завершена")

        log.info("Tables creation complete")
    
    if ctx.text == "kek":
        
        log.info("Bot sheets data update start")

        sheets.updateOnboarding()
        sheets.updateUniqueMessages()

        log.info("Bot sheets data update complete")