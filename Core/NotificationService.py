import aioschedule
from aiogram import Bot
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.UniqueMessagesKeys import textConstant

from logger import logger as log
class NotificationService:

    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    def configureNotifications(self):
        notoficationTimes = storage.getJsonData(storage.path.botContentNotificationTimes)

        for item in notoficationTimes["morning"]:
            aioschedule.every().day.at(item).do(self.morningNotification, item)

        for item in notoficationTimes["day"]:
            aioschedule.every().day.at(item).do(self.dayNotification, item)

        for item in notoficationTimes["evening"]:
            aioschedule.every().day.at(item).do(self.eveningNotification, item)

    async def threadedNotification(self):
        log.info("Notification thread start")
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(10)

    async def morningNotification(self, time: str):
        log.info(time)
        userIds = getAllUsersWith("morning", time)

        for userId in userIds:
            log.info(f"Send notofication to user: {userId}")

            try:
                await self.bot.send_message(userId, textConstant.notificationMorningText.get)
            except Exception as exception:
                log.exception(exception)

    async def dayNotification(self, time: str):
        log.info(time)
        userIds = getAllUsersWith("day", time)

        for userId in userIds:
            log.info(f"Send notofication to user: {userId}")

            try:
                await self.bot.send_message(userId, textConstant.notificationDayText.get)
            except Exception as exception:
                log.exception(exception)

    async def eveningNotification(self, time: str):
        log.info(time)
        userIds = getAllUsersWith("evening", time)

        for userId in userIds:
            log.info(f"Send notofication to user: {userId}")
            
            try:
                await self.bot.send_message(
                    userId, 
                    textConstant.notificationEveningText.get,
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[[InlineKeyboardButton(text="????????????", callback_data='StartEveningReflection')]]
                    )
                )
            except Exception as exception:
                log.exception(exception)

def getAllUsersWith(type: str, time: str) -> list:
    userIds = []

    for userFolder in storage.path.userFoldersAll:
        userInfo = storage.getJsonData(userFolder / "info.json")
        if userInfo["notifications"][type] == time:
            userIds.append(userInfo["info"]["id"])

    return userIds