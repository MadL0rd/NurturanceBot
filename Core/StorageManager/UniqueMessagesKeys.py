
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

    @property
    def get(self) -> str:
        messagesKeys = storage.getJsonData(storage.path.botContentUniqueMessages)
        if self.value in messagesKeys:
            return messagesKeys[self.value]
        else:
            return "Unknown"

textConstant = UniqueMessagesKeys
