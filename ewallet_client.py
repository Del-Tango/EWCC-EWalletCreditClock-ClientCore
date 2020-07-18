import datetime
import time
import json
import requests
import logging
import pysnooper

from base.config import Config
from base import *


def log_init():
    log_config = Config().log_config
    log = logging.getLogger(log_config['log-name'])
    log.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_config['log-path'], 'a')
    formatter = logging.Formatter(
        log_config['log-record-format'],
        log_config['log-date-format'],
    )
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    return log


log = log_init()


class EWalletClientCore():

    def __init__(self, *args, **kwargs):
        self.create_date = datetime.datetime.now()
        self.write_date = datetime.datetime.now()
        self.actions = dict()
        self.events = dict()
        self.status = bool()
        self.instruction_set = dict()
        self.instruction_set_response = dict()
        self.response = None
        self.timestamp = None
        self.config_file = kwargs.get('config_file') or 'conf/ewcc.conf'
        self.config = Config(config_file=self.config_file)
        self.previous_action = str()
        self.previous_event = str()

    # FETCHERS

    def fetch_ewallet_client_core_values(self):
        log.debug('')
        value_set = {
            'create_date': self.create_date,
            'write_date': self.write_date,
            'actions': self.actions,
            'events': self.events,
            'status': self.status,
            'instruction_set': self.instruction_set,
            'instruction_set_response': self.instruction_set_response,
            'response': self.response,
            'timestamp': self.timestamp,
            'config_file': self.config_file,
            'config': self.config.fetch_settings(),
            'previous_action': self.previous_action,
            'previous_event': self.previous_event,
        }
        return value_set

    def fetch_action_label_map(self):
        log.debug('TODO - Not all available actions supported.')
        action_labels = {
            'RequestClientID': action_request_clientid.RequestClientID,
            'RequestSessionToken': action_request_stoken.RequestSessionToken,
        }
        return action_labels

    # UPDATERS

    def update_action_handlers(self, extension):
        log.debug('')
        self.actions.update(extension)
        return True

    # COMPUTERS

    def compute_setup_action_handler(self, handler_map):
        log.debug('')
        self.update_action_handlers(handler_map)
        return True

    # CORE

    # TODO
    def setup_event_handlers(self, event_set):
        log.debug('TODO - Events not yet supported.')

    def state(self, *args, **kwargs):
        log.debug('')
        return self.fetch_ewallet_client_core_values()

#   @pysnooper.snoop('logs/ewcc.log')
    def setup_action_handlers(self, *args, **kwargs):
        log.debug('')
        action_map = self.fetch_action_label_map()
        setup_count = 0
        for item in kwargs.get('actions'):
            compute = self.compute_setup_action_handler({
                item: action_map[item]()
            })
            if not compute:
                self.warning_could_not_setup_action_handler(item)
                continue
            setup_count += 1
            log.info('Successfully set up action handler for {}.'.format(item))
        action_handlers = self.actions
        if setup_count != len(kwargs.get('actions')):
            self.warning_not_all_specified_action_handlers_setup(action_handlers)
        return action_handlers

    def setup_all_handlers(self, *args, **kwargs):
        log.debug('')
        return {
            'actions': self.setup_action_handlers(*args, **kwargs),
            'events': self.setup_event_handlers(*args, **kwargs),
        }

#   @pysnooper.snoop('logs/ewcc.log')
    def setup_handlers(self, *args, **kwargs):
        log.debug('')
        handlers = {
            'action': self.setup_action_handlers,
            'event': self.setup_event_handlers,
        }
        if not kwargs.get('handlers'):
            return self.setup_all_handlers(*args, **kwargs)
        elif not isinstance(kwargs.get('handlers'), list):
            return self.error_invalid_handler_value_set(*args, **kwargs)
        for item in kwargs['handlers']:
            if item not in handlers:
                self.warning_invalid_handler(item)
                continue
            handlers[item](*args, **kwargs)
        return {
            'actions': self.actions,
            'events': self.events,
        }

    def new(self, *args, **kwargs):
        log.debug('TODO')
    def set(self, *args, **kwargs):
        log.debug('TODO')
    def exec(self, *args, **kwargs):
        log.debug('TODO')
    def previous(self, *args, **kwargs):
        log.debug('TODO')
    def purge(self, *args, **kwargs):
        log.debug('TODO')

    # WARNINGS

    def warning_invalid_handler(self, handler_label):
        log.warning('Invalid handler {}.'.format(handler_label))
        return False

    def warning_could_not_setup_action_handler(self, action_label):
        log.warning(
            'Could not setup action handler for client action {}.'\
            .format(action_label)
        )
        return False

    def warning_not_all_specified_action_handlers_setup(self, action_handlers):
        log.warning(
            'Something went wrong. Could not set up all specified action handlers. '
            'Details: {}'.format(action_handlers)
        )
        return False

    # ERRORS

    def error_invalid_handler_value_set(self, *args, **kwargs):
        log.error(
            'Invalid handler value set. Details: {}, {}'.format(args, kwargs)
        )
        return False
