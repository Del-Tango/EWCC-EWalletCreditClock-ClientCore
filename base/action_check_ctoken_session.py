import datetime
import logging

from .config import Config
from .action_base import ActionBase

config_file = __name__.split('.')
config_file.remove(config_file[-1])
config_file.remove(config_file[-1])
file_path = 'conf/ewcc.conf' if not config_file else \
    '/'.join(item for item in config_file) + 'conf/ewcc.conf'
config = Config(config_file=file_path)
config.config_init(config_file=file_path)
log = logging.getLogger(config.log_config.get('log-name') or __name__)


class CheckCTokenSession(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(CheckCTokenSession, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'verify',
            'verify': 'ctoken',
            'ctoken': 'session',
        }
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('')
        return {
            'instruction_set': {
                'controller': 'client',
                'ctype': 'action',
                'action': 'verify',
                'verify': 'ctoken',
                'ctoken': 'session',
            }
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(CheckCTokenSession, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set()
        return super(CheckCTokenSession, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(CheckCTokenSession, self).set_values(
            value_set, *args, **kwargs
        )

