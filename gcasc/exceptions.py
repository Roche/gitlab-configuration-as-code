import sys

from gitlab import (
    GitlabAuthenticationError,
    GitlabCreateError,
    GitlabDeleteError,
    GitlabError,
    GitlabGetError,
    GitlabLicenseError,
    GitlabListError,
    GitlabSetError,
    GitlabUpdateError,
)

from gcasc.utils.logger import Logger


class GcascException(Exception):
    pass


class ClientInitializationException(GcascException):
    pass


class ValidationException(GcascException):
    def __init__(self, message, result=None):
        super().__init__(message)
        self.result = result

    @staticmethod
    def from_validation_result(validation_result):
        if validation_result is None or not validation_result.has_errors():
            return ValidationException("Validation failed, but no errors were provided")
        return ValidationException(
            "Configuration validation failed with following errors",
            result=validation_result,
        )


def _log_exception(ex, logger):
    logger.error(ex)


def _handle_validation_exception(
    exc, logger
):  # type: (ValidationException, Logger) -> ()
    _log_exception(exc, logger)
    exc.result.iterate(lambda message: logger.error(message))


def handle_gcasc_exception(exc, logger):  # type: (GcascException, Logger) -> ()
    switch = {ValidationException: _handle_validation_exception}
    exc_type = type(exc)
    switch.get(exc_type, _log_exception)(exc, logger)
    sys.exit(1)


def handle_gitlab_exception(exc, logger):  # type: (GitlabError, Logger) -> ()
    switch = {
        GitlabAuthenticationError: "Authentication to GitLab failed",
        GitlabListError: "Unable to list GitLab resources",
        GitlabGetError: "Unable to get GitLab resource",
        GitlabCreateError: "GitLab resource creation failed",
        GitlabUpdateError: "GitLab resource update failed",
        GitlabDeleteError: "GitLab resource deletion failed",
        GitlabSetError: "GitLab resource property change failed",
        GitlabLicenseError: "Provided licence is invalid",
    }
    exc_type = type(exc)
    message = switch.get(exc_type, "Error occurred while communicating with GitLab")
    logger.error(f"{message}\nHTTP {exc.response_code}, {exc.error_message}")
    sys.exit(1)
