from unicodedata import name
from aiogram.types import Message, CallbackQuery
import enum
import json
from Core.MessageSender import MessageSender

from logger import logger as log

class MenuModuleHandlerCompletion:

    inProgress: bool
    didHandledUserInteraction: bool
    moduleData: dict

    def __init__(self, inProgress: bool, didHandledUserInteraction: bool, moduleData: dict):
        self.inProgress = inProgress
        self.didHandledUserInteraction = didHandledUserInteraction
        self.moduleData = moduleData

class MenuModuleInterface:

    name: str

    def callbackData(self, data: dict, msg: MessageSender) -> str:
        data = {
            "module": self.name,
            "data": data
        }
        return json.dumps(data)

    def canNotHandle(self, data: dict) -> MenuModuleHandlerCompletion:
        return MenuModuleHandlerCompletion(
            inProgress = True,
            didHandledUserInteraction=False,
            moduleData=data
        )

    def complete(self) -> MenuModuleHandlerCompletion:
        return MenuModuleHandlerCompletion(
            inProgress = False,
            didHandledUserInteraction=True,
            moduleData={}
        )

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> MenuModuleHandlerCompletion:
        log.error("! Function in menu module does not overrided !")

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> MenuModuleHandlerCompletion:
        log.error(f"! Function in menu module does not overrided !\nData: {data}")

    async def handleCallback(self, ctx: CallbackQuery, msg: MessageSender, data: dict) -> MenuModuleHandlerCompletion:
        log.error(f"! Function in menu module does not overrided ! \nData: {data}")

    