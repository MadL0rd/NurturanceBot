from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

import Core.StorageManager.StorageManager as storage
from Core.StorageManager.StorageManager import UserHistoryEvent as event
from Core.MessageSender import MessageSender
from Core.StorageManager.UniqueMessagesKeys import textConstant
import Core.Utils.Utils as utils

from MenuModules.MenuModuleInterface import MenuModuleInterface, MenuModuleHandlerCompletion as Completion
from MenuModules.MenuModuleName import MenuModuleName
from MenuModules.Quiz.Quiz import Quiz
from logger import logger as log

class QuizAnxiety(Quiz):
    # =====================
    # Interface implementation
    # =====================

    namePrivate = MenuModuleName.quizAnxiety
    nextModuleName = MenuModuleName.mainMenu.get
    
    @property
    def startMessageText(self):
        return textConstant.quizAnxietyStart.get

    # Use default implementation
    # def callbackData(self, data: dict, msg: MessageSender) -> str:
    def getQuizData(self) -> list:
        return storage.getJsonData(storage.PathConfig.botContentQuizAnxiety)

    def getQuizResults(self) -> list:
        return storage.getJsonData(storage.PathConfig.botContentQuizAnxietyResults)

    def getStartMessageText(self) -> str:
        return textConstant.quizAnxietyStart.get