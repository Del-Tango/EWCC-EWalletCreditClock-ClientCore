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
        self.execution_category = str()
        self.previous = str()
        self.previous_action = str()
        self.previous_event = str()

    # FETCHERS

    def fetch_complete_resource_map(self):
        log.debug('')
        resource_map = self.actions.copy()
        resource_map.update(self.events)
        return resource_map

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
            'execute': self.execution_category,
            'previous': self.previous,
            'previous_action': self.previous_action,
            'previous_event': self.previous_event,
        }
        return value_set

    def fetch_action_label_map(self):
        log.debug('')
        action_labels = {
            'RequestClientID': action_request_clientid.RequestClientID,
            'RequestSessionToken': action_request_stoken.RequestSessionToken,
            'PauseClockTimer': action_pause_clock_timer.PauseClockTimer,
            'ResumeClockTimer': action_resume_clock_timer.ResumeClockTimer,
            'StartClockTimer': action_start_clock_timer.StartClockTimer,
            'StopClockTimer': action_stop_clock_timer.StopClockTimer,
            'AccountLogin': action_account_login.AccountLogin,
            'AccountLogout': action_account_logout.AccountLogout,
            'AddContactRecord': action_add_contact_record.AddContactRecord,
            'ConvertClockToCredits': action_convert_clock2credits.ConvertClockToCredits,
            'ConvertCreditsToClock': action_convert_credits2clock.ConvertCreditsToClock,
            'CreateNewAccount': action_create_new_account.CreateNewAccount,
            'CreateContactList': action_create_contact_list.CreateContactList,
            'CreateConversionSheet': action_create_conversion_sheet.CreateConversionSheet,
            'CreateCreditClock': action_create_credit_clock.CreateCreditClock,
            'CreateCreditEWallet': action_create_credit_ewallet.CreateCreditEWallet,
            'CreateInvoiceSheet': action_create_invoice_sheet.CreateInvoiceSheet,
            'CreateTimeSheet': action_create_time_sheet.CreateTimeSheet,
            'CreateTransferSheet': action_create_transfer_sheet.CreateTransferSheet,
            'EditAccount': action_edit_account.EditAccount,
            'PayCredits': action_pay_credits.PayCredits,
            'SupplyCredits': action_supply_credits.SupplyCredits,
            'SwitchActiveSessionUser': action_switch_active_session_user.SwitchActiveSessionUser,
            'SwitchContactList': action_switch_contact_list.SwitchContactList,
            'SwitchConversionSheet': action_switch_conversion_sheet.SwitchConversionSheet,
            'SwitchCreditClock': action_switch_credit_clock.SwitchCreditClock,
            'SwitchCreditEWallet': action_switch_credit_ewallet.SwitchCreditEWallet,
            'SwitchInvoiceSheet': action_switch_invoice_sheet.SwitchInvoiceSheet,
            'SwitchTimeSheet': action_switch_time_sheet.SwitchTimeSheet,
            'SwitchTransferSheet': action_switch_transfer_sheet.SwitchTransferSheet,
            'TransferCredits': action_transfer_credits.TransferCredits,
            'UnlinkAccount': action_unlink_account.UnlinkAccount,
            'UnlinkContactList': action_unlink_contact_list.UnlinkContactList,
            'UnlinkContactRecord': action_unlink_contact_record.UnlinkContactRecord,
            'UnlinkConversionRecord': action_unlink_conversion_record.UnlinkConversionRecord,
            'UnlinkConversionSheet': action_unlink_conversion_sheet.UnlinkConversionSheet,
            'UnlinkCreditClock': action_unlink_credit_clock.UnlinkCreditClock,
            'UnlinkCreditEWallet': action_unlink_credit_ewallet.UnlinkCreditEWallet,
            'UnlinkInvoiceRecord': action_unlink_invoice_record.UnlinkInvoiceRecord,
            'UnlinkInvoiceSheet': action_unlink_invoice_sheet.UnlinkInvoiceSheet,
            'UnlinkTimeRecord': action_unlink_time_record.UnlinkTimeRecord,
            'UnlinkTimeSheet': action_unlink_time_sheet.UnlinkTimeSheet,
            'UnlinkTransferRecord': action_unlink_transfer_record.UnlinkTransferRecord,
            'UnlinkTransferSheet': action_unlink_transfer_sheet.UnlinkTransferSheet,
            'ViewAccount': action_view_account.ViewAccount,
            'ViewContactList': action_view_contact_list.ViewContactList,
            'ViewContactRecord': action_view_contact_record.ViewContactRecord,
            'ViewConversionRecord': action_view_conversion_record.ViewConversionRecord,
            'ViewConversionSheet': action_view_conversion_sheet.ViewConversionSheet,
            'ViewCreditClock': action_view_credit_clock.ViewCreditClock,
            'ViewCreditEWallet': action_view_credit_ewallet.ViewCreditEWallet,
            'ViewInvoiceRecord': action_view_invoice_record.ViewInvoiceRecord,
            'ViewInvoiceSheet': action_view_invoice_sheet.ViewInvoiceSheet,
            'ViewLoginRecords': action_view_login_records.ViewLoginRecords,
            'ViewLogoutRecords': action_view_logout_records.ViewLogoutRecords,
            'ViewTimeRecord': action_view_time_record.ViewTimeRecord,
            'ViewTimeSheet': action_view_time_sheet.ViewTimeSheet,
            'ViewTransferRecord': action_view_transfer_record.ViewTransferRecord,
            'ViewTransferSheet': action_view_transfer_sheet.ViewTransferSheet,
        }
        return action_labels

    # TODO
    def fetch_event_label_map(self):
        log.debug('TODO - Client events not yet supported.')
        event_labels = {}
        return event_labels

    # UPDATERS

    def update_core_state_from_resource(self, target_label, resource_map):
        log.debug('')
        resource_state = resource_map[target_label].state()
        resource_type = self.check_resource_type(target_label)
        if resource_type == 'action':
            resource_state.update({
                'execution_category': 'action',
                'previous': target_label,
                'previous_action': target_label,
            })
        elif resource_type == 'event':
            resource_state.update({
                'execution_category': 'event',
                'previous': target_label,
                'previous_event': target_label,
            })
        else:
            return self.error_invalid_resource_label(target_label)
        return self.set_client_core_values(resource_state)

    def update_write_date(self, **kwargs):
        log.debug('')
        try:
            self.write_date = kwargs.get('write_date') \
                or datetime.datetime.now()
        except:
            return self.error_could_not_update_write_date(kwargs)
        return True

    def update_event_handlers(self, extension):
        log.debug('')
        try:
            self.events.update(extension)
        except:
            return self.error_could_not_update_event_handler_set(extension)
        return True

    def update_action_handlers(self, extension):
        log.debug('')
        try:
            self.actions.update(extension)
        except:
            return self.error_could_not_update_action_handler_set(extension)
        return True

    # CHECKERS

    def check_resource_type(self, target_label):
        log.debug('')
        actions = self.fetch_action_label_map()
        events = self.fetch_event_label_map()
        if target_label in actions.keys():
            return 'action'
        elif target_label in events.keys():
            return 'event'
        self.error_invalid_resource_label(target_label)
        return False

    # COMPUTERS

    def compute_setup_event_handler(self, handler_map):
        log.debug('')
        self.update_event_handlers(handler_map)
        return True

    def compute_setup_action_handler(self, handler_map):
        log.debug('')
        self.update_action_handlers(handler_map)
        return True

    # CORE

    def response_core(self):
        log.debug('')
        return {
            'failed': False,
            'response': {
                'execute': self.execution_category,
                'response': self.response,
                'action': self.previous_action,
                'event': self.previous_event,
                'instruction_set_response': self.instruction_set_response,
            }
        }

#   @pysnooper.snoop()
    def last_response(self, *args, **kwargs):
        log.debug('')
        if not args and not kwargs:
            return self.response_core()
        if not args:
            if kwargs.get('raw'):
                return self.response
            elif kwargs.get('raw') and kwargs['raw'] is False:
                return self.instruction_set_response
        resource_map = self.fetch_complete_resource_map()
        if args[0] not in list(resource_map.keys()):
            return self.error_invalid_resource_label(args[0])
        return resource_map[args[0]](**kwargs)

#   @pysnooper.snoop()
    def execute(self, target_label):
        log.debug('')
        resource_map = self.fetch_complete_resource_map()
        if target_label not in resource_map:
            return self.error_invalid_target_label(target_label)
        execute = resource_map[target_label].execute()
        self.update_core_state_from_resource(target_label, resource_map)
        return execute

    # TODO
    def new_issue_report(self, *args, **kwargs):
        log.debug('TODO - Not yet implemented.')
    def previous(self, *args, **kwargs):
        log.debug('TODO')
    def purge(self, *args, **kwargs):
        log.debug('TODO')

    def set_client_core_config_values(self, value_set):
        log.debug('')
        return self.config.set(value_set)

    def set_client_core_values(self, value_set):
        log.debug('')
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
                'state': self.fetch_ewallet_client_core_values(),
            }

    def set_values(self, target_label, value_set):
        log.debug('')
        if not target_label or isinstance(target_label, str) and \
                target_label == 'Core':
            return self.set_client_core_values(value_set)
        if target_label == 'Config':
            return self.set_client_core_config_values(value_set)
        resource_map = self.fetch_complete_resource_map()
        if target_label not in resource_map:
            return self.error_invalid_target_label(target_label)
        return resource_map[target_label].set(value_set)

    def new_handlers(self, *args, **kwargs):
        log.debug('')
        return self.setup_handlers(*args, **kwargs)

    def new(self, new='handlers', *args, **kwargs):
        log.debug('')
        handlers = {
            'handlers': self.new_handlers,
            'issue-report': self.new_issue_report,
        }
        if new not in handlers:
            return self.error_invalid_target_for_action_new(new)
        return handlers[new](*args, **kwargs)

    def setup_event_handlers(self, events='all', **kwargs):
        log.debug('')
        event_map = self.fetch_event_label_map()
        setup_count = 0
        handler_set = events if isinstance(events, list) \
            else (list(event_map.keys()) if events == 'all' else [])
        for item in handler_set:
            if not item:
                continue
            compute = self.compute_setup_event_handler({
                item: event_map[item](config=self.config)
            })
            if not compute:
                self.warning_could_not_setup_event_handler(item)
                continue
            setup_count += 1
            log.info('Successfully set up event handler for {}.'.format(item))
        event_handlers = self.events
        if setup_count != len(handler_set):
            self.warning_not_all_specified_event_handlers_setup(event_handlers)
        return {
            'failed': False,
            'events': event_handlers,
        }

    def state(self, *args, **kwargs):
        log.debug('')
        return {
            'failed': False,
            'state': self.fetch_ewallet_client_core_values(),
        }

#   @pysnooper.snoop('logs/ewcc.log')
    def setup_action_handlers(self, actions='all', *args, **kwargs):
        log.debug('')
        action_map = self.fetch_action_label_map()
        setup_count = 0
        handler_set = actions if isinstance(actions, list) \
            else (list(action_map.keys()) if actions == 'all' else [])
        for item in handler_set:
            if not item:
                continue
            compute = self.compute_setup_action_handler({
                item: action_map[item](config=self.config)
            })
            if not compute:
                self.warning_could_not_setup_action_handler(item)
                continue
            setup_count += 1
            log.info('Successfully set up action handler for {}.'.format(item))
        action_handlers = self.actions
        if setup_count != len(handler_set):
            self.warning_not_all_specified_action_handlers_setup(action_handlers)
        return {
            'failed': False,
            'actions': action_handlers,
        }

    def setup_all_handlers(self, *args, **kwargs):
        log.debug('')
        return {
            'failed': False,
            'actions': self.setup_action_handlers(actions='all'),
            'events': self.setup_event_handlers(events='all'),
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
            'failed': False,
            'actions': self.actions,
            'events': self.events,
        }

    # WARNINGS

    def warning_could_not_set_client_core_attribute(self, attribute):
        core_response = {
            'failed': True,
            'warning': 'Something went wrong. '
                'Could not set client core attribute {}.'.format(attribute),
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_no_client_core_fields_set(self, value_set):
        core_response = {
            'failed': True,
            'warning': 'No client core fields updated from value set {}.'\
                .format(value_set),
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_could_not_setup_event_handler(self, event_label):
        core_response = {
            'failed': True,
            'warning': 'Could not setup event handler for client event {}.'\
                .format(event_label),
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_not_all_specified_event_handlers_setup(self, event_handlers):
        core_response = {
            'failed': True,
            'warning': 'Something went wrong. '
                'Could not setup all specified event handlers. '
                'Details: {}'.format(event_handlers),
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_invalid_handler(self, handler_label):
        core_response = {
            'failed': True,
            'warning': 'Invalid handler {}.'.format(handler_label),
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_could_not_setup_action_handler(self, action_label):
        core_response = {
            'failed': True,
            'warning': 'Could not setup action handler for client action {}.'\
                .format(action_label),
        }
        log.warning(core_response['warning'])
        return core_response

    def warning_not_all_specified_action_handlers_setup(self, action_handlers):
        core_response = {
            'failed': True,
            'warning': 'Something went wrong. '
                'Could not setup all specified action handlers. '
                'Details: {}'.format(action_handlers),
        }
        log.warning(core_response['warning'])
        return core_response

    # ERRORS

    def error_invalid_resource_label(self, resource_label):
        core_response = {
            'failed': True,
            'error': 'Invalid resource label {}.'.format(resource_label),
        }
        log.error(core_response['error'])
        return core_response

    def error_invalid_target_label(self, target_label):
        core_response = {
            'failed': True,
            'error': 'Invalid target label {}.'.format(target_label),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_event_handler_set(extension):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                'Could not update EWCC event handler set. '\
                'Details: {}'.format(extension),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_action_handler_set(extension):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                'Could not update EWCC action handler set. '\
                'Details: {}'.format(extension),
        }
        log.error(core_response['error'])
        return core_response

    def error_could_not_update_write_date(self, details):
        core_response = {
            'failed': True,
            'error': 'Something went wrong. '
                'Could not update EWCC write date. '\
                'Details: {}'.format(details),
        }
        log.error(core_response['error'])
        return core_response

    def error_invalid_target_for_action_new(self, target):
        core_response = {
            'failed': True,
            'error': 'Invalid target for action new {}.'.format(target),
        }
        log.error(core_response['error'])
        return core_response

    def error_invalid_handler_value_set(self, *args, **kwargs):
        core_response = {
            'failed': True,
            'error': 'Invalid handler value set. Details: {}, {}'
                .format(args, kwargs),
        }
        log.error(core_response['error'])
        return core_response
