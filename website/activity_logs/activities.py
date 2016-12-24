from MySQLdb import connect
from MySQLdb import cursors

from mysql_query import Query
from creds import mysql_creds


class Activities(object):

    def __init__(self):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db=mysql_creds['db'], cursorclass=cursors.DictCursor)
        self.activity_lookup = self.get_activity_list()
        self.activity_list = list(self.activity_lookup.values())

    def get_activity_list(self):
        query = Query(self.conn, 'key_values')
        activities = query.select(['field_key', 'field_value'], where="field = 'activity_type'")

        activity_lookup = {}
        for activity in activities:
            activity_lookup[activity['field_key']] = activity['field_value']

        return activity_lookup
