import enum
from MenuModules.NotificationsSettings.NotificationsSettings import NotificationsSettings
from MenuModules.Onboarding.Onboarding import Onboarding
from MenuModules.MainMenu.MainMenu import MainMenu
from MenuModules.MenuModuleInterface import MenuModuleInterface
from MenuModules.AdminMenu.AdminMenu import AdminMenu
from MenuModules.RandomNews.RandomNews import RandomNews
from MenuModules.Exercises.Exercises import Exercises
from MenuModules.Relax.Relax import Relax

class MenuModules(enum.Enum):

    onboarding: MenuModuleInterface = Onboarding()
    mainMenu: MenuModuleInterface = MainMenu()
    adminMenu: MenuModuleInterface = AdminMenu()
    exercises: MenuModuleInterface = Exercises()
    randomNews: MenuModuleInterface = RandomNews()
    relax: MenuModuleInterface = Relax()
    notificationsSettings: MenuModuleInterface = NotificationsSettings()

    @property
    def get(self) -> MenuModuleInterface:
        return self.value