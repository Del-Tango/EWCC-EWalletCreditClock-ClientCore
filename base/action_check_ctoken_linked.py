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


class CheckCTokenLinked(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(CheckCTokenLinked, self).__init__(*args, **kwargs)
        self.instruction_set = {
            'controller': 'client',
            'ctype': 'action',
            'action': 'verify',
            'verify': 'ctoken',
            'ctoken': 'linked',
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
                'ctoken': 'linked',
            }
        }

    def fetch_resource_key_map(self):
        log.debug('')
        return {
            'client_id': 'client-id type-str>',
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
        return super(CheckCTokenLinked, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set()
        return super(CheckCTokenLinked, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        check_illegal_keys = self.check_for_illegal_instruction_set_keys(
            value_set
        )
        if isinstance(check_illegal_keys, dict) and \
                (check_illegal_keys.get('failed') or
                 check_illegal_keys.get('invalid_keys')):
            return self.error_illegal_instruction_set_keys_found(
                kwargs, check_illegal_keys
            )
        return super(CheckCTokenLinked, self).set_values(
            value_set, *args, **kwargs
        )

    # WARNINGS

    def warning_illegal_instruction_set_key_for_resource(self, *args):
        core_response = {
            'failed': True,
            'warning': 'Illegal instruction set key for '
                       'user action handler CheckCTokenLinked. '
                       'Details: {}'.format(args)
        }
        log.warning(core_response['warning'])
        return core_response

    # ERRORS

    def error_illegal_instruction_set_keys_found(self, *args):
        core_response = {
            'failed': True,
            'error': 'Illegal instruction set keys for '
                       'user action handler CheckCTokenLinked. '
                       'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response


