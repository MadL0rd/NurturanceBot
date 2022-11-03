import enum

class MenuModuleName(enum.Enum):

    onboarding: str = "onboarding"
    mainMenu: str = "mainMenu"
    exercises: str = "exercises"
    randomNews: str = "randomNews"
    relax: str = "relax"
    admin: str = "admin"

    @property
    def get(self) -> str:
        return self.value