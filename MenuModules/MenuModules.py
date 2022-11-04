import enum
from MenuModules.Onboarding.Onboarding import Onboarding
from MenuModules.MainMenu.MainMenu import MainMenu
from MenuModules.MenuModuleInterface import MenuModuleInterface
from MenuModules.AdminMenu.AdminMenu import AdminMenu
from MenuModules.RandomNews.RandomNews import RandomNews

class MenuModules(enum.Enum):

    onboarding: MenuModuleInterface = Onboarding()
    mainMenu: MenuModuleInterface = MainMenu()
    adminMenu: MenuModuleInterface = AdminMenu()
    exercises: MenuModuleInterface = Onboarding()
    randomNews: MenuModuleInterface = RandomNews()
    relax: MenuModuleInterface = Onboarding()

    @property
    def get(self) -> MenuModuleInterface:
        return self.value