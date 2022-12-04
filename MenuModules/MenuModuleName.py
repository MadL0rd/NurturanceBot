import enum

class MenuModuleName(enum.Enum):

    onboarding: str = "onboarding"
    mainMenu: str = "mainMenu"
    mainMenuNewSession: str = "mainMenuNewSession"
    exercises: str = "exercises"
    randomNews: str = "randomNews"
    relax: str = "relax"
    admin: str = "admin"
    notificationsSettings: str = "motificationsSettings"
    otherHuman: str = "otherHuman"
    otherHumanEnding: str = 'otherHumanEnding'
    otherHumanEndingYes: str = 'otherHumanEndingYes'
    otherHumanEndingNo: str = 'otherHumanEndingNo'
    eveningReflectionQuestions: str = "eveningReflectionQuestions"
    reflectionMenu: str = 'reflectionMenu'
    fairytale: str = 'fairytale'
    fairytaleEnding: str = 'fairytaleEnding'
    quiz: str = "quiz"
    quizDepression: str = "quizDepression"
    quizAnxiety: str = "quizAnxiety"


    @property
    def get(self) -> str:
        return self.value