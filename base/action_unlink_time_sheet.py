import logging

from .config import Config
from .action_base import ActionBase

config = Config(config_file='conf/ewcc.conf')
config.config_init()
log = logging.getLogger(config.log_config['log-name'])


class UnlinkTimeSheet(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(UnlinkTimeSheet, self).__init__(*args, **kwargs)
        default_values = self.fetch_resource_purge_map()
        self.instruction_set = default_values['instruction_set']
        return res

    # FETCHERS

    def fetch_resource_purge_map(self):
        log.debug('')
        return {
            'instruction_set': {
                "controller": "client",
                "ctype": "action",
                "action": "unlink",
                "unlink": "time",
                "time": "list",
            }
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(UnlinkTimeSheet, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        return super(UnlinkTimeSheet, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(UnlinkTimeSheet, self).set_values(
            value_set, *args, **kwargs
        )
