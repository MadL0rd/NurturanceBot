from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class MainMenu(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.mainMenu

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleMainMenu, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        )
        for buttonText in self.menuDict:
            keyboardMarkup.add(KeyboardButton(buttonText))

        userTg = ctx.from_user
        userInfo = storage.getUserInfo(userTg)

        if "isAdmin" in userInfo and userInfo["isAdmin"] == True:
            keyboardMarkup.add(KeyboardButton(textConstant.menuButtonAdmin.get))

        await msg.answer(
            ctx = ctx,
            text = textConstant.mainMenuText.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "startMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "startMessageDidSent" not in data or data["startMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if messageText == textConstant.menuButtonAdmin.get:
            return self.complete(nextModuleName = MenuModuleName.admin.get)

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
            textConstant.menuButtonExercises.get: MenuModuleName.exercises.get,
            # textConstant.menuButtonRandomNews.get: MenuModuleName.randomNews.get,
            # textConstant.menuButtonRelax.get: MenuModuleName.relax.get,
            textConstant.menuButtonNotifications.get: MenuModuleName.notificationsSettings.get,
            textConstant.menuButtonQuizDepression.get: MenuModuleName.quizDepression.get,
            textConstant.menuButtonQuizAnxiety.get: MenuModuleName.quizAnxiety.get
        }