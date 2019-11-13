import logging

from .base import Configurer

logger = logging.getLogger('configurer.applicationsettings')

class SettingsConfigurer(Configurer):

    def __init__(self, gitlab, settings):
        super().__init__(gitlab, settings)
        pass

    def configure(self):
        logger.info('Configuring Application Settings')
        settings = self.gitlab.settings.get()
        changes = self._update_setting(settings, self.config)
        logger.info('Found %s changed values', changes)
        if changes != 0:
            logger.info('Applying changes...')
            settings.save()
        else:
            logger.info('Nothing to do')
        return settings

    def _update_setting(self, current, new, changes=0, prefix=''):
        for key, value in new.items():
            if isinstance(value, dict):
                self._update_setting(current, value, changes, '{0}_'.format(key))
                continue

            if isinstance(value, list):
                logger.warning('List is not supported')
                continue

            prefixed_key = '{0}{1}'.format(prefix, key)

            logger.debug('Checking %s', prefixed_key)
            if hasattr(current, prefixed_key):
                current_value = getattr(current, prefixed_key)
                if current_value != value:
                    changes += 1
                    self._log(prefixed_key, current_value, value)
                    setattr(current, prefixed_key, value)
            else:
                logger.warning('Found invalid configuration option: %s', prefixed_key)
        return changes

    def validate(self):
        pass
