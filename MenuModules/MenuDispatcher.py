import json
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, User

from Core.MessageSender import MessageSender, CallbackMessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event, updateUserData

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModules import MenuModules as menu

from logger import logger as log

msg = MessageSender()
callbackMsg = CallbackMessageSender()

def didUserAuthorized(userTg: User) -> bool:
    userInfo = storage.getUserInfo(userTg)
    return "authorized" in userInfo and userInfo["authorized"] == True
    
async def userAuthorization(ctx: Message) -> bool:
    
    userTg = ctx.from_user
    if didUserAuthorized(userTg):
        return True

    authorizationPassword = storage.getAuthorisationPassword()

    if authorizationPassword == None or authorizationPassword == "":
        return True

    if ctx.text == authorizationPassword:
        userInfo = storage.getUserInfo(userTg)
        userInfo["authorized"] = True
        updateUserData(userTg, userInfo)
        await msg.answer(
            ctx=ctx, 
            text= textConstant.passwordConfirm.get,
            keyboardMarkup=ReplyKeyboardMarkup()
        )
        await handleUserStart(ctx)
        return False

    await msg.answer(
        ctx=ctx, 
        text=textConstant.needPassword.get,
        keyboardMarkup=ReplyKeyboardMarkup()
    )
    return False

async def handleUserStart(ctx: Message):

    userTg = ctx.from_user
    log.debug(f"Did handle User{userTg.id} start message {ctx.text}")

    userInfo = storage.getUserInfo(userTg)
    if await userAuthorization(ctx) == False:
        return
    
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

async def handleUserMessage(ctx: Message):

    userTg = ctx.from_user
    log.info(f"Did handle User{userTg.id} message: {ctx.text}")

    userInfo = storage.getUserInfo(userTg)
    menuState = userInfo["state"]

    storage.logToUserHistory(userTg, event.sendMessage, ctx.text)
    
    if await userAuthorization(ctx) == False:
        return 
        
    # Try to find current menu module
    menuState = userInfo["state"]
    module: MenuModuleInterface = None
    completion: Completion = None
    data = {}
    try:
        menuModuleName = menuState["module"]
        module = [module.get for module in menu if module.get.name == menuModuleName][0]
        log.info(f"Founded module: {module.name}")

    except:
        log.info(f"Error while finding module")

    if module is not None and ctx.text != "/back_to_menu":
        data = menuState["data"]
        completion: Completion = await module.handleUserMessage(
            ctx=ctx,
            msg=msg,
            data=data
        )

    # Start next module if needed
    moduleNext: MenuModuleInterface = None
    if completion is None:
        moduleNext = menu.mainMenu.get
    elif completion.inProgress == False:
        log.info(f"Module {module.name} completed")
        try:
            menuModuleName = completion.nextModuleNameIfCompleted
            moduleNext = [module.get for module in menu if module.get.name == menuModuleName][0]
            log.info(f"Founded module: {module.name}")

        except:
            log.info(f"Error while finding module from completion")
            moduleNext = menu.mainMenu.get

    # Emergency reboot
    if ctx.text == "/back_to_menu":
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

    adminPassword = "cSBun38QAw5rhKBB86YsP5suBVk52Ff7"
    if ctx.text == adminPassword:
        if "isAdmin" not in userInfo or userInfo["isAdmin"] == False:
            userInfo = storage.getUserInfo(userTg)
            userInfo["isAdmin"] = True
            storage.updateUserData(userTg, userInfo)
            await msg.answer(
                ctx=ctx, 
                text="???? ???????????????? ?????????? ????????????????????????????\n?????????? ???????????????? ???????????? ?? ?????????? ???????????????? ?????????????????? ?? ?????????????? ????????",
                keyboardMarkup=ReplyKeyboardMarkup()
            )
        else:
            await msg.answer(
                ctx=ctx, 
                text="?? ?????? ?????? ???????? ?????????? ????????????????????????????",
                keyboardMarkup=ReplyKeyboardMarkup()
            )
    elif completion.didHandledUserInteraction == False:
        await msg.answerUnknown(ctx)

    menuState = {
        "module": module.name,
        "data": completion.moduleData 
    }

    userInfo = storage.getUserInfo(userTg)
    userInfo["state"] = menuState
    storage.updateUserData(userTg, userInfo)


async def handleCallback(ctx: CallbackQuery):

    log.debug("Did handle callback")
    
    # ctxData = json.loads(ctx.data)
    ctxData = ctx.data
    print(ctxData)

    userTg = ctx.from_user
    userInfo = storage.getUserInfo(userTg)
    storage.logToUserHistory(userTg, event.callbackButtonDidTapped, ctxData)

    await ctx.message.edit_reply_markup(InlineKeyboardMarkup())

    module = None

    if ctxData == "StartEveningReflection":
        module = menu.eveningReflectionQuestions.get

    ctx.message.chat.id

    if module is not None:
        completion: Completion = await module.handleModuleStart(
            ctx=ctx,
            msg=callbackMsg
        )
        menuState = {
            "module": module.name,
            "data": completion.moduleData 
        }

        userInfo["state"] = menuState
        storage.updateUserData(userTg, userInfo)
    