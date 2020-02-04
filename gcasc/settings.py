from .base import Mode, UpdateOnlyConfigurer


class SettingsConfigurer(UpdateOnlyConfigurer):
    def __init__(self, gitlab, settings, mode=Mode.APPLY):
        super().__init__("ApplicationSettings", gitlab, settings, mode=mode)

    def _load(self):
        return self.gitlab.settings.get()

    def validate(self):
        pass
