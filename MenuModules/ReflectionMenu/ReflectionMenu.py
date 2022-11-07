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

class ReflectionMenu(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.reflectionMenu

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.reflectionMenuButtonFairytale.get)
        ).add(KeyboardButton(textConstant.reflectionMenuButtonOtherHuman.get)
        ).add(KeyboardButton(textConstant.menuButtonReturnToMainMenu.get))
        

        await msg.answer(
            ctx = ctx,
            text = textConstant.reflectionMenuText.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress = True,
            didHandledUserInteraction=True,
            moduleData={ "startMessageDidSent" : True }
        )


    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if ctx.text == textConstant.reflectionMenuButtonFairytale.get:
            return self.complete(nextModuleName=MenuModuleName.mainMenu.get)
        
        if ctx.text == textConstant.reflectionMenuButtonOtherHuman.get:
            return self.complete(nextModuleName=MenuModuleName.otherHuman.get)

        if ctx.text == textConstant.menuButtonReturnToMainMenu.get:
            return self.complete(nextModuleName=MenuModuleName.mainMenu.get)        

        return self.canNotHandle(data)

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================
