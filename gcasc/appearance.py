from .base import UpdateOnlyConfigurer, Mode


class AppearanceConfigurer(UpdateOnlyConfigurer):
    def __init__(self, gitlab, settings, mode=Mode.APPLY):
        super().__init__("Appearance", gitlab, settings, mode=mode)

    def _load(self):
        return self.gitlab.appearance.get()