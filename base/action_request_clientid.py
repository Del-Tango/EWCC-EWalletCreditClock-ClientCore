import datetime
import logging

from .config import Config
from .action_base import ActionBase

config = Config()
log = logging.getLogger(config.log_config['log-name'])


class RequestClientID(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(RequestClientID, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'request',
            'request': 'client_id',
        }
        return res

    # FETCHERS

    # CORE

    def execute(self, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set()
        return super(RequestClientID, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(RequestClientID, self).set_values(value_set, *args, **kwargs)

