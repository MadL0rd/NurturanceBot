
import enum
import Core.StorageManager.StorageManager as storage 

class UniqueMessagesKeys(enum.Enum):

    unknownState = "unknownState"

    menuButtonReturnToMainMenu = "menuButtonReturnToMainMenu"

    mainMenuText = "mainMenuText"
    menuButtonExercises = "menuButtonExercises"
    menuButtonRandomNews = "menuButtonRandomNews"
    menuButtonRelax = "menuButtonRelax"
    menuButtonAdmin = "menuButtonAdmin"

    adminMenuText = "adminMenuText"
    adminMenuButtonLoadData = "adminMenuButtonLoadData"
    adminMenuButtonReloadData = "adminMenuButtonReloadData"

    randomNewsStartText = "randomNewsStartText"
    randomNewsButtonNews = "randomNewsButtonNews"
    randomNewsAllNewsWasShown = "randomNewsAllNewsWasShown"

    exercisesStartText = "exercisesStartText"
    exercisesButtonThought = "exercisesButtonThought"
    exercisesButtonEmotion = "exercisesButtonEmotion"

    exercisesEmotionStartText = "exercisesEmotionStartText"
    exercisesThoughtStartText = "exercisesThoughtStartText"
    exercisesEmotionEmotionsListImage = "exercisesEmotionEmotionsListImage"
    exercisesEmotionScaleText = "exercisesEmotionScaleText"
    exercisesThoughtScaleText = "exercisesThoughtScaleText"
    exercisesButtonComplete = "exercisesButtonComplete"
    exercisesScaleTextComplete = "exercisesScaleTextComplete"
    exercisesCompleteText = "exercisesCompleteText"
    exercisesSessionCompleteText = "exercisesSessionCompleteText"
    exercisesButtonSessionReload = "exercisesButtonSessionReload"
    exercisesButtonSessionEnd = "exercisesButtonSessionEnd"
    notificationMorningText = "notificationMorningText"
    notificationDayText = "notificationDayText"
    notificationEveningText = "notificationEveningText"

    @property
    def get(self) -> str:
        messagesKeys = storage.getJsonData(storage.path.botContentUniqueMessages)
        if self.value in messagesKeys:
            return messagesKeys[self.value]
        else:
            return "Unknown"

textConstant = UniqueMessagesKeys
