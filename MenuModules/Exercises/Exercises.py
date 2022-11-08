import random
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

        # Choose exercise type if needed
        if "exerciseType" not in data:
            if messageText == textConstant.exercisesButtonEmotion.get:
                await msg.sendPhoto(ctx, textConstant.exercisesEmotionEmotionsListImage.get)

                keyboardMarkup=ReplyKeyboardMarkup(
                    resize_keyboard=True
                )
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

        # Enter emotion or thought
        if "exerciseUserValue" not in data:
            data["exerciseUserValue"] = ctx.text

            answerText = ""
            if data["exerciseType"] == "emotion":
                storage.logToUserHistory(ctx.from_user, event.chooseExerciseEmotion, ctx.text)
                answerText = textConstant.exercisesEmotionScaleText.get

            if data["exerciseType"] == "thought":
                storage.logToUserHistory(ctx.from_user, event.chooseExerciseThought, ctx.text)
                answerText = textConstant.exercisesThoughtScaleText.get

            await sendAssessmentMessage(ctx, msg, answerText)

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        # Emotion or thought intensity
        if "intensityValue" not in data:
            if ctx.text in emojiNumbers:
                
                intensityValue = emojiNumbers[ctx.text]
                data["intensityValue"] = intensityValue
                storage.logToUserHistory(ctx.from_user, event.assessmentBefore, f"{intensityValue}")

                exercises = {
                    "currentIndex": 0,
                    "content": []
                }
                exercisesFile = storage.path.botContentEmotions
                questionsFile = storage.path.botContentQuestions
                if data["exerciseType"] == "emotion":
                    exercisesFile = storage.path.botContentEmotions
                if data["exerciseType"] == "thought":
                    exercisesFile = storage.path.botContentThoughts

                if intensityValue > 4:
                    exercises["content"] = [
                        {
                            "type": "exercise",
                            "value": random.choice(storage.getJsonData(exercisesFile))
                        },
                        {
                            "type": "exercise",
                            "value": random.choice(storage.getJsonData(exercisesFile))
                        }
                    ]
                else:
                    exercises["content"] = [
                        {
                            "type": "exercise",
                            "value": random.choice(storage.getJsonData(exercisesFile))
                        },
                        {
                            "type": "question",
                            "value": random.choice(storage.getJsonData(questionsFile))
                        }
                    ]

                await showExercise(ctx, msg, exercises["content"][0])

                data["exercises"] = exercises
                
                historyText = f"{data['exerciseType']}\n"
                for item in data["exercises"]["content"]:
                    historyText += f"Тип: {item['type']}; ID: {item['value']['ID']}\n"
                storage.logToUserHistory(ctx.from_user, event.sessionGenerated, historyText)

                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )
            
            return self.canNotHandle(data)

        currentIndex = data["exercises"]["currentIndex"]
        item = data["exercises"]["content"][currentIndex]

        if item["type"] == "exercise" and ctx.text == textConstant.exercisesButtonComplete.get:
            currentIndex += 1
            if len(data["exercises"]["content"]) > currentIndex:
                item = data["exercises"]["content"][currentIndex]
                data["exercises"]["currentIndex"] = currentIndex
                await showExercise(ctx, msg, item)
                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )
            else:
                answerText = textConstant.exercisesScaleTextComplete.get
                await sendAssessmentMessage(ctx, msg, answerText)

                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )

        if item["type"] == "question" and "userQuestionAnswer" not in data:
            storage.logToUserHistory(ctx.from_user, event.questionAnswer, ctx.text)
            answerText = textConstant.exercisesScaleTextComplete.get
            await sendAssessmentMessage(ctx, msg, answerText)
            data["userQuestionAnswer"] = ctx.text

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        if "intensityValueAfter" not in data:
            if ctx.text in emojiNumbers:
                intensityValueAfter = emojiNumbers[ctx.text]
                data["intensityValueAfter"] = intensityValueAfter
                storage.logToUserHistory(ctx.from_user, event.assessmentAfter, f"{intensityValueAfter}")
                delta = data["intensityValue"] - intensityValueAfter
                storage.logToUserHistory(ctx.from_user, event.assessmentDelta, f"{delta}")
                
                keyboardMarkup = ReplyKeyboardMarkup(
                    resize_keyboard=True
                ).add(KeyboardButton(textConstant.exercisesButtonSessionReload.get)
                ).add(KeyboardButton(textConstant.exercisesButtonSessionEnd.get))
                await msg.answer(ctx, textConstant.exercisesSessionCompleteText.get, keyboardMarkup)

                return Completion(
                    inProgress=True,
                    didHandledUserInteraction=True,
                    moduleData=data
                )
            
            return self.canNotHandle(data)

        if ctx.text == textConstant.exercisesButtonSessionReload.get:
            historyText = f"{data['exerciseType']}\n"
            for item in data["exercises"]["content"]:
                historyText += f"Тип: {item['type']}; ID: {item['value']['ID']}\n"
            storage.logToUserHistory(ctx.from_user, event.sessionReload, historyText)

            await showExercise(ctx, msg, data["exercises"]["content"][0])
            data["exercises"]["currentIndex"] = 0
            data["intensityValue"] = data["intensityValueAfter"]
            if "intensityValueAfter" in data:
                del data["intensityValueAfter"]
            if "userQuestionAnswer" in data:
                del data["userQuestionAnswer"]

            return Completion(
                inProgress=True,
                didHandledUserInteraction=True,
                moduleData=data
            )

        if ctx.text == textConstant.exercisesButtonSessionEnd.get:
            return self.complete(nextModuleName=MenuModuleName.mainMenuNewSession.get)
        
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

async def sendAssessmentMessage(ctx: Message, msg: MessageSender, text: str):

    keyboardMarkup=ReplyKeyboardMarkup(
        resize_keyboard=True
    ).row(KeyboardButton("1️⃣"), KeyboardButton("2️⃣"), KeyboardButton("3️⃣")
    ).row(KeyboardButton("4️⃣"), KeyboardButton("5️⃣"), KeyboardButton("6️⃣")
    ).row(KeyboardButton("7️⃣"), KeyboardButton("8️⃣"), KeyboardButton("9️⃣")
    ).row(KeyboardButton("🔟"), KeyboardButton("0️⃣"))

    await msg.answer(
        ctx=ctx,
        text=text,
        keyboardMarkup=keyboardMarkup
    )

async def showExercise(ctx: Message, msg: MessageSender, itemDict: dict):
    keyboardMarkup=ReplyKeyboardMarkup(
        resize_keyboard=True
    ).add(KeyboardButton(textConstant.exercisesButtonComplete.get))
    if itemDict["type"] == "question":
        keyboardMarkup = ReplyKeyboardRemove()
    
    item = itemDict["value"]
    if "text" in item:
        await msg.answer(ctx, item["text"], keyboardMarkup)
    if "picture" in item:
        await msg.sendPhoto(ctx, item["picture"])
    if "audio" in item:
        await msg.sendAudio(ctx, item["audio"])
    if "video" in item:
        await msg.sendVideo(ctx, item["video"])