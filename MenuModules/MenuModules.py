import enum
from MenuModules.Onboarding.Onboarding import Onboarding
from MenuModules.MainMenu.MainMenu import MainMenu
from MenuModules.MenuModuleInterface import MenuModuleInterface
from MenuModules.AdminMenu.AdminMenu import AdminMenu

class MenuModules(enum.Enum):

    onboarding: MenuModuleInterface = Onboarding()
    mainMenu: MenuModuleInterface = MainMenu()
    adminMenu: MenuModuleInterface = AdminMenu()
    exercises: MenuModuleInterface = Onboarding()
    randomNews: MenuModuleInterface = Onboarding()
    relax: MenuModuleInterface = Onboarding()

    @property
    def get(self) -> MenuModuleInterface:
        return self.value