import datetime

from .utils import logger
import gcasc.utils.validators as validators

from .base import Configurer, Mode, ValidationResult

logger = logger.get_logger("configurer.license")


class LicenseConfigurer(Configurer):
    def __init__(
        self, gitlab, license, mode=Mode.APPLY
    ):  # type: (gitlab.Gitlab, dict, Mode)->LicenseConfigurer
        super().__init__(gitlab, license, mode=mode)

    def configure(self):
        logger.info("Configuring GitLab licenses")
        license = self.gitlab.get_license()
        if not self.__check_if_same_license(license) and self.mode == Mode.APPLY:
            license = self._update_license()
        logger.info(
            "Current license:\nplan: %s\nstarts_at: %s\nexpires_at: %s\nuser_limit: %s",
            self.__get_plan(license),
            self.__get_starts_at(license),
            self.__get_expires_at(license),
            self.__get_user_limit(license),
        )
        return license

    def __get(self, field, license=None):  # type: (str, dict) -> str
        license_config = license if license is not None else self.config
        return license_config.get(field)

    def __get_date(self, field, license=None):
        date = self.__get(field, license)
        return date.strftime("%Y-%m-%d") if isinstance(date, datetime.date) else date

    def __get_starts_at(self, license=None):  # type: (dict) -> str
        return self.__get_date("starts_at", license)

    def __get_expires_at(self, license=None):  # type: (dict) -> str
        return self.__get_date("expires_at", license)

    def __get_plan(self, license=None):  # type: (dict) -> str
        return self.__get("plan", license)

    def __get_user_limit(self, license=None):  # type: (dict) -> str
        return self.__get("user_limit", license)

    def __get_data(self, license=None):  # type: (dict) -> str
        return self.__get("data", license)

    def __check_if_same_license(self, license):
        return (
            self.__get_starts_at() == self.__get_starts_at(license)
            and self.__get_expires_at() == self.__get_expires_at(license)
            and self.__get_plan() == self.__get_plan(license)
            and self.__get_user_limit() == self.__get_user_limit(license)
        )

    def _update_license(self):
        logger.info("Updating GitLab license...")
        return self.gitlab.set_license(self.__get_data())

    def validate(self):  # type: () -> ValidationResult
        errors = ValidationResult()
        if not self.__get_starts_at():
            errors.add("License must have starts_at property set in format yyyy-MM-dd")
        elif not validators.validate_date(self.__get_starts_at(), "%Y-%m-%d"):
            errors.add(
                "starts_at license property must follow format yyyy-MM-dd, e.g. 2019-03-28"
            )
        if not self.__get_expires_at():
            errors.add("License must have expires_at property set in format yyyy-MM-dd")
        elif not validators.validate_date(self.__get_expires_at(), "%Y-%m-%d"):
            errors.add(
                "expires_at license property must follow format yyyy-MM-dd, e.g. 2019-03-28"
            )
        if not self.__get_plan():
            errors.add("License must have plan property set")
        elif not self.__get_plan() in ["starter", "premium", "ultimate"]:
            errors.add(
                "License plan property was '{0}', but should be one of: starter, premium or ultimate",
                self.__get_plan(),
            )
        if not self.__get_user_limit():
            errors.add("License must have user_limit property set in format")
        if not self.__get_data():
            errors.add(
                "License must have data property configured containing license itself"
            )
        return errors
