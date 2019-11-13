from abc import ABC


class Configurer(ABC):
    def __init__(self, gitlab, config):
        self.gitlab = gitlab
        self.config = config
        self._validate()

    def _log(self, field, old_val, new_val):
        print("Change value of {0} from {1} to {2}".format(field, old_val, new_val))

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