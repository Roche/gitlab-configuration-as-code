from jsonschema.exceptions import ValidationError as SchemaValidationError


def rewrite_error_message(error):
    return error.message


validator_type_message_generator = {
    "required": rewrite_error_message,
    "dependencies": rewrite_error_message,
    "type": lambda error: f"is not of type '{error.validator_value}'",
    "enum": lambda error: f"is not one of '{error.validator_value}'",
    "maxLength": lambda error: f"is too long (maximum {error.validator_value} characters expected)",
    "minLength": lambda error: f"is too short (minimum {error.validator_value} characters expected)",
    "format": lambda error: f"does not match '{error.validator_value}' format",
    "pattern": lambda error: f"does not match pattern '{error.validator_value}'",
    "maximum": lambda error: f"is greater than the maximum of {error.validator_value}",
    "minimum": lambda error: f"is less than the minimum of {error.validator_value}",
    "exclusiveMaximum": lambda error: f"is greater than or equal to the maximum of {error.validator_value}",
    "exclusiveMinimum": lambda error: f"is less than or equal to the minimum of {error.validator_value}",
    "multipleOf": lambda error: f"is not multiple of of {error.validator_value}",
    "minItems": lambda error: f"does not contain enough elements (minimum {error.validator_value} elements expected)",
    "maxItems": lambda error: f"contains too many elements (maximum {error.validator_value} elements expected)",
    "uniqueItems": lambda error: f"has non-unique elements",
    "additionalProperties": lambda error: f"contains unexpected properties",
    "const": rewrite_error_message,
}


def create_message(schema_error):  # type: (SchemaValidationError) -> str
    return validator_type_message_generator.get(
        schema_error.validator,
        lambda error: f"did not pass {error.validator} ({error.validator_value}) validation",
    )(schema_error)


class ValidationResult(object):
    def __init__(self, type=None, errors=None):
        self._errors = [] if errors is None else errors
        self.type = type

    def __create_full_message(self, message, path=None, *args):
        message = message.format(*args) if args else message
        full_path = self.__prepare_path(path)
        return f"{full_path} {message}" if len(full_path) > 0 else message

    def add(self, error, path=None, *args):  # type: (str, list, *str) -> ()
        self._errors.append(
            {
                "message": error,
                "full_message": self.__create_full_message(error, path, args),
                "path": path,
            }
        )

    def __wrap(self, part):
        return f"[{part}]" if isinstance(part, int) else f"['{part}']"

    def __prepare_path(self, path):
        type = self.type if self.type is not None else ""
        if path is None:
            return type
        full_path = ""
        if isinstance(path, list):
            mapped = map(self.__wrap, path)
            full_path = "".join(mapped)
        elif isinstance(path, dict):
            pass
        return f"{type}{full_path}"

    def get(self):
        return self._errors

    def iterate(self, consumer):
        messages = map(lambda x: x["full_message"], self._errors)
        [consumer(message) for message in messages]

    def get_as_string(self):
        messages = map(lambda x: x["full_message"], self._errors)
        return "\n".join(messages)

    def has_errors(self):
        return len(self._errors) > 0

    def has_error(self, message=None, path=None):
        by_message = message is not None
        by_path = path is not None
        if by_message and by_path:
            return self.has_error_message_and_path(message, path)
        elif by_message and not by_path:
            return self.has_error_message(message)
        elif not by_message and by_path:
            return self.has_error_path(path)
        else:
            return False

    def has_error_message_and_path(self, message, path):
        path = path if isinstance(path, list) else [path]
        return (
            next(
                (
                    e
                    for e in self._errors
                    if e["path"] == path and message in e["message"]
                ),
                None,
            )
            is not None
        )

    def has_error_path(self, path):
        path = path if isinstance(path, list) else [path]
        return next((e for e in self._errors if e["path"] == path), None) is not None

    def has_error_message(self, message):
        return (
            next((e for e in self._errors if message in e["message"]), None) is not None
        )
