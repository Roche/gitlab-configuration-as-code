from abc import ABC
from enum import Enum

from gitlab import Gitlab
from .utils import logger


class Mode(Enum):
    TEST_SKIP_VALIDATION = -2
    TEST = -1
    APPLY = 0


class Configurer(ABC):
    def __init__(
        self, gitlab, config, mode=Mode.APPLY
    ):  # type: (Gitlab, dict, Mode)->any
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


class UpdateOnlyConfigurer(Configurer):
    def __init__(self, name, gitlab, config, mode=Mode.APPLY):
        self.name = name
        self.logger = logger.get_logger(name)
        super().__init__(gitlab, config, mode=mode)

    def _save(self, data):
        data.save()

    def _load(self):
        raise NotImplementedError("")

    def configure(self):
        self.logger.info("Configuring %s", self.name)
        data = self._load()
        changes = self._update_setting(data, self.config)
        self.logger.info("Found %s changed values", changes)
        if changes != 0:
            self.logger.info("Applying changes...")
            if self.mode == Mode.APPLY:
                self._save(data)
            else:
                self.logger.info("No changes will be applied due to test mode enabled")
        else:
            self.logger.info("Nothing to do")
        return data

    def _update_setting(
        self, current, new, changes=0, prefix=""
    ):  # type: (dict, dict, int, str)->int
        for key, value in new.items():
            if isinstance(value, dict):
                changes += self._update_setting(
                    current, value, changes, "{0}_".format(key)
                )
                continue

            if isinstance(value, list):
                self.logger.warn("List is not supported")
                continue

            prefixed_key = "{0}{1}".format(prefix, key)

            self.logger.debug("Checking %s", prefixed_key)
            if hasattr(current, prefixed_key):
                current_value = getattr(current, prefixed_key)
                if current_value != value:
                    changes += 1
                    self.logger.info("modified: %s.%s", self.name, prefixed_key)
                    if self.mode == Mode.APPLY:
                        setattr(current, prefixed_key, value)
            else:
                self.logger.warn("Found invalid configuration option: %s", prefixed_key)
        return changes


class ValidationResult(object):
    def __init__(self, errors=None):
        self.errors = [] if errors is None else errors

    def add(self, error, *args):  # type: (str, *str) -> ()
        message = error.format(*args) if args else error
        self.errors.append(message)

    def get(self):
        return self.errors

    def get_as_string(self):
        return "\n".join(self.errors)

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
            return ValidationError("Validation failed, but no errors provided")
        errors = validation_result.get_as_string()
        return ValidationError(
            "Configuration validation failed with errors:\n{0}".format(errors)
        )
