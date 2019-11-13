import logging
import os

level_str = os.getenv('LOGGING_LEVEL', 'INFO')
level = logging.getLevelName(level_str)

logging.basicConfig(format='[%(levelname)s] [%(name)s] %(message)s', level=level)


def get_logger(name='gcasc'):
    return Logger(name)


def _apply_masking(value, mask=False):
    return '***' if mask else value


class Logger(object):

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def log_update(self, field, old_value, new_value, masked=False):
        self.debug('Changed value of %s from %s to %s', field, _apply_masking(old_value, masked),
                   _apply_masking(new_value, masked))
        pass

    def log_create(self, value, field=None, masked=False):
        value_to_log = _apply_masking(value, masked)
        if field is None:
            self.debug('Created new object: %s', value_to_log)
        else:
            self.debug('Created new field %s with value %s', field, value_to_log)
        pass

    def log_delete(self, field):
        self.debug('Deleted field or object: %s', field)
        pass

    def debug(self, message, *args):
        self.logger.debug(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def warn(self, message, *args):
        self.logger.warning(message, *args)

    def info(self, message, *args):
        self.logger.info(message, *args)
