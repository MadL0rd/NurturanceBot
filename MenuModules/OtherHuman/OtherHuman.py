from email import message
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from Core.StorageManager.UniqueMessagesKeys import textConstant
from logger import logger as log

class OtherHuman(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.otherHuman

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleOtherHuman, "")

        pageIndex = 0
        otherHumanPages = storage.getJsonData(storage.path.botContentOtherHuman)
        if len(otherHumanPages) > pageIndex:
            page = OtherHumanPage(otherHumanPages[pageIndex])
            await sendOtherHumanPage(ctx, msg, page)
        else:
            log.error("OtherHuman is empty")
            return Completion(
                inProgress = False,
                didHandledUserInteraction=True,
                moduleData={}
            )

        return Completion(
            inProgress = pageIndex < len(otherHumanPages),
            didHandledUserInteraction=True,
            moduleData={ "previousPageIndex" : pageIndex }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        pageIndex = data["previousPageIndex"]
        otherHumanPages = storage.getJsonData(storage.path.botContentOtherHuman)
        page = OtherHumanPage(otherHumanPages[pageIndex])

        if ctx.text != page.buttonText and pageIndex != 1:
            return self.canNotHandle(data)
        
        pageIndex += 1
        if len(otherHumanPages) == pageIndex:
            return self.complete()

        # Надо придумать как ожидать ввод данных от пользователя
        # if pageIndex == 2 and ctx.text == ctx.text:
        #     return await sendOtherHumanPage(ctx, msg, page)
            


        page = OtherHumanPage(otherHumanPages[pageIndex])
        await sendOtherHumanPage(ctx, msg, page)

        # if pageIndex == len(otherHumanPages):
        #     self.complete(nextModuleName=MenuModuleName.otherHumanEnding.get)
    
        return Completion(
            inProgress = True,
            didHandledUserInteraction = True,
            moduleData = { "previousPageIndex" : pageIndex }
        )

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        





    # =====================
    # Custom stuff
    # =====================


class OtherHumanPage:

    message: str
    buttonText: str

    def __init__(self, data: dict):
        self.message = data["message"]
        self.buttonText = data["buttonText"]

async def sendOtherHumanPage(ctx: Message, msg: MessageSender, page: OtherHumanPage):

    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    ).add(KeyboardButton(page.buttonText))

    await msg.answer(
        ctx=ctx,
        text=page.message,
        keyboardMarkup=keyboardMarkup
    )