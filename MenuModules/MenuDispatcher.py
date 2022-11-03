from operator import mod
from aiogram.types import Message, CallbackQuery

from Core.MessageSender import MessageSender
import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModules import MenuModules as menu
import MenuModules.AdminMenu.AdminMenu as adminMenu

from logger import logger as log

msg = MessageSender()

async def handleUserStart(ctx: Message):

    userTg = ctx.from_user
    log.debug(f"Did handle User{userTg.id} start message {ctx.text}")

    userInfo = storage.getUserInfo(userTg)

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
    
    # Try to find current menu module
    menuState = userInfo["state"]
    module: MenuModuleInterface = None
    completion: Completion = None
    data = {}
    try:
        menuModuleName = menuState["module"]
        module = [module.get for module in menu if module.get.name == menuModuleName][0]
        log.debug(f"Founded module: {module.name}")

    except:
        log.debug(f"Error while finding module")

    if module is not None:
        data = menuState["data"]
        completion: Completion = await module.handleUserMessage(
            ctx = ctx,
            msg=msg,
            data = data
        )

    # Start next module if needed
    moduleNext: MenuModuleInterface = None
    if completion is None:
        moduleNext = menu.mainMenu.get
    elif completion.inProgress == False:
        try:
            menuModuleName = completion.nextModuleNameIfCompleted
            moduleNext = [module.get for module in menu if module.get.name == menuModuleName][0]
            log.debug(f"Founded module: {module.name}")

        except:
            log.debug(f"Error while finding module from completion")
            moduleNext = menu.mainMenu.get

    # Emergency reboot
    if ctx.text == "Emergency reboot":
        moduleNext = menu.mainMenu.get

    if moduleNext is not None:
        module = moduleNext
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

    menuState = {
        "module": module.name,
        "data": completion.moduleData 
    }

    storage.updateUserData(userTg, userInfo)

    userInfo["state"] = menuState
    storage.updateUserData(userTg, userInfo)


async def handleCallback(ctx: CallbackQuery):

    log.debug("Did handle callback")
    
    # ctxData = json.loads(ctx.data)
    # print(ctxData)
    storage.getUserInfo(ctx.from_user)