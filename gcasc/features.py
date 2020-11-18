from .base import Configurer, Mode
from .utils import logger

logger = logger.get_logger("Features")


class FeaturesConfigurer(Configurer):
    _NAME = "features"
    _SCHEMA = """
        type: array
        items:
          - type: object
            required:
              - name
              - value
            properties:
              name:
                type: string
              value:
                type:
                  - string
                  - boolean
                  - number
              projects:
                type: array
                items:
                  type: string
              users:
                type: array
                items:
                  type: string
              groups:
                type: array
                items:
                  type: string
            additionalProperties: false
    """

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
            if self.mode == Mode.APPLY:
                self.__apply(name, value, feature)
            logger.info("Configured: %s => %s", name, value)
        return self.gitlab.features.list()

    def __set_canary(
        self, canary_name, canaries, feature_name, feature_value, feature_group
    ):
        if canaries:
            for canary_value in canaries:
                logger.info("Configuring canary: %s => %s", canary_name, canary_value)
                self.gitlab.features.set(
                    feature_name,
                    feature_value,
                    feature_group=feature_group,
                    **{canary_name: canary_value}
                )
            return True
        return False

    def __apply(self, name, value, feature):
        feature_group = feature.get("feature_group")
        users = feature.get("users")
        is_set = self.__set_canary("user", users, name, value, feature_group)
        groups = feature.get("groups")
        is_set = (
            self.__set_canary("group", groups, name, value, feature_group) or is_set
        )
        projects = feature.get("projects")
        is_set = (
            self.__set_canary("project", projects, name, value, feature_group) or is_set
        )
        if not is_set:  # set feature globally
            self.gitlab.features.set(name, value, feature_group=feature_group)

    def __remove_existing(self):
        if self.mode == Mode.APPLY:
            features = self.gitlab.features.list()
            [feature.delete() for feature in features]
