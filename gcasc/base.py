from abc import ABC
from enum import Enum

from gitlab import Gitlab


class Mode(Enum):
    TEST_SKIP_VALIDATION = -2
    TEST = -1
    APPLY = 0


class Configurer(ABC):
    def __init__(self, gitlab, config, mode=Mode.APPLY):  # type: (Gitlab, dict, Mode)->any
        self.gitlab = gitlab
        self.config = config
        self.mode = mode
        if self.mode != Mode.TEST_SKIP_VALIDATION:
            self._validate()

    def configure(self):
        pass

    def validate(self):  # type: () -> ValidationResult
        pass

    def _validate(self):
        if self.gitlab is None:
            raise RuntimeError("GitLab client is not provided")
        if self.config is not None:
            result = self.validate()
            if result and result.has_errors():
                error = ValidationError.from_validation_result(result)
                raise error


class ValidationResult(object):

    def __init__(self, errors=None):
        self.errors = [] if errors is None else errors

    def add(self, error, *args):  # type: (str, *str) -> ()
        message = error.format(*args) if args else error
        self.errors.append(message)

    def get(self):
        return self.errors

    def get_as_string(self):
        return '\n'.join(self.errors)

    def has_errors(self):
        return self.errors.__len__() > 0

    def has_error(self, error):
        for e in self.errors:
            if error in e:
                return True
        return False


class ValidationError(RuntimeError):

    @staticmethod
    def from_validation_result(validation_result):
        if validation_result is None:
            return ValidationError('Validation failed, but no errors provided')
        errors = validation_result.get_as_string()
        return ValidationError('Configuration validation failed with errors:\n{0}'.format(errors))
