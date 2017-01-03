from MySQLdb import connect
from MySQLdb import cursors
from collections import OrderedDict

from website.utilities.creds import mysql_creds
from website.utilities.mysql_query import Query

FIELD_INFO_TABLE = 'field_info'
KEY_VALUE_TABLE = 'key_values'
ACTIVITY_LOG_TABLE = 'activity_log'
RUNNING_LOG_TABLE = 'running_log'


class Activities(object):

    def __init__(self):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db='logs', cursorclass=cursors.DictCursor)
        self.activity_lookup = self.get_activity_list()
        self.activity_list = list(self.activity_lookup.keys())
        self.fields_lists = {}

    def get_key_value_pair(self, field):
        query = Query(self.conn, KEY_VALUE_TABLE)
        key_values = query.select(['field_key', 'field_value'], where="field = '{}'".format(field))
        return key_values

    def get_activity_list(self):
        activities = self.get_key_value_pair('activity')
        activity_lookup = {}
        for activity in activities:
            activity_lookup[activity['field_value']] = int(activity['field_key'])

        return activity_lookup

    def get_fields(self, table):
        query = Query(self.conn, FIELD_INFO_TABLE)
        field_info_fields = ['field']
        fields = query.select(field_info_fields, where="field_table = '{}'".format(table))
        # cache fields for later
        fields = [row.get('field') for row in fields]
        self.fields_lists[table] = fields
        return fields

    def get_form_fields(self, table, seen_list=None):
        query = Query(self.conn, FIELD_INFO_TABLE)
        field_info_fields = ['field, display_name, form_type, form_order, form_value, placeholder', 'normalized']
        fields = query.select(field_info_fields, where="field_table = '{}'".format(table))
        if not seen_list:
            # if seen list is not passed in, start a new one
            seen_list = []
        form_fields = []
        insert_fields = []
        for field in fields:
            # add field to insert fields list, to be set to the class to be used later if needed
            insert_fields.append(field.get('field'))
            # for the rest: ignore fields that have been seen or don't have a form order (aren't in form yet)
            if field in seen_list or not field.get('form_order'):
                continue

            seen_list.append(field)
            if field.get('normalized'):
                # if field is normalized, get the list of values from key values table
                values = self.get_key_value_pair(field.get('field'))
                values = [row.get('field_value') for row in values]
                field['form_value'] = values
            # append field to final form fields dict
            form_fields.append(field)

        # set insert list to class
        self.fields_lists[table] = insert_fields
        # order fields into desired order
        form_fields = sorted(form_fields, key=lambda k: k['form_order'])
        # return seen list so it can be used by another form creation
        return form_fields, seen_list

    def get_activity_fields(self):
        form_fields, seen_list = self.get_form_fields(ACTIVITY_LOG_TABLE)
        return form_fields

    def get_run_fields(self):
        general_fields, seen_list = self.get_form_fields(ACTIVITY_LOG_TABLE)
        run_fields, seen_list2 = self.get_form_fields(RUNNING_LOG_TABLE, seen_list)
        return general_fields, run_fields

    def add_activity(self, activity_info):
        # write to activity log
        activity_fields = self.fields_lists.get(ACTIVITY_LOG_TABLE, self.get_fields(ACTIVITY_LOG_TABLE))
        activity_log_data = {k: v for (k, v) in activity_info.items() if k in activity_fields}
        # if no activity data, return
        if not activity_log_data or not activity_log_data.get('date') or not activity_log_data.get('activity'):
            return False
        activity = self.activity_lookup[activity_info.get('activity')]
        activity_log_data['activity'] = activity
        query = Query(self.conn, ACTIVITY_LOG_TABLE)
        query.insert_update([activity_log_data])

        if activity == 1:
            # write to running log
            run_fields = self.fields_lists.get(RUNNING_LOG_TABLE, self.get_fields(RUNNING_LOG_TABLE))
            run_log_data = {k: v for (k, v) in activity_info.items() if k in run_fields}
            # if no activity data, return
            if not run_log_data or not run_log_data.get('date'):
                return False
            # change terrain back to keys
            if run_log_data.get('terrain'):
                terrain = self.get_key_value_pair('terrain')
                terrain_lookup = {row.get('field_value'): int(row.get('field_key')) for row in terrain}
                run_log_data['terrain'] = terrain_lookup[run_log_data['terrain']]
            query = Query(self.conn, RUNNING_LOG_TABLE)
            query.insert_update([run_log_data])

        return True