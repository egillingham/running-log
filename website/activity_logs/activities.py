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

    ACTIVITY_FIELDS = ['activity', 'date', 'sick', 'traveling', 'latitude', 'longitude']
    ACTIVITY_FORM_FIELDS = OrderedDict({'date': {'title': 'Date Time', 'type': 'datetime-local', 'order': 1},
                                        'sick': {'title': 'Currently Sick?', 'type': 'checkbox', 'value': True,
                                                 'order': 2},
                                        'traveling': {'title': 'Currently Traveling?', 'type': 'checkbox',
                                                      'value': True, 'order': 3},
                                        'latitude': {'title': 'Latitude', 'type': 'number', 'order': 4},
                                        'longitude': {'title': 'Longitude', 'type': 'number', 'order': 5}
                            })
    RUNNING_FIELDS = ['date', 'miles', 'minutes', 'feeling', 'extras', 'description', 'terrain', 'course',
                      'course_description', 'miles_approx', 'minutes_approx', 'stretch', 'workout']
    RUNNING_FORM_FIELDS = OrderedDict({})

    def __init__(self):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db='logs', cursorclass=cursors.DictCursor)
        self.activity_lookup = self.get_activity_list()
        self.activity_list = list(self.activity_lookup.keys())

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

    def get_form_fields(self, table, seen_list=None):
        where = "field_table = '{}'".format(table)
        query = Query(self.conn, FIELD_INFO_TABLE)
        field_info_fields = ['field, display_name, form_type, form_order, form_value, placeholder', 'normalized']
        fields = query.select(field_info_fields, where=where)
        if not seen_list:
            seen_list = []
        form_fields = []
        for field in fields:
            if field in seen_list or not field.get('form_order'):
                continue

            seen_list.append(field)
            if field.get('normalized'):
                values = self.get_key_value_pair(field.get('field'))
                values = [row.get('field_value') for row in values]
                field['form_value'] = values
            form_fields.append(field)

        form_fields = sorted(form_fields, key=lambda k: k['form_order'])
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
        activity_log_data = {k: v for (k, v) in activity_info.items() if k in self.ACTIVITY_FIELDS}
        # if no activity data, return
        if not activity_log_data or not activity_log_data.get('date') or not activity_log_data.get('activity'):
            return False
        activity = self.activity_lookup[activity_info.get('activity')]
        activity_log_data['activity'] = activity
        query = Query(self.conn, ACTIVITY_LOG_TABLE)
        query.insert_update([activity_log_data])

        return True
