from email import message
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from Core.StorageManager.UniqueMessagesKeys import textConstant
from logger import logger as log

class OtherHumanEndingNo(MenuModuleInterface):

    namePrivate = MenuModuleName.otherHumanEndingNo

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        endingkeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.otherHumanButtonRestart.get)
        ).add(KeyboardButton(textConstant.otherHumanButtonWriteFairytale.get)
        ).add(KeyboardButton(textConstant.otherHumanButtonEndSession.get))

        await msg.answer(
            ctx = ctx,
            text = textConstant.otherHumanWhatsNext.get,
            keyboardMarkup = endingkeyboardMarkup
        )

        return Completion(
            inProgress = True,
            didHandledUserInteraction=True,
            moduleData={ "startMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if ctx.text == textConstant.otherHumanButtonRestart.get:
            return self.complete(nextModuleName=MenuModuleName.otherHuman.get)
        
        if ctx.text == textConstant.otherHumanButtonEndSession.get:
            return self.complete(nextModuleName=MenuModuleName.mainMenuNewSession.get)

        if ctx.text == textConstant.otherHumanButtonWriteFairytale.get:
            return self.complete(nextModuleName=MenuModuleName.fairytale.get)

        return self.canNotHandle(data)

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")

