import asyncio
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from time import sleep
import aioschedule

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class Relax(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.relax

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleMainMenu, "")

        await msg.answer(
            ctx=ctx,
            text=textConstant.relaxStartMessage.get,
            keyboardMarkup=ReplyKeyboardRemove()
        )

        loop = asyncio.get_event_loop()
        loop.create_task(sendMessageAfterFiveMinutes(ctx, msg))

        return self.complete()

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        return self.complete()

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

    @property
    def menuDict(self) -> dict:
        # TODO: update after modules implementation
        return {
            # textConstant.menuButtonRelax.get: MenuModuleName.relax.get
            textConstant.menuButtonExercises.get: MenuModuleName.exercises.get,
            textConstant.menuButtonRandomNews.get: MenuModuleName.randomNews.get,
            textConstant.menuButtonRelax.get: MenuModuleName.onboarding.get,
            textConstant.menuButtonNotifications.get: MenuModuleName.notificationsSettings.get
        }

@asyncio.coroutine
async def sendMessageAfterFiveMinutes(ctx: Message, msg: MessageSender):
    await asyncio.sleep(5 * 60)
    await msg.answer(
        ctx=ctx,
        text=textConstant.relaxCompleteMessage.get,
        keyboardMarkup = ReplyKeyboardMarkup()
    )