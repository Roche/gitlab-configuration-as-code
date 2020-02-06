from .utils import logger
import gcasc.utils.validators as validators

from .base import Configurer, Mode, ValidationResult

logger = logger.get_logger("configurer.features")


class FeaturesConfigurer(Configurer):
    def __init__(
        self, gitlab, features, mode=Mode.APPLY
    ):  # type: (gitlab.Gitlab, dict, Mode)->FeaturesConfigurer
        super().__init__(gitlab, features, mode=mode)

    def configure(self):
        logger.info("Configuring GitLab Features")
        self.__remove_existing()

        for feature in self.config:
            name = feature["name"]
            value = feature["value"]
            logger.info("Feature: %s=%s", name, value)
            if self.mode == Mode.APPLY:
                self.__apply(name, value, feature)
        return self.gitlab.features.list()

    def __apply(self, name, value, feature):
        feature_group = feature.get("feature_group")
        canaries = feature.get("canaries")
        logger.info("Feature: %s=%s", name, value)
        if canaries:
            for canary in canaries:
                self.gitlab.features.set(
                    name,
                    value,
                    feature_group=feature_group,
                    user=canary.get("user"),
                    group=canary.get("group"),
                    project=canary.get("project"),
                )
        else:
            self.gitlab.features.set(name, value, feature_group=feature_group)

    def __remove_existing(self):
        if self.mode == Mode.APPLY:
            features = self.gitlab.features.list()
            [feature.delete() for feature in features]

    def validate(self):  # type: () -> ValidationResult
        errors = ValidationResult()
        # if not self.__get_starts_at():
        #     errors.add("Feature name must be provided")
        # if not self.
        # elif not validators.validate_date(self.__get_starts_at(), "%Y-%m-%d"):
        #     errors.add(
        #         "starts_at license property must follow format yyyy-MM-dd, e.g. 2019-03-28"
        #     )
        return errors
