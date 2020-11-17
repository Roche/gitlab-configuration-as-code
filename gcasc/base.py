import collections
from abc import ABC
from enum import Enum

import jsonschema
import yaml
from gitlab import Gitlab
from jsonschema import draft7_format_checker

from . import GcascException
from .exceptions import ValidationException
from .utils import logger as logging
from .utils.validators import ValidationResult, create_message


class Mode(Enum):
    TEST_SKIP_VALIDATION = -2
    TEST = -1
    APPLY = 0


class Configurer(ABC):
    _NAME = None
    _SCHEMA = None

    def __init__(
        self, gitlab, config, mode=Mode.APPLY
    ):  # type: (Gitlab, dict, Mode)->any

        if not self._NAME:
            raise GcascException(
                "Class property _NAME must be defined! It will be expected "
                "to exist in configuration file as a key"
            )
        self.logger = logging.get_logger(self._NAME)
        self.gitlab = gitlab
        self.config = config
        self.mode = mode

    def configure(self):
        pass

    def _validate(self, result):  # type: (ValidationResult) -> ()
        pass

    def _get(self, property):
        return self.config.get(property)

    def __apply_schema_error(self, err, result):
        message = create_message(err)
        path = list(collections.deque(err.absolute_path))
        if len(path) == 0:
            # assume that for empty path this is objet property, thus value needs to be included in path
            path.append(err.instance)
        result.add(message, path=path)

    def __validate_schema(self, result):  # type: (ValidationResult) -> ()
        self.logger.debug("Validating configuration schema")
        schema = yaml.safe_load(self._SCHEMA)
        validator = jsonschema.Draft7Validator(
            schema, format_checker=draft7_format_checker
        )
        for err in sorted(
            validator.iter_errors(self.config), key=lambda error: error.absolute_path
        ):
            if err.validator in ["allOf", "anyOf", "oneOf", "patternProperties"]:
                [self.__apply_schema_error(ctx_err, result) for ctx_err in err.context]
            else:
                self.__apply_schema_error(err, result)

    def validate(self):
        self.logger.debug("Validating provided configuration")
        if self.gitlab is None:
            raise GcascException("GitLab client is not initialized")
        if self.config is not None:
            result = ValidationResult(self._NAME)
            if self._SCHEMA is not None and len(self._SCHEMA) > 0:
                self.__validate_schema(result)
            self._validate(result)
            if result and result.has_errors():
                if self.logger.is_debug_enabled():
                    self.logger.debug("Validation errors found:")
                    result.iterate(lambda message: self.logger.debug(message))
                error = ValidationException.from_validation_result(result)
                raise error


class UpdateOnlyConfigurer(Configurer):
    def __init__(self, name, gitlab, config, mode=Mode.APPLY):
        self.name = name
        self.logger = logging.get_logger(name)
        super().__init__(gitlab, config, mode=mode)

    def _save(self, data):
        data.save()

    def _load(self):
        raise NotImplementedError("")

    def configure(self):
        self.logger.info("Configuring %s", self.name)
        self.logger.debug("Loading data")
        data = self._load()
        self.logger.debug("Data loaded. Updating setttings...")
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
                    current, value, changes, "{0}{1}_".format(prefix, key)
                )
                continue

            prefixed_key = "{0}{1}".format(prefix, key)

            self.logger.debug("Checking %s", prefixed_key)
            if hasattr(current, prefixed_key):
                current_value = getattr(current, prefixed_key)
                if current_value != value:
                    changes += 1
                    if current_value is None:
                        self.logger.info("Set: %s = %s", prefixed_key, value)
                    elif value is None:
                        self.logger.info("Unset: %s = %s", prefixed_key, current_value)
                    else:
                        self.logger.info(
                            "Updated %s: %s => %s", prefixed_key, current_value, value
                        )
                    if self.mode == Mode.APPLY:
                        setattr(current, prefixed_key, value)
            else:
                self.logger.warn(
                    "Invalid configuration option: %s. Skipping...", prefixed_key
                )
        return changes
