import re

from .base import Configurer, Mode
from .utils import diff, logger, objects
from .utils.validators import ValidationResult

logger = logger.get_logger("instance_variables")


class InstanceVariablesConfigurer(Configurer):
    _NAME = "instance_variables"
    _SCHEMA = """
        type: object
        propertyNames:
          pattern: "^[a-zA-Z0-9_]*$"
          maxLength: 255
        patternProperties:
          "^.*$":
            type:
              - object
              - string
              - boolean
              - integer
            maxLength: 10000
            required:
              - value
            properties:
              masked:
                type: boolean
              protected:
                type: boolean
              value:
                maxLength: 10000
                type:
                  - string
                  - boolean
                  - integer
              variable_type:
                type: string
                enum:
                  - file
                  - env_var
            additionalProperties: false
    """

    def __init__(
        self, gitlab, instance_variables, mode=Mode.APPLY
    ):  # type: (gitlab.Gitlab, dict, Mode)->InstanceVariablesConfigurer
        super().__init__(gitlab, instance_variables, mode=mode)

    def __map_variable(self, k, v):
        return {**v, "key": k} if isinstance(v, dict) else {"value": v, "key": k}

    def configure(self):
        logger.info("Configuring Instance Variables")
        existing_variables = self.gitlab.variables.list()
        list_conf = [self.__map_variable(k, v) for k, v in self.config.items()]
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

    def _validate(self, errors):  # type: (ValidationResult) -> ()
        for key, variable in self.config.items():
            is_dict = isinstance(variable, dict)
            if not is_dict:
                continue
            value = variable.get("value") if is_dict else variable
            if value is None:
                continue
            path = [key, "value"]
            if variable.get("masked"):
                if len(value) < 8:
                    errors.add("must have at least 8 chars to be masked", path=path)
                if "\n" in value:
                    errors.add("must be in a single line to be masked", path=path)
                # https://gitlab.com/gitlab-org/gitlab/-/blob/fd3a3a8f75f7bddc7c02dc9cf178986bc008ae60/app/models/concerns/ci/maskable.rb
                if not bool(re.match(r"\A[a-zA-Z0-9_+=/@:.~\-]+\Z", value)):
                    errors.add(
                        "must consist only of characters from Base64 alphabet plus '@', ':', '-'",
                        path=path,
                    )

        return errors
