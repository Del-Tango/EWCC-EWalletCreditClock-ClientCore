import datetime
import configparser
import logging
import pysnooper
import os

config = configparser.ConfigParser()
config._interpolation = configparser.ExtendedInterpolation()


class Config():

    def __init__(self, *args, **kwargs):
        self.config_timestamp = datetime.datetime.now()
        self.config_file = kwargs.get('config_file')
        self.client_config = kwargs.get('client_config') or {}
        self.log_config = kwargs.get('log_config') or {}
        self.cloud_config = kwargs.get('cloud_config') or {}
        self.initialized = None if not self.config_file else \
            self.config_init()

    # FETCHERS

    def fetch_config_purge_map(self, *args, **kwargs):
        value_set = {
            'config_timestamp': datetime.datetime.now(),
            'config_file': str(),
            'client_config': dict(),
            'log_config': dict(),
            'cloud_config': dict(),
        }
        return value_set

    def _fetch_ewsc_certificate(self):
        return self.cloud_config.get('ewsc-cert')

    def _fetch_ewsc_master_login(self):
        return self.cloud_config.get('ewsc-master-login')

    def _fetch_ewsc_master_sequence(self):
        return self.cloud_config.get('ewsc-master-sequence')

#   @pysnooper.snoop()
    def fetch_settings(self):
        settings = {
            'config_timestamp': self.config_timestamp,
            'config_file': self.config_file,
            'client_config': self.client_config,
            'log_config': self.log_config,
            'cloud_config': self.sanitize_cloud_config_section(),
        }
        return settings

    # SETUP

#   @pysnooper.snoop()
    def config_init(self, config_file=None):
        if not self.config_file:
            if not config_file or not isinstance(config_file, str):
                return False
            self.config_file = config_file
        config.read(self.config_file)
        if not config:
            return False
        if config['ClientDetails']:
            self.client_config = {
                'debug': config['ClientDetails'].get('debug') or False
            }
        if config['LogDetails']:
            self.log_config = {
                'log-name': config['LogDetails'].get('log_name') or 'EWClientCore',
                'log-level': config['LogDetails'].get('log_level') or 'DEBUG',
                'log-dir': config['LogDetails'].get('log_dir') or 'logs',
                'log-file': config['LogDetails'].get('log_file') or 'ewcc.log',
                'log-path': config['LogDetails'].get('log_path') or 'logs/ewcc.log',
                'log-record-format': '[ %(asctime)s ] %(name)s '
                    '[ %(levelname)s ] - %(filename)s - %(lineno)d: '
                    '%(funcName)s - %(message)s',
                'log-date-format': "%d-%m-%Y %H:%M:%S",
            }
        if config['CloudDetails']:
            self.cloud_config = {
                'ewsc-address': config['CloudDetails'].get('ewsc_address') or
                    'https://alvearesolutions.com',
                'ewsc-port': int(config['CloudDetails'].get('ewsc_port')) or 80,
                'ewsc-url': config['CloudDetails'].get('ewsc_url') or
                    '/ewallet/instruction-set',
                'ewsc-cert': config['CloudDetails'].get('ewsc_cert'),
                'ewsc-master-login': config['CloudDetails'].get('ewsc_master_login'),
                'ewsc-master-sequence': config['CloudDetails'].get('ewsc_master_sequence'),
            }
        return True

#   @pysnooper.snoop()
    def log_init(self):
        if not self.config_file:
            return False
        log = logging.getLogger(self.log_config.get('log-name') or __name__)
        log.setLevel(logging.DEBUG)
        if not self.log_config or not self.log_config.get('log_path'):
            config_reload = self.config_reload(self.config_file)
            if not config_reload or isinstance(config_reload, dict) and \
                    config_reload.get('failed') or not self.log_config:
                return False
        file_handler = logging.FileHandler(self.log_config['log-path'], 'a')
        formatter = logging.Formatter(
            self.log_config['log-record-format'],
            self.log_config['log-date-format'],
        )
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        return log

    # SANITIZERS

#   @pysnooper.snoop()
    def sanitize_cloud_config_section(self):
        cloud_config = self.cloud_config.copy()
        for item in ['ewsc-cert', 'ewsc-master-login', 'ewsc-master-sequence']:
            if item in cloud_config:
                del cloud_config[item]
        return cloud_config

    # CORE

    def config_reload(self, *args, **kwargs):
        if not args:
            return self.error_no_config_reload_target_specified(args, kwargs)
        if not os.path.isfile(args[0]):
            return self.warning_config_reload_target_not_a_file(args, kwargs)
        self.config_file = None
        config_reload = self.config_init(config_file=args[0])
        return self.warning_could_not_reload_settings(args, kwargs) \
            if not config_reload else {
                'failed': False,
                'config': self.fetch_settings()
            }

    def purge(self, *args, **kwargs):
        purge_map = self.fetch_config_purge_map()
        purge_fields = kwargs.get('purge') or purge_map.keys()
        value_set = {item: purge_map[item] for item in purge_fields}
        return self.set_values(value_set)

    def set_values(self, value_set):
        fields_set = []
        for field in value_set:
            try:
                setattr(self, field, value_set[field])
                fields_set.append(field)
            except:
                self.warning_could_not_set_client_core_config_attribute(field)
        return self.warning_no_client_core_config_fields_set(value_set) \
            if not fields_set else {
                'failed': False,
                'updated': fields_set,
                'config': self.fetch_settings(),
            }

    # WARNINGS

    def warning_could_not_reload_settings(self, *args):
        core_response = {
            'failed': True,
            'level': 'core-config',
            'warning': 'Something went wrong. '
                       'Could not reload settings from configurations file. '
                       'Details: {}'.format(args)
        }
        return core_response

    def warning_config_reload_target_not_a_file(self, *args):
        core_response = {
            'failed': True,
            'level': 'core-config',
            'warning': 'Config reload target is not a file. Details: {}'.format(args)
        }
        return core_response

    def warning_no_client_core_config_fields_set(self, *args):
        core_response = {
            'failed': True,
            'level': 'core-config',
            'warning': 'No client core config settings updated. Details: {}'\
                       .format(args),
        }
#       self.log.warning(core_response['warning'])
        return core_response

    def warning_could_not_set_client_core_config_attribute(self, *args):
        core_response = {
            'failed': True,
            'level': 'core-config',
            'warning': 'Something went wrong. '
                       'Could not set client core config attribute. Details: {}'\
                       .format(args),
        }
#       self.log.warning(core_response['warning'])
        return core_response

    # ERRORS

    def error_no_config_reload_target_specified(self, *args):
        core_response = {
            'failed': True,
            'level': 'core-config',
            'error': 'No config reload target specified. Details: {}'.format(args)
        }
#       log.error(core_response['error'])
        return core_response

    # CODE DUMP


