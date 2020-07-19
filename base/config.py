import datetime
import configparser
import logging

config = configparser.ConfigParser()
config._interpolation = configparser.ExtendedInterpolation()

class Config():

    def __init__(self, *args, **kwargs):
        self.config_timestamp = datetime.datetime.now()
        self.config_file = kwargs.get('config_file') or 'conf/ewcc.conf'
        config.read(self.config_file)
        self.log = logging.getLogger(config['LogDetails']['log_name'])

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

        self.cloud_config = {
            'ewsc-address': config['CloudDetails'].get('ewsc_address') or
                'https://alvearesolutions.com',
            'ewsc-port': int(config['CloudDetails'].get('ewsc_port')) or 80,
            'ewsc-url': config['CloudDetails'].get('ewsc_url') or
                '/ewallet/instruction-set',
            'ewsc-cert': config['CloudDetails'].get('ewsc_cert'),
            'ewsc-master-login': config['CloudDetails'].get('ewsc_master_login'),
            'ewsc-master-sequence': config['CloudDetails'].get('ewsc_master_login'), # Probably base64 encoded <login>:<pass>
        }

    # FETCHERS

    def _fetch_ewsc_certificate(self):
        self.log.debug('')
        return self.cloud_config.get('ewsc-cert')

    def _fetch_ewsc_master_login(self):
        self.log.debug('')
        return self.cloud_config.get('ewsc-master-login')

    def _fetch_ewsc_master_sequence(self):
        self.log.debug('')
        return self.cloud_config.get('ewsc-master-sequence')

    def fetch_settings(self):
        self.log.debug('')
        settings = {
            'config_timestamp': self.config_timestamp,
            'config_file': self.config_file,
            'log_config': self.log_config,
            'cloud_config': self.sanitize_cloud_config_section(),
        }
        return settings

    # SANITIZERS

    def sanitize_cloud_config_section(self):
        self.log.debug('')
        cloud_config = self.cloud_config.copy()
        for item in ['ewsc-cert', 'ewsc-master-login', 'ewsc-master-sequence']:
            del cloud_config[item]
        return cloud_config

    # CORE

    def set(self, value_set):
        self.log.debug('')
        fields_set = []
        for field in value_set:
            try:
                setattr(self, field, value_set[field])
                fields_set.append(field)
            except:
                self.warning_could_not_set_client_core_attribute(field)
        return self.warning_no_client_core_fields_set(value_set) \
            if not fields_set else {
                'failed': False,
                'updated': fields_set,
                'config': self.fetch_settings(),
            }
