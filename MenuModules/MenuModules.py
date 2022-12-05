import enum
from MenuModules.EveningReflectionQuestions.EveningReflectionQuestions import EveningReflectionQuestions
from MenuModules.Fairytale.Fairytale import Fairytale
from MenuModules.Fairytale.FairytaleEnding import FairytaleEnding
from MenuModules.MainMenu.MainMenuNewSession import MainMenuNewSession
from MenuModules.NotificationsSettings.NotificationsSettings import NotificationsSettings
from MenuModules.Onboarding.Onboarding import Onboarding
from MenuModules.MainMenu.MainMenu import MainMenu
from MenuModules.MenuModuleInterface import MenuModuleInterface
from MenuModules.AdminMenu.AdminMenu import AdminMenu
from MenuModules.OtherHuman.OtherHuman import OtherHuman
from MenuModules.OtherHuman.OtherHumanEnding import OtherHumanEnding
from MenuModules.OtherHuman.OtherHumanEndingYes import OtherHumanEndingYes
from MenuModules.OtherHuman.OtherHumanEndingNo import OtherHumanEndingNo
from MenuModules.Quiz.Quiz import Quiz
from MenuModules.Quiz.QuizAnxiety import QuizAnxiety
from MenuModules.Quiz.QuizDepression import QuizDepression
from MenuModules.RandomNews.RandomNews import RandomNews
from MenuModules.Exercises.Exercises import Exercises
from MenuModules.Relax.Relax import Relax
from MenuModules.ReflectionMenu.ReflectionMenu import ReflectionMenu

class MenuModules(enum.Enum):

    onboarding: MenuModuleInterface = Onboarding()
    mainMenu: MenuModuleInterface = MainMenu()
    mainMenuNewSession: MenuModuleInterface = MainMenuNewSession()
    adminMenu: MenuModuleInterface = AdminMenu()
    exercises: MenuModuleInterface = Exercises()
    randomNews: MenuModuleInterface = RandomNews()
    relax: MenuModuleInterface = Relax()
    notificationsSettings: MenuModuleInterface = NotificationsSettings()
    otherHuman: MenuModuleInterface = OtherHuman()
    eveningReflectionQuestions: MenuModuleInterface = EveningReflectionQuestions()
    reflectionMenu: MenuModuleInterface = ReflectionMenu()
    otherHumanEnding: MenuModuleInterface = OtherHumanEnding()
    otherHumanEndingYes: MenuModuleInterface = OtherHumanEndingYes()
    otherHumanEndingNo: MenuModuleInterface = OtherHumanEndingNo()
    fairytale: MenuModuleInterface = Fairytale()
    fairytaleEnding: MenuModuleInterface = FairytaleEnding()
    quiz: MenuModuleInterface = Quiz()
    quizDepression: MenuModuleInterface = QuizDepression()
    quizAnxiety: MenuModuleInterface = QuizAnxiety()
    
    @property
    def get(self) -> MenuModuleInterface:
        return self.value