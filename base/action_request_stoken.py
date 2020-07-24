import datetime

from .action_base import ActionBase

import datetime
import logging

from .config import Config
from .action_base import ActionBase

config = Config(config_file='conf/ewcc.conf')
config.config_init()
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

    def fetch_resource_purge_map(self):
        log.debug('')
        return {
            'instruction_set': {
                'controller': 'client',
                'ctype': 'action',
                'action': 'request',
                'request': 'session_token',
            }
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(RequestSessionToken, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set()
        return super(RequestSessionToken, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(RequestSessionToken, self).set_values(value_set, *args, **kwargs)

