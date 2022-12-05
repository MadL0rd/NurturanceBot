from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class TestMenu(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.testMenu

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleTestMenu, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        for buttonText in self.menuDict:
            keyboardMarkup.add(KeyboardButton(buttonText))

        await msg.answer(
            ctx = ctx,
            text = textConstant.testMenuText.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "testMenuMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "testMenuMessageDidSent" not in data or data["testMenuMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText not in self.menuDict:
            return self.canNotHandle(data)

        return self.complete(nextModuleName = self.menuDict[messageText])
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        # TODO: temporary module block
        return {
            textConstant.menuButtonQuizDepression.get: MenuModuleName.quizDepression.get,
            textConstant.menuButtonQuizAnxiety.get: MenuModuleName.quizAnxiety.get,
            textConstant.menuButtonReturnToMainMenu.get: MenuModuleName.mainMenu.get
        }