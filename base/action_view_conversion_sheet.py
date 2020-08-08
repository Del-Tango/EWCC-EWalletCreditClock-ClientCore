import logging

from .config import Config
from .action_base import ActionBase

config_file = __name__.split('.')
config_file.remove(config_file[-1])
config_file.remove(config_file[-1])
file_path = '/'.join(item for item in config_file) + '/conf/ewcc.conf'
config = Config(config_file=file_path)
config.config_init(config_file=file_path)
log = logging.getLogger(config.log_config.get('log-name') or __name__)


class ViewConversionSheet(ActionBase):

    def __init__(self, *args, **kwargs):
        res = super(ViewConversionSheet, self).__init__(*args, **kwargs)
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
                "action": "view",
                "view": "conversion",
                "conversion": "list",
            }
        }

    # CORE

    def purge(self, *args, **kwargs):
        log.debug('')
        purge_map = self.fetch_resource_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        return super(ViewConversionSheet, self).purge(
            *args, purge=purge_fields, purge_map=purge_map
        )

    def execute(self, *args, **kwargs):
        log.debug('')
        instruction_set = self.fetch_instruction_set() \
            if not args or not isinstance(args[0], dict) else args[0]
        return super(ViewConversionSheet, self).execute(instruction_set)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        return super(ViewConversionSheet, self).set_values(
            value_set, *args, **kwargs
        )
