from .utils import logger

from .base import Configurer, Mode, ValidationResult

logger = logger.get_logger("configurer.features")


class FeaturesConfigurer(Configurer):
    _NAME = "features"

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
        for idx, feature in enumerate(self.config):
            name = feature.get("name")
            if not name:
                errors.add("feature[{0}] must have name property", str(idx))
            else:
                name = "{0}.{1}".format(idx, name)
            if feature.get("value") is None:
                errors.add("feature[{0}] must have value property", name)
        return errors
