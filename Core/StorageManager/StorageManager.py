from datetime import datetime, date, timedelta
from email.policy import strict
import enum
import json
from pathlib import Path
import string
import pytz
import xlsxwriter

from aiogram.types import User

from logger import logger as log

from Core.Utils import Utils as utils

# =====================
# Base
# =====================

class UserHistoryEvent(enum.Enum):

    start = "Старт"
    sendMessage = "Отправил сообщение"
    callbackButtonDidTapped = "Нажал на кнопку в сообщении"
    becomeAdmin = "Стал администратором"
    startModuleOnboarding = "Начал смотреть онбординг"
    startModuleMainMenu = "Перешел в главное меню" 
    startModuleNews =  "Запросил новость"
    startModuleExercises =  "Перешел к упражнениям"
    startModuleEveningReflectionQuestions = "Приступил к вечерней рефлексии"
    startModuleFairytale = "Приступил к написанию сказки"
    startModuleOtherHuman = "Перешел к проработке отношений с другим человеком"
    chooseExerciseEmotion =  "Начал прорабатывать эмоцию"
    chooseExerciseThought =  "Начал прорабатывать мысль"
    assessmentBefore = "Оценил до"
    assessmentAfter = "Оценил после"
    assessmentDelta = "Разница оценок до и после"
    questionAnswer = "Ответил на вопрос"
    sessionGenerated = "Сессия создана"
    sessionReload = "Перезапустил сессию"
    sessionComplete = "Завершил сессию"
    notificationChooseTime = "Передвинул время уведомлений"
    startModuleTestMenu = "Зашёл в меню выбора тестов"
    startModuleQuiz = "Запустил тест"
    otherHumanSessionSuccessYes = "ПоработалСЧеловеком Удачно"
    otherHumanSessionSuccessNo = "ПоработалСЧеловеком Неудачно"

class PathConfig:

    baseDir = Path("./DataStorage")
        
    internalDir = baseDir / "Internal"
    botContentPrivateConfig = internalDir / "PrivateConfig.json"
    botContentNotificationTimes = internalDir / "NotificationTimes.json"

    usersDir = baseDir / "Users"

    botContentDir = baseDir / "BotContent"
    botContentOnboarding = botContentDir/ "Onboarding.json"
    botContentUniqueMessages = botContentDir/ "UniqueTextMessages.json"
    botContentNews = botContentDir / "News.json"
    botContentEmotions = botContentDir / "Emotions.json"
    botContentThoughts = botContentDir / "Thoughts.json"
    botContentQuestions = botContentDir / "Questions.json"
    botContentEveningReflectionQuestions = botContentDir / "EveningReflectionQuestions.json"
    botContentFairytale = botContentDir / "Fairytale.json"
    botContentOtherHuman = botContentDir / "OtherHuman.json"
    botContentQuizDepression = botContentDir / "QuizDepression.json"
    botContentQuizDepressionResults = botContentDir / "QuizDepressionResults.json"
    botContentQuizAnxiety = botContentDir / "QuizAnxiety.json"
    botContentQuizAnxietyResults = botContentDir / "QuizAnxietyResults.json"
    botContentAuthorizationPassword = botContentDir / "AuthorizationPassword.json"

    totalHistoryTableFile = baseDir / "TotalHistory.xlsx"
    statisticHistoryTableFile = baseDir / "StatisticalHistory.xlsx"
    specHistoryTableFile = baseDir / "SpecHistory.xlsx"

    @property
    def userFoldersAll(self) -> list:
        return [userFolder for userFolder in self.usersDir.iterdir() if userFolder.is_dir()]

    def userFolder(self, user: User):
        return self.usersDir / f"{user.id}"

    def userInfoFile(self, user: User):
        return self.userFolder(user) / "info.json"
    
    def userNewsFile(self, user: User):
        return self.userFolder(user) / "news.json"

    def userHistoryFile(self, user: User):
        return self.userFolder(user) / "history.json"

path = PathConfig()

def getJsonData(filePath: Path):
    with filePath.open() as json_file:
        data = json.load(json_file)
    return data

def writeJsonData(filePath: Path, content):
    if utils.isWindows:
        data = json.dumps(content, indent=2)
        with filePath.open('w', encoding= 'utf-8') as file:
            file.write(data)
    else:
        data = json.dumps(content, ensure_ascii=False, indent=2)
        with filePath.open('w') as file:
            file.write(data)

# =====================
# Public interaction
# =====================

def getUserInfo(user: User):
    
    userInfoFile = path.userInfoFile(user)

    # If user file does not exist
    if not userInfoFile.exists():
        log.info(f"User {user.id} dir does not exist")
        generateUserStorage(user)

    userInfoFile = path.userInfoFile(user)

    return getJsonData(userInfoFile)

def getUserNews(user: User)->list: 
    
    userNewsFile = path.userNewsFile(user)

    # If user file does not exist
    if not userNewsFile.exists():
        log.info(f"User {user.id} dir does not exist")
        generateUserStorage(user)

    userNewsFile = path.userNewsFile(user)

    return getJsonData(userNewsFile)

def generateUserStorage(user: User):

    userFolder = path.userFolder(user)
    userFolder.mkdir(parents=True, exist_ok=True)

    notoficationsConfig = getJsonData(path.botContentNotificationTimes)
    
    userData = json.loads(user.as_json())
    userData = {
        "info": userData,
        "isAdmin": False,
        "state": {},
        "notifications": notoficationsConfig["userDefault"]
    }
    updateUserNews(user,[])
    updateUserData(user, userData)
    logToUserHistory(user, UserHistoryEvent.start, "Начало сохранения истории пользователя")

def getTimestamp():

    tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz)
    return {
        "date": now.strftime("%d.%m.%Y"),
        "time": now.strftime("%H:%M:%S"),
        "week": now.isocalendar()[1]
    }

def updateUserData(user: User, userData):
    
    userInfoFile = path.userInfoFile(user)
    userData["updateTime"] = getTimestamp()
    writeJsonData(userInfoFile, userData)

def updateUserNews(user: User, userNews):
    
    userNewsFile = path.userNewsFile(user)
    writeJsonData(userNewsFile, userNews)

def logToUserHistory(user: User, event: UserHistoryEvent, content: string):

    log.info(f"{user.id} {event.value}: {content}")

    historyFile = path.userHistoryFile(user)

    history = []
    if historyFile.exists():
        history = getJsonData(historyFile)
    
    history.append({
        "timestamp": getTimestamp(),
        "event": event.value,
        "content": content
    })

    writeJsonData(historyFile, history)

# =====================
# Data tables creation
# =====================

def generateStatisticTable():

    log.info("Statistic table generation start")

    statisticEvents = [
        UserHistoryEvent.start,
        UserHistoryEvent.startModuleExercises,
        UserHistoryEvent.chooseExerciseEmotion,
        UserHistoryEvent.chooseExerciseThought,
        UserHistoryEvent.questionAnswer,
        UserHistoryEvent.sessionGenerated,
        UserHistoryEvent.sessionReload,
        UserHistoryEvent.sessionComplete,
        UserHistoryEvent.notificationChooseTime,
        UserHistoryEvent.otherHumanSessionSuccessYes,
        UserHistoryEvent.otherHumanSessionSuccessNo
    ]

    dateConfig = getJsonData(path.botContentPrivateConfig)["startDate"]
    startDate = date(dateConfig["year"], dateConfig["month"], dateConfig["day"])

    workbook = xlsxwriter.Workbook(path.statisticHistoryTableFile)

    event = UserHistoryEvent.assessmentDelta
    generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.sum)

    event = UserHistoryEvent.assessmentBefore
    generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.average)
    event = UserHistoryEvent.assessmentAfter
    generateStatisticPageForEvent(workbook, event.value, startDate, StatisticPageOperation.average)

    for event in statisticEvents:
        generateStatisticPageForEvent(workbook, event.value, startDate)

    workbook.close()

    log.info("Statistic table generation completed")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

class StatisticPageOperation(enum.Enum):
    count = "Количество"
    sum = "Сумма"
    average = "Среднее значение"

def generateStatisticPageForEvent(workbook: xlsxwriter.Workbook, eventName: string, startDate: date, operation: StatisticPageOperation = StatisticPageOperation.count):

    worksheet = workbook.add_worksheet(eventName)
    row = 1
    col = 0

    startRow = 4

    worksheet.write(row, col, "Метрика:")
    worksheet.write(row, col + 1, eventName)
    row += 1
    worksheet.write(row, col, "Тип агрегирования:")
    worksheet.write(row, col + 1, operation.value)

    row = startRow
    worksheet.write(row, col, "Дата / Пользователь")
    row += 1

    dates = [strDate.strftime("%d.%m.%Y") for strDate in daterange(startDate, date.today())]
    for single_date in dates:
        worksheet.write(row, col, single_date)
        row += 1
    col += 1

    usersCount = 0
    for userFolder in path.userFoldersAll:
        usersCount += 1
        row = startRow
        history = getJsonData(userFolder / "history.json")
        
        columnTitle = f"user{userFolder.name}"
        worksheet.write(row, col, columnTitle)
        
        row += 1
        for single_date in dates:
            dayEvents = [event for event in history if event["timestamp"]["date"] == single_date and event["event"] == eventName]

            if operation == StatisticPageOperation.count:
                dateEventsCount = len(dayEvents)
                worksheet.write(row, col, dateEventsCount)

            if operation == StatisticPageOperation.sum:
                try:
                    values = [int(event["content"]) for event in dayEvents]
                except:
                    values = []
                worksheet.write(row, col, sum(values))

            if operation == StatisticPageOperation.average:
                try:
                    values = [int(event["content"]) for event in dayEvents]
                    result = sum(values) / len(values)
                except:
                    result = 0
                worksheet.write(row, col, result)

            row += 1

        col += 1

    worksheet.set_column(0, usersCount, 15)

def generateTotalTable():
    log.info("Total table generation start")

    workbook = xlsxwriter.Workbook(path.totalHistoryTableFile)
    bold = workbook.add_format({'bold': True})

    for userFolder in path.userFoldersAll:
        sheetTitle = f"user{userFolder.name}"
        
        worksheet = workbook.add_worksheet(sheetTitle)
        row = 0 

        titles = ["Дата", "Время", "Неделя", "Событие", "Описание"]
        for col, title in enumerate(titles):
            worksheet.write(row, col, title, bold)
            worksheet.set_column(col, col, len(title))
        worksheet.set_column(4, 4, 50)

        history = getJsonData(userFolder / "history.json")

        row = 1
        for event in history:
            col = 0
            worksheet.write(row, col, event["timestamp"]["date"])
            col += 1
            worksheet.write(row, col, event["timestamp"]["time"])
            col += 1
            worksheet.write(row, col, event["timestamp"]["week"])
            col += 1
            worksheet.write(row, col, event["event"])
            col += 1
            worksheet.write(row, col, event["content"])
            row += 1

    workbook.close()

    log.info("Total table generation completed")

def generateSpecTable():
    log.info("Spec table generation start")

    # Lits for necessary events in Special Table
    if utils.isWindows == True:
        # Because we have some problems with encoding on Windows
        specEventList = [
            "\u041f\u0435\u0440\u0435\u0448\u0435\u043b \u043a \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f\u043c",
            "\u041f\u0440\u0438\u0441\u0442\u0443\u043f\u0438\u043b \u043a \u0432\u0435\u0447\u0435\u0440\u043d\u0435\u0439 \u0440\u0435\u0444\u043b\u0435\u043a\u0441\u0438\u0438",
            "\u041d\u0430\u0447\u0430\u043b \u043f\u0440\u043e\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0442\u044c \u044d\u043c\u043e\u0446\u0438\u044e",
            "\u041d\u0430\u0447\u0430\u043b \u043f\u0440\u043e\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0442\u044c \u043c\u044b\u0441\u043b\u044c",
            "\u041e\u0446\u0435\u043d\u0438\u043b \u0434\u043e",
            "\u041e\u0446\u0435\u043d\u0438\u043b \u043f\u043e\u0441\u043b\u0435",
            "\u0420\u0430\u0437\u043d\u0438\u0446\u0430 \u043e\u0446\u0435\u043d\u043e\u043a \u0434\u043e \u0438 \u043f\u043e\u0441\u043b\u0435"
        ]
    else:
        specEventList = [
            UserHistoryEvent.startModuleExercises,
            UserHistoryEvent.startModuleEveningReflectionQuestions,
            UserHistoryEvent.chooseExerciseEmotion,
            UserHistoryEvent.chooseExerciseThought,
            UserHistoryEvent.assessmentBefore,
            UserHistoryEvent.assessmentAfter,
            UserHistoryEvent.assessmentDelta
        ]

    workbook = xlsxwriter.Workbook(path.specHistoryTableFile) # workbook creation
    bold = workbook.add_format({'bold': True})
    sheetTitle = "Page"
    worksheet = workbook.add_worksheet(sheetTitle)
    row = 1

    titles = ["Дата", "Время", "Неделя", "Событие", "Описание", "id пользователя"] # column naming
    for col, title in enumerate(titles):
        worksheet.write(row, col, title, bold)
        worksheet.set_column(col, col, len(title))
    worksheet.set_column(4, 4, 50)
    row += 1

    eventList = [] # empty list for necessary events
    for userFolder in path.userFoldersAll:
        history = getJsonData(userFolder / "history.json")
        for event in history:
            if event["event"] in specEventList:
                event["userId"] = userFolder.name # adding id to the event dict
                eventList.append(event)

    sortedEventList = sorted(eventList, key= lambda d: (d["timestamp"]["date"], d["timestamp"]["time"])) # sorting by date and time

    for event in sortedEventList: # table writing
        if event["event"] in specEventList:
            col = 0
            worksheet.write(row, col, event["timestamp"]["date"])
            col += 1
            worksheet.write(row, col, event["timestamp"]["time"])
            col += 1
            worksheet.write(row, col, event["timestamp"]["week"])
            col += 1
            worksheet.write(row, col, event["event"])
            col += 1
            worksheet.write(row, col, event["content"])
            col += 1
            worksheet.write(row, col, event["userId"])
            row += 1

    workbook.close()

    log.info("Spec table generation completed")

def getAuthorisationPassword() -> str:
    try:
        authorizationPasswordGet = getJsonData(PathConfig.botContentAuthorizationPassword)
        authorizationPassword = authorizationPasswordGet["password"]
        return authorizationPassword
    except:
        setAuthorisationPassword("")
        return ""
   

def setAuthorisationPassword(password: str):
    writeJsonData(
        filePath=path.botContentAuthorizationPassword,
        content= {
            "password": password
        }
    )