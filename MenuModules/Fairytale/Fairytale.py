from email import message
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from Core.StorageManager.UniqueMessagesKeys import textConstant
from logger import logger as log

class Fairytale(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.fairytale

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleFairytale, "")
        
        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.fairytaleButtonStart.get))
        await msg.answer(
            ctx=ctx,
            text=textConstant.fairytaleStart.get,
            keyboardMarkup=keyboardMarkup
        )

        pageIndex = -1

        return Completion(
            inProgress = True,
            didHandledUserInteraction=True,
            moduleData={ "previousPageIndex" : pageIndex }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        pageIndex = data["previousPageIndex"]

        if pageIndex == -1 and ctx.text != textConstant.fairytaleButtonStart.get:
            return self.canNotHandle(data)

        pageIndex += 1
        
        FairytalePages = storage.getJsonData(storage.path.botContentFairytale)

        if pageIndex == len(FairytalePages):
            return self.complete(nextModuleName=MenuModuleName.fairytaleEnding.get)

        page = FairytalePage(FairytalePages[pageIndex])
        
        if len(FairytalePages) == pageIndex:
            return self.complete()
            
        if ctx.text == ctx.text:
            await sendFairytalePage(ctx, msg, page)

# =====================
# #ЭТО КОСТЫЛЬ, нужен для того чтобы переходить на otherHumanEnding
# #Скорее всего можно проще, но я не осилил
# ======================
        # if pageIndex == len(otherHumanPages) - 1:
        #     return self.complete(nextModuleName=MenuModuleName.otherHumanEnding.get)
        
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


class FairytalePage:

    message: str

    def __init__(self, data: dict):
        self.message = data["text"]

async def sendFairytalePage(ctx: Message, msg: MessageSender, page: FairytalePage):
    await msg.answer(
        ctx=ctx,
        text=page.message,
        keyboardMarkup=ReplyKeyboardRemove()
    )