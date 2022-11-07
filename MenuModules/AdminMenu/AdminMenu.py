from aiogram.types import Message, CallbackQuery
from main import bot
import Core.StorageManager.StorageManager as storage
from logger import logger as log
import Core.GoogleSheetsService as sheets
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName

class AdminMenu(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.admin

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.adminMenuButtonReloadData.get)
        ).add(KeyboardButton(textConstant.adminMenuButtonLoadData.get)
        ).add(KeyboardButton("ZALUPA")
        ).add(KeyboardButton(textConstant.menuButtonReturnToMainMenu.get))
        

        await msg.answer(
            ctx = ctx,
            text = textConstant.adminMenuText.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress = True,
            didHandledUserInteraction=True,
            moduleData={ "startMessageDidSent" : True }
        )


    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if ctx.text == textConstant.menuButtonReturnToMainMenu.get:
            return self.complete(nextModuleName=MenuModuleName.mainMenu.get)
        
        if ctx.text == "ZALUPA":
            return self.complete(nextModuleName=MenuModuleName.eveningReflectionQuestions.get)
        
        if ctx.text == textConstant.adminMenuButtonReloadData.get:
            
            log.info("Bot sheets data update start")

            message = await ctx.answer(updateStateReloadDataMessage(0))

            sheets.updateUniqueMessages()
            await message.edit_text(updateStateReloadDataMessage(1))

            sheets.updateOnboarding()
            await message.edit_text(updateStateReloadDataMessage(2))

            sheets.updateNews()
            await message.edit_text(updateStateReloadDataMessage(3))

            sheets.updatetaskEmotions()
            await message.edit_text(updateStateReloadDataMessage(4))

            sheets.updatetaskThoughts()
            await message.edit_text(updateStateReloadDataMessage(5))

            sheets.updateQuestions()
            await message.edit_text(updateStateReloadDataMessage(6))

            sheets.updateEveningReflectionQuestions()
            await message.edit_text(updateStateReloadDataMessage(7))

            sheets.updateFairytale()
            await message.edit_text(updateStateReloadDataMessage(8))

            sheets.updateOhterHuman()

            await message.edit_text("❇️ Тексты обновлены")

            log.info("Bot sheets data update complete")

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True
            )
        
        if ctx.text == textConstant.adminMenuButtonLoadData.get:

            log.info("Tables creation start")

            message = await ctx.answer("⚠️ Подождите, идет подготовка данных\n🔴 Таблица с полной историей\n🔴 Агрегированная таблица")
            storage.generateTotalTable()
            await message.edit_text("⚠️ Подождите, идет подготовка данных\n🟢 Таблица с полной историей\n🔴 Агрегированная таблица")
            storage.generateStatisticTable()
            await message.edit_text("Данные готовы и уже выгружаются\n🟢 Таблица с полной историей\n🟢 Агрегированная таблица")
            await bot.send_document(chat_id = ctx.chat.id, document = storage.path.totalHistoryTableFile.open("rb"),)
            await bot.send_document(chat_id = ctx.chat.id, document = storage.path.statisticHistoryTableFile.open("rb"),)
            await message.edit_text("❇️ Выгрузка завершена")

            log.info("Tables creation complete")

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True
            )

        return self.canNotHandle(data)

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

def updateStateReloadDataMessage(stateIndex: int) -> str:
    text = "⚠️ Подождите, идет выгрузка данных из гугл таблицы"
    tablePageNames = [
        "УникальныеСообщения",
        "Онбординг",
        "Новости",
        'УпражненияЭмоции',
        'УпражненияМысли',
        'Вопросы',
        'ВечерняяРефлексияВопросы',
        'Сказка',
        'Работа с другим человеком'
    ]
    for index, value in enumerate(tablePageNames):
        indicator = "🔴" if index > stateIndex else "🟢"
        text += f"\n{indicator} {value}"

    return text