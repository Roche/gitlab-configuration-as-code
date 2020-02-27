from .utils import logger

from .base import Configurer, Mode, ValidationResult
from validator_collection import checkers
import gcasc.utils.validators as validators

logger = logger.get_logger("configurer.oauth_applications")


class OauthApplicationsConfigurer(Configurer):
    _NAME = "oauth_applications"

    def __init__(
        self, gitlab, apps, mode=Mode.APPLY
    ):  # type: (gitlab.Gitlab, dict, Mode)->OauthApplicationsConfigurer
        super().__init__(gitlab, apps, mode=mode)

    def configure(self):
        logger.info("Configuring GitLab OAuth applications")
        self.__remove_existing()
        # TODO -- change to not removing existing apps if matcher uri and/or name!!!
        for app in self.config:
            name = app["name"]
            redirect_uri = app["redirect_uri"]
            logger.info("OAuth application: %s, %s", name, redirect_uri)
            if self.mode == Mode.APPLY:
                self.__apply(name, redirect_uri, app)
        return self.gitlab.features.list()

    def __apply(self, name, redirect_uri, app):
        trusted = app.get("trusted", False)
        scopes = app.get("scopes", [])
        self.gitlab.applications.create({
            "name": name,
            "redirect_uri": redirect_uri,
            "trusted": bool(trusted),
            "scopes": scopes
        })

    def __remove_existing(self):
        if self.mode == Mode.APPLY:
            apps = self.gitlab.applications.list()
            [app.delete() for app in apps]

    def validate(self):  # type: () -> ValidationResult
        errors = ValidationResult()
        for idx, app in enumerate(self.config):
            name = app.get("name")
            if not name:
                errors.add("oauth_application[{0}] must have name property", str(idx))
            redirect_uri = app.get("redirect_uri")
            if redirect_uri is None:
                errors.add("oauth_application[{0}] must have redirect_uri property", str(idx))
            else:
                if not checkers.is_url(redirect_uri):
                    errors.add("oauth_application[{0}].redirect_uri must be a valid URI", str(idx))
                if not (validators.is_http(redirect_uri) or validators.is_http(redirect_uri)):
                    errors.add("oauth_application[{0}].redirect_uri must start with http or https protocol", str(idx))
            self.__validate_scopes(app.get("scopes", []), errors)
        return errors

    def __validate_scopes(self, scopes, errors):

        pass