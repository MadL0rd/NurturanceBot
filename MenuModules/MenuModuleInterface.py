from unicodedata import name
from aiogram.types import Message, CallbackQuery
import enum
import json
from Core.MessageSender import MessageSender
from MenuModules.MenuModuleName import MenuModuleName

from logger import logger as log

class MenuModuleHandlerCompletion:

    inProgress: bool
    didHandledUserInteraction: bool
    moduleData: dict
    nextModuleNameIfCompleted: str

    def __init__(self, inProgress: bool, didHandledUserInteraction: bool, moduleData: dict = {}, nextModuleNameIfCompleted: str = ""):
        self.inProgress = inProgress
        self.didHandledUserInteraction = didHandledUserInteraction
        self.moduleData = moduleData
        self.nextModuleNameIfCompleted = nextModuleNameIfCompleted

class MenuModuleInterface:

    namePrivate: MenuModuleName

    @property
    def name(self) -> str:
        return self.namePrivate.value

    def callbackData(self, data: dict, msg: MessageSender) -> str:
        data = {
            "module": self.name,
            "data": data
        }
        return json.dumps(data)

    def canNotHandle(self, data: dict) -> MenuModuleHandlerCompletion:
        return MenuModuleHandlerCompletion(
            inProgress=True,
            didHandledUserInteraction=False,
            moduleData=data
        )

    def complete(self, nextModuleName: str = "") -> MenuModuleHandlerCompletion:
        return MenuModuleHandlerCompletion(
            inProgress=False,
            didHandledUserInteraction=True,
            moduleData={},
            nextModuleNameIfCompleted=nextModuleName
        )

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> MenuModuleHandlerCompletion:
        log.error("! Function in menu module does not overrided !")

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> MenuModuleHandlerCompletion:
        log.error(f"! Function in menu module does not overrided !\nData: {data}")

    async def handleCallback(self, ctx: CallbackQuery, msg: MessageSender, data: dict) -> MenuModuleHandlerCompletion:
        log.error(f"! Function in menu module does not overrided ! \nData: {data}")

    