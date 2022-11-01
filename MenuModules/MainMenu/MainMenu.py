from email import message
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import Core.MessageSender as msg
import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event

from MenuModules.MenuState import menu



async def handleUserMessage(ctx: Message, menuState: dict):

    print(ctx.text)
    menuState["didHandled"] == True
    return menuState