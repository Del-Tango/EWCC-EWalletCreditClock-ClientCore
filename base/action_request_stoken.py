import datetime

from .action_base import ActionBase

import datetime
import logging

from .config import Config
from .action_base import ActionBase

config = Config()
log = logging.getLogger(config.log_config['log-name'])


class RequestSessionToken(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(RequestSessionToken, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'request',
            'request': 'session_token',
        }
        return res

    # FETCHERS

    # CORE

    def execute(self, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set()
        return super(RequestSessionToken, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(RequestSessionToken, self).set_values(value_set, *args, **kwargs)

