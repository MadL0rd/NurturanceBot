from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.Utils.Utils as utils

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class Quiz(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.quiz
    nextModuleName = MenuModuleName.mainMenu.get

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleQuiz, "")

        await msg.answer(
            ctx = ctx,
            text = str(self.getStartMessageText()),
            keyboardMarkup = ReplyKeyboardRemove()
        )
        
        return await self.handleUserMessage(
            ctx = ctx,
            msg = msg,
            data =
            {
                "sumOfScores": 0,
                "final": False
            }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        
        messageText = ctx.text
        pull = self.getQuizData()
        questionIndex = 0
        if "prevQuestionIndex" in data and data["prevQuestionIndex"] < len(pull):
            prevQuestionIndex = data["prevQuestionIndex"]
            prevQuestion = pull[prevQuestionIndex]
            prevQuestionButtons = prevQuestion["buttons"]
            pressedButtons = [button for button in prevQuestionButtons if button["text"] == messageText] 
            if len(pressedButtons) > 0:
                button = pressedButtons[0]
                data["sumOfScores"] = data["sumOfScores"] + int(button["score"])
                questionIndex = prevQuestionIndex + 1
                data["prevQuestionIndex"] = questionIndex
            else:
                return self.canNotHandle(data)
        
        if questionIndex < len(pull) and data["final"] == False:
            question = pull[questionIndex]           
            listOfVariants = [button["text"] for button in question["buttons"]]
            keyboardMarkup = utils.replyMarkupFromListOfButtons(listOfVariants, twoColumns = False)
            await msg.answer(
                ctx = ctx,
                text = question["title"],
                keyboardMarkup = keyboardMarkup
            )
            data["prevQuestionIndex"] = questionIndex
            data["currentQuestion"] = question
            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )
            
        if data["final"] == False:
            pullResults = self.getQuizResults()
            foundResult = None
            # TODO: Naming fix
            for result in pullResults:
                if int(result["rLimit"]) >= data["sumOfScores"] and int(result["lLimit"]) <= data["sumOfScores"]:
                    text = result["text"]
                    keyboardMarkup = ReplyKeyboardMarkup().add(KeyboardButton(result["button"]))
                    foundResult = result
            await msg.answer(
                ctx = ctx,
                text = text,
                keyboardMarkup = keyboardMarkup
            )
            data["final"] = True
            data["finalButtonText"] = foundResult["button"]
            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        if data["final"] == True and data["finalButtonText"] and messageText == data["finalButtonText"]:
            return self.complete(nextModuleName = MenuModuleName.mainMenu.get)

        return self.canNotHandle(data)
       
    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================
    def getQuizData(self) -> list:
        return []      
    def getQuizResults(self) -> list:
        return []
    def getStartMessageText(self) -> str:
        return ""