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

# =====================
# Base
# =====================

class UserHistoryEvent(enum.Enum):

    start = "Старт"
    sendMessage = "Отправил сообщение"
    becomeAdmin = "Стал администратором"
    startModuleOnboarding = "Начал смотреть онбординг"
    startModuleMainMenu = "Перешел в главное меню" 
    startModuleNews =  "Запросил новость"
    startModuleTaskEmotions = 'Запросил упражнение по эмоциям'
    startModuleTaskThoughts = 'Запросил упражнение по мыслям'


class PathConfig:

    baseDir = Path("./DataStorage")

    usersDir = baseDir / "Users"

    botContentDir = baseDir / "BotContent"
    botContentOnboarding = botContentDir/ "Onboarding.json"
    botContentUniqueMessages = botContentDir/ "UniqueTextMessages.json"
    botContentPrivateConfig = botContentDir / "PrivateConfig.json"
    botContentNews = botContentDir / "News.json"
    botContentEmotions = botContentDir / "Emotions.json"
    botContentThoughts = botContentDir / "Thoughts.json"

    totalHistoryTableFile = baseDir / "TotalHistory.xlsx"
    statisticHistoryTableFile = baseDir / "StatisticalHistory.xlsx"

    def userFolder(self, user: User):
        return self.usersDir / f"{user.id}"

    def userInfoFile(self, user: User):
        return self.userFolder(user) / "info.json"
    
    def userHistoryFile(self, user: User):
        return self.userFolder(user) / "history.json"

path = PathConfig()

def getJsonData(filePath: Path):
    with filePath.open() as json_file:
        data = json.load(json_file)
    return data

def writeJsonData(filePath: Path, content):
    # log.debug(content)
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

def generateUserStorage(user: User):

    userFolder = path.userFolder(user)
    userFolder.mkdir(parents=True, exist_ok=True)
    
    userData = json.loads(user.as_json())
    userData = {
        "info": userData,
        "isAdmin": False,
        "state": {}
    }

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
        UserHistoryEvent.sendMessage
    ]

    dateConfig = getJsonData(path.botContentPrivateConfig)["startDate"]
    startDate = date(dateConfig["year"], dateConfig["month"], dateConfig["day"])

    workbook = xlsxwriter.Workbook(path.statisticHistoryTableFile)

    for event in statisticEvents:
        generateStatisticPageForEvent(workbook, event.value, startDate)

    workbook.close()

    log.info("Statistic table generation completed")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)

def generateStatisticPageForEvent(workbook: xlsxwriter.Workbook, eventName: string, startDate: date):

    worksheet = workbook.add_worksheet(eventName)
    row = 0 
    col = 0

    worksheet.write(row, col, "Дата / Пользователь")
    row += 1

    dates = [strDate.strftime("%d.%m.%Y") for strDate in daterange(startDate, date.today())]
    for single_date in dates:
        worksheet.write(row, col, single_date)
        row += 1
    col += 1

    usersCount = 0
    for userFolder in path.usersDir.iterdir():
        usersCount += 1
        row = 0
        history = getJsonData(userFolder / "history.json")
        
        columnTitle = f"user{userFolder.name}"
        worksheet.write(row, col, columnTitle)
        
        row = 1
        for single_date in dates:
            dateEventsCount = len([event for event in history if event["timestamp"]["date"] == single_date and event["event"] == eventName])
            worksheet.write(row, col, dateEventsCount)
            row += 1

        col += 1

    worksheet.set_column(0, usersCount, 15)

def generateTotalTable():
    log.info("Total table generation start")

    workbook = xlsxwriter.Workbook(path.totalHistoryTableFile)
    bold = workbook.add_format({'bold': True})

    for userFolder in path.usersDir.iterdir():
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