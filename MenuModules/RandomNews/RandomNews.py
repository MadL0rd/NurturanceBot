from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.StorageManager.StorageManager import PathConfig
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log
from random import choice
from pathlib import Path

class RandomNews(MenuModuleInterface):

    keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.randomNewsButtonNews.get)
        ).add(KeyboardButton(textConstant.menuButtonReturnToMainMenu.get))

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.randomNews

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleNews, "")

        await msg.answer(
            ctx = ctx,
            text = textConstant.randomNewsStartText.get,
            keyboardMarkup = self.keyboardMarkup
        )
        await self.sendNews(ctx, msg)

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={}
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        messageText = ctx.text

        # Return to main menu
        if ctx.text == textConstant.menuButtonReturnToMainMenu.get:
            return self.complete(nextModuleName=MenuModuleName.mainMenu.get)

        # Send new news
        if messageText == textConstant.randomNewsButtonNews.get:
            await self.sendNews(ctx, msg)
            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData={}
            )

        return self.canNotHandle()
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    async def sendNews(self, ctx: CallbackQuery, msg: MessageSender):
        
        newsList = storage.getJsonData(storage.path.botContentNews)
        userNews = storage.getUserNews(ctx.from_user)
        if len(newsList) == len(userNews):
            await msg.answer(
            ctx = ctx,
            text = textConstant.randomNewsAllNewsWasShown.get,
            keyboardMarkup = self.keyboardMarkup
            )
            return
        
        arrayOfUnsendedNews=[]
        i = 1
        for i in range(1,len(newsList)+1): 
            if str(i) not in userNews:
                arrayOfUnsendedNews.append(i)
       
        newsNumber = choice(arrayOfUnsendedNews)
        newsLine = newsList[newsNumber-1]     
        NewsText = newsLine.get("text")
        newsPicture = newsLine.get("picture")
        
        userNews.append(str(newsNumber))
        storage.updateUserNews(ctx.from_user, userNews)
        

        await msg.answer(
            ctx = ctx,
            text = NewsText,
            keyboardMarkup = self.keyboardMarkup
            )

        await MessageSender.sendPhoto(
            self= self,
            ctx= ctx,
            url= newsPicture
        )
        #else:
           # await msg.answer(
            #    ctx = ctx,
             #   text = "Какая-то ебучая новость",
              #  keyboardMarkup = self.keyboardMarkup
            #)
        
        # pageIndex = 0
        # NewsPages = storage.getJsonData(storage.path.botContentNews)
        # if len(NewsPages) > pageIndex:
        #     page = NewsPage(NewsPages[pageIndex])
        #     await sendNews(ctx, msg, page)
        # else:
        #     log.error("News is empty")

class NewsPage:

    text: str
    picture: str

    def __init__(self, data: dict):
        self.message = data["ID"]
        self.message = data["text"]
        self.message = data["picture"]

async def sendNews(ctx: Message, msg: MessageSender, page: NewsPage):

    await msg.answer(
        ctx=ctx,
        text=page.text,
    )