from .utils import logger
from .utils import diff
from .utils import objects
import re

from .base import Configurer, Mode, ValidationResult

logger = logger.get_logger("instance_variables")


class InstanceVariablesConfigurer(Configurer):
    _NAME = "instance_variables"

    def __init__(
        self, gitlab, instance_variables, mode=Mode.APPLY
    ):  # type: (gitlab.Gitlab, dict, Mode)->InstanceVariablesConfigurer
        super().__init__(gitlab, instance_variables, mode=mode)

    def __map_variable(self, k, v):
        return {**v, "key": k} if isinstance(v, dict) else {"value": v, "key": k}

    def configure(self):
        logger.info("Configuring Instance Variables")
        existing_variables = self.gitlab.variables.list()
        list_conf = [self.__map_variable(k,v) for k, v in self.config.items()]
        result = diff.diff_list(list_conf, existing_variables, "key")
        if result.has_changes():
            self._remove(result.remove)
            self._create(result.create)
            self._update(result.update)
        else:
            logger.info("Nothing has changed")

    def _remove(self, variables):
        for var in variables:
            logger.info("Removing: %s", var.key)
            if self.mode == Mode.APPLY:
                var.delete()

    def _update(self, variables):
        for new_values, var in variables:
            logger.info("Updating: %s", var.key)
            objects.update_object(var, new_values)
            if self.mode == Mode.APPLY:
                var.save()

    def _create(self, variables):
        for var in variables:
            logger.info("Creating: %s", var.get("key"))
            if self.mode == Mode.APPLY:
                self.gitlab.variables.create(var)

    def validate(self):  # type: () -> ValidationResult
        errors = ValidationResult()
        for key, variable in self.config.items():
            is_dict = isinstance(variable, dict)
            value = variable.get("value") if is_dict else variable
            value_length = len(value)
            if not value or value_length == 0:
                errors.add("instance_variables[{0}] must have value property", key)
            elif value and value_length > 10000:
                errors.add("instance_variables[{0}] can have 10,000 characters", key)
            if not is_dict:
                continue
            if variable.get("masked"):
                if value_length < 8:
                    errors.add(
                        "instance_variables[{0}] must have at least 8 chars to be masked",
                        key,
                    )

                if "\n" in value:
                    errors.add("instance_variables[{0}] must be in a single line", key)
                if not bool(re.match(r"[a-zA-Z0-9+/=@:]+$", value)):
                    errors.add(
                        "instance_variables[{0}] must consist only of characters from Base64 alphabet plus '@', ':'",
                        key,
                    )
            variable_type = variable.get("variable_type")
            if variable_type and variable_type not in ["env_var", "file"]:
                errors.add("instance_variables[{0}] variable_type must be 'env_var' or 'file'", key)
        return errors
