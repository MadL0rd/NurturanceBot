
import enum
import Core.StorageManager.StorageManager as storage 

class UniqueMessagesKeys(enum.Enum):

    unknownState = "unknownState"

    menuButtonReturnToMainMenu = "menuButtonReturnToMainMenu"

    mainMenuText = "mainMenuText"
    menuButtonExercises = "menuButtonExercises"
    menuButtonRandomNews = "menuButtonRandomNews"
    menuButtonRelax = "menuButtonRelax"
    menuButtonQuizDepression = "menuButtonQuizDepression"
    menuButtonQuizAnxiety = "menuButtonQuizAnxiety"
    menuButtonAdmin = "menuButtonAdmin"
    menuButtonStartNewSession = "menuButtonStartNewSession"
    menuTextStartNewSession = "menuTextStartNewSession"
    menuButtonNotifications = "menuButtonNotifications"

    adminMenuText = "adminMenuText"
    adminMenuButtonLoadData = "adminMenuButtonLoadData"
    adminMenuButtonReloadData = "adminMenuButtonReloadData"
    adminMenuButtonEveningReflectionStart = "adminMenuButtonEveningReflectionStart"

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
    exercisesSessionCompleteText = "exercisesSessionCompleteText"
    exercisesButtonSessionReload = "exercisesButtonSessionReload"
    exercisesButtonSessionEnd = "exercisesButtonSessionEnd"
    
    notificationMorningText = "notificationMorningText"
    notificationDayText = "notificationDayText"
    notificationEveningText = "notificationEveningText"
    notificationSettingsText = "notificationSettingsText"

    relaxStartMessage = "relaxStartMessage"
    relaxCompleteMessage = "relaxCompleteMessage"
  
    quizDepressionStart = "quizDepressionStart"
    quizAnxietyStart = "quizAnxietyStart"
    reflectionMenuText = "reflectionMenuText"
    reflectionMenuButtonFairytale = "reflectionMenuButtonFairytale"
    reflectionMenuButtonOtherHuman = "reflectionMenuButtonOtherHuman"

    otherHumanEnding = "otherHumanEnding"
    otherHumanButtonSessionSuccessYes = "otherHumanButtonSessionSuccessYes"
    otherHumanButtonSessionSuccessNo = "otherHumanButtonSessionSuccessNo"
    otherHumanWhatsNext = "otherHumanWhatsNext"
    otherHumanButtonRestart = "otherHumanButtonRestart"
    otherHumanButtonEndSession = "otherHumanButtonEndSession"
    otherHumanButtonWriteFairytale = "otherHumanButtonWriteFairytale"

    fairytaleStart = "fairytaleStart"
    fairytaleButtonStart = "fairytaleButtonStart"
    fairytaleEndingText = "fairytaleEndingText"
    fairytaleEndingButtonRestart = "fairytaleEndingButtonRestart"
    fairytaleEndingButtonEndSession = "fairytaleEndingButtonEndSession"
    fairytaleEndingButtonOtherPerson = "fairytaleEndingButtonOtherPerson"

    @property
    def get(self) -> str:
        messagesKeys = storage.getJsonData(storage.path.botContentUniqueMessages)
        if self.value in messagesKeys:
            return messagesKeys[self.value]
        else:
            return "Unknown"

textConstant = UniqueMessagesKeys
