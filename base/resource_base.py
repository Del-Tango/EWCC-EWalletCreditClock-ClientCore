import datetime
import logging
import requests
import json

from base64 import b64encode

from .config import Config

config = Config()
log = logging.getLogger(config.log_config['log-name'])


class ResourceBase():

    def __init__(self, *args, **kwargs):
        self.create_date = datetime.datetime.now()
        self.write_date = datetime.datetime.now()
        self.config = kwargs.get('config') or config
        self.instruction_set = dict()
        self.instruction_set_response = dict()
        self.response = None
        self.timestamp = None
        self.status = bool()
        self.previous = str()

    # FETCHERS

    def fetch_resource_values(self):
        log.debug('')
        return {
            'create_date': self.create_date,
            'write_date': self.write_date,
            'instruction_set': self.instruction_set,
            'instruction_set_response': self.instruction_set_response,
            'response': self.response,
            'timestamp': self.timestamp,
            'status': self.status,
            'previous': self.previous,
        }

    def fetch_instruction_set(self):
        log.debug('')
        instruction_set = self.instruction_set
        if not isinstance(instruction_set, dict):
            return self.error_instruction_set_parameter_not_properly_set(
                instruction_set
            )
        elif not instruction_set:
            return self.warning_unpopulated_instruction_set(instruction_set)
        return instruction_set

    def fetch_supported_http_request_methods(self):
        log.debug('')
        return ['POST', 'GET']

    def fetch_action_instruction_set_target_url(self):
        log.debug('')
        return self.config.cloud_config['ewsc-url']

    # FORMATTERS

    def format_master_account_credentials_for_basic_auth(self, login, sequence):
        log.debug('')
        if not isinstance(login, str) or not isinstance(sequence, str):
            return self.error_invalid_basic_http_authorization_credentials(login, sequence)
        master_creds = '{}:{}'.format(login, sequence)
        encoded_creds = master_creds.encode('UTF-8')
        basic_auth_creds = b64encode(encoded_creds).decode('ascii')
        return basic_auth_creds or False

    def format_data_set_for_api_call(self, values):
        log.debug('')
        master_creds = self.format_master_account_credentials_for_basic_auth(
            self.config._fetch_ewsc_master_login(),
            self.config._fetch_ewsc_master_sequence()
        )
        if not master_creds or not isinstance(master_creds, str):
            return self.error_could_not_format_master_account_credentials_for_authorization(
               master_creds
            )
        formatted_values = {
            'Header': {
                'Authorization': 'Basic ' + master_creds,
                'Content-Type': 'application/json',
            },
            'Body': values,
        }
        return formatted_values

    # UPDATERS

    def update_last_executed_instruction_set(self, instruction_set):
        log.debug('')
        try:
            self.instruction_set = instruction_set
        except:
            self.error_could_not_update_last_executed_instruction_set(instruction_set)
            return False
        return True

    def update_last_write_date(self):
        log.debug('')
        try:
            self.write_date = datetime.datetime.now()
        except:
            self.error_could_not_update_last_resource_write_date()
            return False
        return True

    def update_last_ewsc_response_raw(self, response):
        log.debug('')
        try:
            self.response = response
        except:
            self.error_could_not_update_last_ewsc_response_raw(response)
            return False
        return True

    def update_last_ewsc_instruction_set_response(self, response):
        log.debug('')
        try:
            self.instruction_set_response = self.json_to_dictionary_convertor(response.text)
        except:
            self.error_could_not_update_last_ewsc_instruction_set_response(response)
            return False
        return True

    def update_last_ewsc_response_status(self, instruction_set_response):
        log.debug('')
        try:
            self.status = False if instruction_set_response.get('failed') \
                else True
        except:
            self.error_could_not_update_last_ewsc_response_status(
                instruction_set_response
            )
            return False
        return True

    def update_last_instruction_set_execution_timestamp(self):
        log.debug('')
        try:
            self.timestamp = datetime.datetime.now()
        except:
            self.error_could_not_update_last_instruction_set_execution_timestamp()
            return False
        return True

    def update_last_ewsc_response(self, instruction_set, response):
        log.debug('')
        updates = {
            'response': self.update_last_ewsc_response_raw(response),
            'instruction_set': self.update_last_executed_instruction_set(instruction_set),
            'instruction_set_response': self.update_last_ewsc_instruction_set_response(response),
            'status': self.update_last_ewsc_response_status(self.instruction_set_response),
            'timestamp': self.update_last_instruction_set_execution_timestamp(),
            'write_date': self.update_last_write_date()
        }
        return self.warning_could_not_update_last_ewsc_resource_response(response) \
            if False in list(updates.values()) else {
                'failed': False,
                'updates': updates,
            }

    # GENERAL

    def dictionary_to_json_convertor(self, target_dict):
        log.debug('')
        try:
            converted = json.dumps(target_dict)
        except:
            return self.error_could_not_convert_dictonary_to_json(target_dict)
        return converted

    def json_to_dictionary_convertor(self, target_json):
        log.debug('')
        try:
            converted = json.loads(target_json)
        except:
            return self.error_could_not_convert_json_to_dictionary(target_json)
        return converted

    # CLOUD

    def issue_api_call(self, method, target_url, data_set):
        log.debug('')
        supported_request_methods = self.fetch_supported_http_request_methods()
        if method not in supported_request_methods:
            return self.error_unsupported_http_request_method(
                method, target_url, data_set
            )
        try:
            json_payload = self.dictionary_to_json_convertor(data_set['Body'])
            api_call = requests.request(
                method, target_url, headers=data_set['Header'],
                data=json_payload
            )
        except:
            return self.error_could_not_issue_ewsc_api_call(
                method, target_url, data_set
            )
        return api_call

    def process_api_call(self, instruction_set, response):
        log.debug('')
        log.info('EWSC - HTTP Response {} -'.format(response.status_code))
        self.update_last_ewsc_response(instruction_set, response)
        return self.json_to_dictionary_convertor(response.text)

    # CORE

    def response(self, raw=False):
        log.debug('')
        return self.instruction_set_response if not raw else self.response

    def state(self, **kwargs):
        log.debug('')
        state = kwargs.get('state') or {}
        state.update(self.fetch_resource_values())
        return state

    def execute(self, instruction_set):
        log.debug('')
        target_url = self.fetch_action_instruction_set_target_url()
        formatted_data = self.format_data_set_for_api_call(instruction_set)
        api_call = self.issue_api_call('POST', target_url, formatted_data)
        return self.process_api_call(instruction_set, api_call)

    def set_values(self, value_set, *args, **kwargs):
        log.debug('')
        fields_set = []
        for field in value_set:
            try:
                setattr(self, field, value_set[field])
                fields_set.append(field)
            except:
                self.warning_could_not_set_resource_attribute(field)
        return fields_set

    def purge(self):
        log.debug('TODO')

    # WARNINGS

    def warning_unpopulated_instruction_set(self, *args):
        core_response = {
            'failed': True,
            'warning': 'Unpopulated resource instruction set. Details: {}'\
                       .format(args)
        }
        log.error(core_response['warning'])
        return core_response

    def warning_could_not_update_last_ewsc_resource_response(self, response):
        core_response = {
            'failed': True,
            'warning': 'Something went wrong. '
                       'Could not update last EWSC resource response values. '
                       'Details: {}, {}'.format(response, response.text)
        }
        log.warning(core_response['warning'])
        return core_response

    # ERRORS

    def error_could_not_update_last_instruction_set_execution_timestamp(self):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last instruction set execution timestamp.',
        }
        log.error(core_response['error'])
        return core_response

    def error_instruction_set_parameter_not_properly_set(self, *args):
        core_response = {
            'failed': True,
            'error': 'Instruction set parameter not properly set. Details: {}'\
                     .format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_convert_dictionary_to_json(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not convert python dictionary to JSON. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_convert_json_to_dictionary(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not convert JSON to python dictionary. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_ewsc_response_status(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last EWSC instruction set response status. '
                     'Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_executed_instruction_set(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last executed instruction set. '
                     'Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_resource_write_date(self):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update resource write date. '
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_ewsc_response_raw(self, response):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last EWSC raw resource response. '
                     'Details: {}'.format(response)
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_last_ewsc_instruction_set_response(self, response):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not update last EWSC instruction set resource response. '
                     'Details: {}'.format(response),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_issue_ewsc_api_call(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                     'Could not issue API call to EWSC remote machine. '
                     'Details: {}'.format(args)
        }
        log.error(core_response['error'])
        return core_response

    def error_unsupported_http_request_method(self, *args):
        core_response = {
            'failed': True,
            'error': 'Unsupported HTTP request method. Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_invalid_basic_http_authorization_credentials(self, *args):
        core_response = {
            'failed': True,
            'error': 'Invalid HTTP Basic Auth credentials. Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_format_master_account_credentials_for_authorization(self, *args):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. Could not format master account '
                     'credentials for authorization. Details: {}'.format(args),
        }
        log.error(core_response['error'])
        return core_response


