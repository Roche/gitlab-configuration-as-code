from abc import ABC
from enum import Enum


class Mode(Enum):
    TEST = -1
    APPLY = 0


class Configurer(ABC):
    def __init__(self, gitlab, config, mode=Mode.APPLY):
        # type: (gitlab.Gitlab, dict, Mode)->any
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
            raise RuntimeError("GitLab client is not provided")
        if self.config is not None:
            self.validate()
