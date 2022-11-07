from email import message
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log
from Core.StorageManager.UniqueMessagesKeys import textConstant
from random import choice


class EveningReflectionQuestions(MenuModuleInterface):

    namePrivate = MenuModuleName.eveningReflectionQuestions

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleEveningReflectionQuestions, "")

        await self.sendReflectionQuestion(ctx, msg)

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={}
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        # Going to Reflection menu
        if ctx.text == ctx.text:
            return self.complete(nextModuleName=MenuModuleName.reflectionMenu.get)
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    async def sendReflectionQuestion(self, ctx: CallbackQuery, msg: MessageSender):
        
        reflectionQuestionList = storage.getJsonData(storage.path.botContentEveningReflectionQuestions)

        reflectionQuestionLine = choice(reflectionQuestionList)   
        reflectionQuestionText = reflectionQuestionLine.get("text")
        
        await msg.answer(
            ctx = ctx,
            text = reflectionQuestionText,
            keyboardMarkup=ReplyKeyboardRemove()
        )

class EveningReflectionQuestionsPage:

    text: str

    def __init__(self, data: dict):
        self.message = data["ID"]
        self.message = data["text"]