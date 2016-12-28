from MySQLdb import connect
from MySQLdb import cursors

from website.utilities.creds import mysql_creds
from website.utilities.mysql_query import Query


class Activities(object):

    def __init__(self):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db='logs', cursorclass=cursors.DictCursor)
        self.activity_lookup = self.get_activity_list()
        self.activity_list = list(self.activity_lookup.keys())

    def get_activity_list(self):
        query = Query(self.conn, 'key_values')
        activities = query.select(['field_key', 'field_value'], where="field = 'activity'")

        activity_lookup = {}
        for activity in activities:
            activity_lookup[activity['field_value']] = int(activity['field_key'])

        return activity_lookup

    def add_activity(self, activity_info):
        # write to activity log
        activity_log_data = {k: v for (k, v) in activity_info.items() if k in ['date', 'activity']}
        # if no activity data, return
        if not activity_log_data:
            return False
        activity = self.activity_lookup[activity_info.get('activity')]
        activity_log_data['activity'] = activity
        query = Query(self.conn, 'activity_log')
        query.insert_update([activity_log_data])

        return True
