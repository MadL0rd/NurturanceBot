from email import message
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class Onboarding(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.onboarding

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleOnboarding, "")

        pageIndex = 0
        onboardingPages = storage.getJsonData(storage.path.botContentOnboarding)
        if len(onboardingPages) > pageIndex:
            page = OnboardingPage(onboardingPages[pageIndex])
            await sendOnboardingPage(ctx, msg, page)
        else:
            log.error("Onboarding is empty")
            return Completion(
                inProgress = False,
                didHandledUserInteraction=True,
                moduleData={}
            )

        return Completion(
            inProgress = pageIndex < len(onboardingPages),
            didHandledUserInteraction=True,
            moduleData={ "previousPageIndex" : pageIndex }
        )

    async def handleModuleNews(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleNews, "")

        pageIndex = 0
        NewsPages = storage.getJsonData(storage.path.botContentNews)
        if len(NewsPages) > pageIndex:
            page = NewsPage(NewsPages[pageIndex])
            await sendNews(ctx, msg, page)
        else:
            log.error("News is empty")
            return Completion(
                inProgress = False,
                didHandledUserInteraction=True,
                moduleData={}
            )

        return Completion(
            inProgress = pageIndex < len(NewsPages),
            didHandledUserInteraction=True,
            moduleData={ "previousPageIndex" : pageIndex }
        )

    async def handleUserMessage(self, ctx: Message, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        pageIndex = data["previousPageIndex"]
        onboardingPages = storage.getJsonData(storage.path.botContentOnboarding)
        page = OnboardingPage(onboardingPages[pageIndex])

        if ctx.text != page.buttonText:
            return self.canNotHandle(data)
        
        pageIndex += 1
        if len(onboardingPages) == pageIndex:
            return self.complete()
        
        page = OnboardingPage(onboardingPages[pageIndex])
        await sendOnboardingPage(ctx, msg, page)
    
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

class OnboardingPage:

    message: str
    buttonText: str

    def __init__(self, data: dict):
        self.message = data["message"]
        self.buttonText = data["buttonText"]

async def sendOnboardingPage(ctx: Message, msg: MessageSender, page: OnboardingPage):

    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    ).add(KeyboardButton(page.buttonText))

    await msg.answer(
        ctx=ctx,
        text=page.message,
        keyboardMarkup=keyboardMarkup
    )

class NewsPage:

    text: str
    picture: str

    def __init__(self, data: dict):
        self.message = data["text"]
        self.message = data["picture"]

async def sendNews(ctx: Message, msg: MessageSender, page: NewsPage):

    await msg.answer(
        ctx=ctx,
        text=page.text,
    )