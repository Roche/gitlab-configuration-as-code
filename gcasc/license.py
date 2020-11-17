import datetime

from .base import Configurer, Mode
from .utils import logger

logger = logger.get_logger("License")


class LicenseConfigurer(Configurer):
    _NAME = "license"
    _SCHEMA = """
        type: object
        required:
          - starts_at
          - expires_at
          - plan
          - user_limit
          - data
        properties:
          starts_at:
            type: string
            format: date
          expires_at:
            type: string
            format: date
          plan:
            type: string
            enum:
              - starter
              - premium
              - ultimate
          user_limit:
            type: number
            minimum: 1
          data:
            type: string
        additionalProperties: false
    """

    def __init__(
        self, gitlab, license, mode=Mode.APPLY
    ):  # type: (gitlab.Gitlab, dict, Mode)->LicenseConfigurer
        super().__init__(gitlab, license, mode=mode)

    def configure(self):
        logger.info("Configuring GitLab licenses")
        current_license = self.gitlab.get_license()
        if (
            not self.__check_if_same_license(current_license)
            and self.mode == Mode.APPLY
        ):
            current_license = self._update_license()
        logger.info(
            "Current license:\nplan: %s\nstarts_at: %s\nexpires_at: %s\nuser_limit: %s",
            self.__get_plan(current_license),
            self.__get_starts_at(current_license),
            self.__get_expires_at(current_license),
            self.__get_user_limit(current_license),
        )
        return current_license

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
