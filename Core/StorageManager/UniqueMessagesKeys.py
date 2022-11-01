
import enum
import Core.StorageManager.StorageManager as storage 

class UniqueMessagesKeys(enum.Enum):

    adminButtonText = "adminButtonText"
    unknownState = "unknownState"
    menuButtonReturnToMainMenu = "menuButtonReturnToMainMenu"

    def get(self):
        messagesKeys = storage.getJsonData(storage.path.botContentUniqueMessages)
        if self.value in messagesKeys:
            return messagesKeys[self.value]
        else:
            return "Unknown"

textConstant = UniqueMessagesKeys
