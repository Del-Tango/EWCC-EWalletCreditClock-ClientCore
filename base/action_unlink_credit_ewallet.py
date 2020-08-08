import logging

from .config import Config
from .action_base import ActionBase

config = Config(config_file='conf/ewcc.conf')
config.config_init()
log = logging.getLogger(config.log_config['log-name'])


class UnlinkCreditEWallet(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(UnlinkCreditEWallet, self).__init__(*args, **kwargs)
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
                "unlink": "credit",
                "credit": "ewallet",
            }
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(UnlinkCreditEWallet, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        return super(UnlinkCreditEWallet, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(UnlinkCreditEWallet, self).set_values(
            value_set, *args, **kwargs
        )
