import datetime
import logging

from .config import Config
from .resource_base import ResourceBase

config = Config()
log = logging.getLogger(config.log_config['log-name'])


class ActionBase(ResourceBase):

    def __init__(self, *args, **kwargs):
        log.debug('')
        return super(ActionBase, self).__init__(*args, **kwargs)

    def execute(self, instruction_set):
        log.debug('')
        if not instruction_set or isinstance(instruction_set, dict) and \
                instruction_set.get('failed'):
            return instruction_set
        return super(ActionBase, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(ActionBase, self).set_values(value_set, *args, **kwargs)

