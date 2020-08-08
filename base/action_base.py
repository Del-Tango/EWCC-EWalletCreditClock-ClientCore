import datetime
import logging

from .config import Config
from .resource_base import ResourceBase

config_file = __name__.split('.')
config_file.remove(config_file[-1])
config_file.remove(config_file[-1])
file_path = 'conf/ewcc.conf' if not config_file else \
    '/'.join(item for item in config_file) + '/conf/ewcc.conf'
config = Config(config_file=file_path)
config.config_init(config_file=file_path)
log = logging.getLogger(config.log_config.get('log-name') or __name__)


class ActionBase(ResourceBase):

    def __init__(self, *args, **kwargs):
        log.debug('')
        return super(ActionBase, self).__init__(*args, **kwargs)

    def execute(self, *args, **kwargs):
        log.debug('')
        return super(ActionBase, self).execute(*args, **kwargs)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(ActionBase, self).set_values(value_set, *args, **kwargs)

# CODE DUMP
#       if not instruction_set or isinstance(instruction_set, dict) and \
#               instruction_set.get('failed'):
#           return instruction_set

