from abc import ABC
from enum import Enum


class Mode(Enum):
    TEST = -1
    APPLY = 0


class Configurer(ABC):
    def __init__(self, gitlab, config, mode=Mode.APPLY):
        self.gitlab = gitlab
        self.config = config
        self.mode = mode
        self._validate()

    def configure(self):
        pass

    def validate(self):
        pass

    def _validate(self):
        if self.gitlab is None:
            raise RuntimeError('GitLab client is not provided')

        if self.config is None:
            raise RuntimeError('Configuration was not provided')

        self.validate()
