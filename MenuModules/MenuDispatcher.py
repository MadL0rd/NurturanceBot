from operator import mod
from aiogram.types import Message, CallbackQuery
import enum

from sqlalchemy import true

from Core.MessageSender import MessageSender, MessageSenderAdmin
import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event

import MenuModules.AdminMenu.AdminMenu as adminMenu
from MenuModules.Onboarding.Onboarding import Onboarding
from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion

from logger import logger as log

msgSender = MessageSenderAdmin()
msgSenderAdmin = MessageSenderAdmin()

class MenuModules(enum.Enum):

    onboarding: MenuModuleInterface = Onboarding()
    mainMenu: MenuModuleInterface = Onboarding()

    @property
    def get(self) -> MenuModuleInterface:
        return self.value

menu = MenuModules

async def handleUserStart(ctx: Message):

    userTg = ctx.from_user
    log.debug(f"Did handle User{userTg.id} start message {ctx.text}")

    userInfo = storage.getUserInfo(userTg)

    msg: MessageSender
    if "isAdmin" in userInfo and userInfo["isAdmin"] == True:
        msg = msgSender
    else:
        msg = msgSenderAdmin

    menuState = userInfo["state"]
    if not "module" in menuState:
        module: MenuModuleInterface = menu.onboarding.get
        log.debug(module.name)
        completion: Completion = await module.handleModuleStart(ctx, msg)
        if completion.inProgress == True:
            userInfo["state"] = {
                "module": module.name,
                "data": completion.moduleData 
            }
        else:
            userInfo["state"] = {}
        storage.updateUserData(userTg, userInfo)
    else:
        await handleUserMessage(ctx)
        return

async def handleUserMessage(ctx: Message):

    userTg = ctx.from_user
    log.debug(f"Did handle User{userTg.id} message: {ctx.text}")

    userInfo = storage.getUserInfo(userTg)
    menuState = userInfo["state"]

    storage.logToUserHistory(userTg, event.sendMessage, ctx.text)

    msg: MessageSender
    if "isAdmin" in userInfo and userInfo["isAdmin"] == True:
        msg = msgSenderAdmin
    else:
        msg = msgSender

    # Try to find current menu module
    menuState = userInfo["state"]
    module: MenuModuleInterface
    completion: Completion
    needToStartMenu = False
    data = {}
    try:
        menuModuleName = menuState["module"]
        module = [module.get for module in menu if module.get.name == menuModuleName][0]
        log.debug(f"Founded module: {module.name}")

    except:
        # If can nof find module redirect to main menu
        log.debug(f"Error while finding module")
        needToStartMenu = true

    if needToStartMenu == False:
        data = menuState["data"]
        completion: Completion = await module.handleUserMessage(
            ctx = ctx,
            msg=msg,
            data = data
        )
    else:
        module = menu.mainMenu.get
        menuState = {
            "module": module.name,
            "data": {}
        }
        completion: Completion = await module.handleModuleStart(
            ctx = ctx,
            msg=msg
        )

    if completion.didHandledUserInteraction == False:
        await msg.answerUnknown(ctx)

    if completion.inProgress == False:
        # If module did finished redirect to main menu
        log.debug(f"Module {module.name} completed. Start main menu")

        module = menu.mainMenu.get
        completion: Completion = await module.handleModuleStart(
            ctx = ctx,
            msg=msg
        )

    menuState = {
        "module": module.name,
        "data": completion.moduleData 
    }

    storage.updateUserData(userTg, userInfo)

    userInfo["state"] = menuState
    storage.updateUserData(userTg, userInfo)

    if "isAdmin" in userInfo and userInfo["isAdmin"] == True:
        await adminMenu.handleUserMessage(ctx)

async def handleCallback(ctx: CallbackQuery):

    log.debug("Did handle callback")
    
    # ctxData = json.loads(ctx.data)
    # print(ctxData)
    storage.getUserInfo(ctx.from_user)