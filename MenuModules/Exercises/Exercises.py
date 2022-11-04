from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
from pathlib import Path

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from logger import logger as log

class Exercises(MenuModuleInterface):

    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.exercises

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:

    async def handleModuleStart(self, ctx: Message, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        storage.logToUserHistory(ctx.from_user, event.startModuleExercises, "")

        keyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True
        ).add(KeyboardButton(textConstant.exercisesButtonEmotion.get)
        ).add(KeyboardButton(textConstant.exercisesButtonThought.get))

        await msg.answer(
            ctx = ctx,
            text = textConstant.exercisesStartText.get,
            keyboardMarkup = keyboardMarkup
        )

        return Completion(
            inProgress=True,
            didHandledUserInteraction=True,
            moduleData={ "startMessageDidSent" : True }
        )

    async def handleUserMessage(self, ctx: Message, msg: MessageSender, data: dict) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")

        if "startMessageDidSent" not in data or data["startMessageDidSent"] != True:
            return self.handleModuleStart(ctx, msg)
        
        messageText = ctx.text

        if "exerciseType" not in data:
            if messageText == textConstant.exercisesButtonEmotion.get:
                await msg.sendPhoto(ctx, textConstant.exercisesEmotionEmotionsListImage.get)

                keyboardMarkup=ReplyKeyboardMarkup()
                for emotionLine in emotionLinesArray:
                    buttons = []
                    for emotion in emotionLine:
                        buttons.append(KeyboardButton(emotion))
                    if len(buttons) == 2:
                        keyboardMarkup.row(buttons[0], buttons[1])
                    else:
                        keyboardMarkup.row(buttons[0])
                await msg.answer(
                    ctx=ctx,
                    text=textConstant.exercisesEmotionStartText.get,
                    keyboardMarkup=keyboardMarkup
                )

                data["exerciseType"] = "emotion"
                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )

            if messageText == textConstant.exercisesButtonThought.get:
                await msg.answer(
                    ctx=ctx,
                    text=textConstant.exercisesThoughtStartText.get,
                    keyboardMarkup=ReplyKeyboardRemove()
                )

                data["exerciseType"] = "thought"
                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )
                
            return self.canNotHandle(data)

        if "exerciseUserValue" not in data:
            data["exerciseUserValue"] = ctx.text

            answerText = ""
            if data["exerciseType"] == "emotion":
                storage.logToUserHistory(ctx.from_user, event.chooseExerciseEmotion, ctx.text)
                answerText = textConstant.exercisesEmotionScaleText.get

            if data["exerciseType"] == "thought":
                storage.logToUserHistory(ctx.from_user, event.chooseExerciseThought, ctx.text)
                answerText = textConstant.exercisesThoughtScaleText.get

            keyboardMarkup=ReplyKeyboardMarkup(
            ).row(KeyboardButton("1️⃣"), KeyboardButton("2️⃣"), KeyboardButton("3️⃣")
            ).row(KeyboardButton("4️⃣"), KeyboardButton("5️⃣"), KeyboardButton("6️⃣")
            ).row(KeyboardButton("7️⃣"), KeyboardButton("8️⃣"), KeyboardButton("9️⃣")
            ).row(KeyboardButton("🔟"), KeyboardButton("0️⃣"))

            await msg.answer(
                ctx=ctx,
                text=answerText,
                keyboardMarkup=keyboardMarkup
            )

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        if "intensityValue" not in data:
            if ctx.text in emojiNumbers:
                
                intensityValue = emojiNumbers[ctx.text]
                data["intensityValue"] = intensityValue

                exercises = {
                    "currentIndex": 0
                }
                exercisesFile: Path
                # questionsFile = storage.path.
                if data["exerciseType"] == "emotion":
                    storage.logToUserHistory(ctx.from_user, event.assessmentEmotion, f"{intensityValue}")
                    exercisesFile = storage.path.botContentEmotions

                if data["exerciseType"] == "thought":
                    storage.logToUserHistory(ctx.from_user, event.assessmentThought, f"{intensityValue}")
                    exercisesFile = storage.path.botContentEmotions

                storage.logToUserHistory(ctx.from_user, event.chooseExerciseEmotion, ctx.text)
                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )
            
            return self.canNotHandle(data)

        
        return self.canNotHandle(data)
        

    async def handleCallback(self, ctx: CallbackQuery, data: dict, msg: MessageSender) -> Completion:

        log.debug(f"User: {ctx.from_user.id}")
        log.error(f"{self.name} module does not have callbacks\nData: {data}")
        
    # =====================
    # Custom stuff
    # =====================

emotionLinesArray = [
    ["Страх", "Тревога"], 
    ["Беспомощность", "Одиночество"], 
    ["Вина", "Грусть"], 
    ["Ужас", "Беспокойство"], 
    ["Оцепенение", "Замешательство"],
    ["Гнев"]
]

emojiNumbers = {
    "0️⃣": 0,
    "1️⃣": 1,
    "2️⃣": 2,
    "3️⃣": 3,
    "4️⃣": 4,
    "5️⃣": 5,
    "6️⃣": 6,
    "7️⃣": 7,
    "8️⃣": 8,
    "9️⃣": 9,
    "🔟": 10
}