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


class CheckCTokenStatus(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(CheckCTokenStatus, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'verify',
            'verify': 'ctoken',
            'ctoken': 'status',
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
                'ctoken': 'status',
            }
        }

    def fetch_resource_key_map(self):
        log.debug('')
        return {
            'client_id': '<client-id type-str>',
        }

    # CHECKERS

    def check_for_illegal_instruction_set_keys(self, instruction_keys):
        log.debug('')
        valid_resource_keys = list(self.fetch_resource_key_map().keys())
        valid_keys, invalid_keys = [], []
        for key in instruction_keys:
            if key not in valid_resource_keys:
                self.warning_illegal_instruction_set_key_for_resource(
                    instruction_keys, valid_resource_keys
                )
                invalid_keys.append(key)
                continue
            valid_keys.append(key)
        return {
            'failed': False,
            'valid_keys': valid_keys,
            'invalid_keys': invalid_keys,
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(CheckCTokenStatus, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set()
        return super(CheckCTokenStatus, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(CheckCTokenStatus, self).set_values(
            value_set, *args, **kwargs
        )

