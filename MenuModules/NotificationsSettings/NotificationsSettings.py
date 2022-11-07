from email import message
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from Core.StorageManager.UniqueMessagesKeys import textConstant
from logger import logger as log

class NotificationsSettings(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.notificationsSettings

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleOnboarding, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton("Утро")
        ).add(KeyboardButton("День")
        ).add(KeyboardButton("Вечер")
        ).add(KeyboardButton(textConstant.menuButtonReturnToMainMenu.get))

        await msg.answer(
            ctx=ctx,
            text=textConstant.notificationSettingsText.get,
            keyboardMarkup=keyboardMarkup
        )

        userNotifications = storage.getUserInfo(ctx.from_user)["notifications"]
        await msg.answer(
            ctx=ctx,
            text=f"Текущие настройки\nУтро:\t{userNotifications['morning']}\nДень:\t{userNotifications['day']}\nВечер:\t{userNotifications['evening']}",
            keyboardMarkup=keyboardMarkup
        )

        return Completion(
            inProgress = True,
            didHandledUserInteraction=True,
            moduleData={}
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "selectedType" not in data:
            if ctx.text == textConstant.menuButtonReturnToMainMenu.get:
                return self.complete(nextModuleName=MenuModuleName.mainMenu.get)

            if ctx.text == "Утро":
                keyboardMarkup = replyMarkupForNotificationType("morning")
                await msg.answer(
                    ctx=ctx,
                    text="Выбери время",
                    keyboardMarkup=keyboardMarkup
                )
                return Completion(
                    inProgress = True,
                    didHandledUserInteraction=True,
                    moduleData={
                        "selectedType": "morning"
                    }
                )

            if ctx.text == "День":
                keyboardMarkup = replyMarkupForNotificationType("day")
                await msg.answer(
                    ctx=ctx,
                    text="Выбери время",
                    keyboardMarkup=keyboardMarkup
                )
                return Completion(
                    inProgress = True,
                    didHandledUserInteraction=True,
                    moduleData={
                        "selectedType": "day"
                    }
                )

            if ctx.text == "Вечер":
                keyboardMarkup = replyMarkupForNotificationType("evening")
                await msg.answer(
                    ctx=ctx,
                    text="Выбери время",
                    keyboardMarkup=keyboardMarkup
                )
                return Completion(
                    inProgress = True,
                    didHandledUserInteraction=True,
                    moduleData={
                        "selectedType": "evening"
                    }
                )
            
            return self.canNotHandle(data=data)

        type = data["selectedType"]
        notoficationTimes = storage.getJsonData(storage.path.botContentNotificationTimes)
        if ctx.text in notoficationTimes[type] or ctx.text == noNotificationText:
            userInfo = storage.getUserInfo(ctx.from_user)
            userInfo["notifications"][type] = ctx.text
            storage.updateUserData(ctx.from_user, userInfo)
            return await self.handleModuleStart(ctx, msg)
    
        return self.canNotHandle(data)

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

def groupButtonsToPairs(source: list):
    result = []
    while len(source) > 0:
        if len(source) > 1:
            result.append([source[0], source[1]])
            del source[0]
            del source[0]
        else:
            result.append([source[0]])
            del source[0]
    return result

noNotificationText = "Не отправлять"

def replyMarkupForNotificationType(type: str) -> ReplyKeyboardMarkup:
    keyboardMarkup = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    notoficationTimes = storage.getJsonData(storage.path.botContentNotificationTimes)[type]
    notoficationTimes.append(noNotificationText)
    notoficationTimes = groupButtonsToPairs(notoficationTimes)
    for line in notoficationTimes:
        if len(line) > 1:
            keyboardMarkup.row(
                KeyboardButton(line[0]),
                KeyboardButton(line[1])
            )
        else:
            keyboardMarkup.row(
                KeyboardButton(line[0])
            )

    return keyboardMarkup