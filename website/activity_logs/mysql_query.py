import MySQLdb
import datetime
import re
import sys


class Query(object):

    TYPE_RE = re.compile(r'\).*')
    STRING_TYPES = ['varchar', 'text', 'datetime', 'timestamp', 'date', 'time', 'year', 'char', 'blob',
                    'tinyblob', 'tinytext', 'mediumblob', 'mediumtext', 'longblob', 'longtext']
    NUMBER_TYPES = ['int', 'float', 'double', 'decimal', 'tinyint', 'smallint', 'mediumint', 'bigint']

    def __init__(self, conn, table):
        self.conn = conn
        self.table = table
        # used to cache field info for multiple queries to same table
        self.field_information = {}
        # used to determine batch row size
        self.byte_limit = 500000

    def connect_to_db(self, db, create_if_missing=False):
        try:
            self.conn.select_db(db)
        except MySQLdb.DatabaseError:
            if create_if_missing:
                query = 'CREATE DATABASE IF NOT EXISTS {}'.format(db)
                self.execute_query(query)
                self.conn.select_db(db)
            else:
                raise MySQLdb.DatabaseError

    def select_query(self, query):
        with self.conn as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return rows

    def execute_query(self, query):
        with self.conn as cur:
            cur.execute(query)

    def delete_query(self, query):
        with self.conn as cur:
            cur.execute(query)

    def create_table_if_missing(self, create_table_syntax):
        query = 'SHOW TABLES LIKE "{}"'.format(self.table)
        table = self.select_query(query)
        if not table:
            self.execute_query(create_table_syntax)

    def select(self, fields, where=None, limit=None, order_by=None, batch_query=False):
        """
        generate and executes select query
        :param fields: list of fields to select
        :param where: where query, without the 'where' text
        :param limit: optional limit to the query
        :param order_by: optional order by in list format [field, direction]
        :param batch_query: boolean option to batch query or not
        :return: a generator to be used in a loop
        """
        # max execution time of 10 seconds: avoids query killer and
        # also who wants a query running longer than 10 seconds anyways
        query = u"SELECT /*+ MAX_EXECUTION_TIME(10000) */ {} FROM {}".format(u', '.join(fields), self.table)
        if where:
            query = u"{} WHERE {}".format(query, where)
        if order_by:
            query = u"{} ORDER BY {}".format(query, self.create_order_by(order_by))

        # if you don't want a batched query, just run the query
        if not batch_query:
            if limit:
                query = u"{} LIMIT {}".format(query, limit)

            rows = self.select_query(query)
            for row in rows:
                yield row

        # else continue on and batch your query
        else:
            # Find the size of 1 row, and get rows less than byte_limit
            batch_size = self._get_batch_size(query)
            offset = 0

            # if limit is smaller than batch_size, no need to batch
            if limit and limit < batch_size:
                query = u"{} LIMIT {}".format(query, limit)
                rows = self.select_query(query)
                for row in rows:
                    yield row
            else:
                # rewrite query with limit and offset
                rewritten_query = u'{} LIMIT {} OFFSET {}'.format(query, batch_size, offset)
                rows = self.select_query(rewritten_query)

                while rows and self.test_if_limit_hit(limit, offset):
                    # close and open the cursor for each batch
                    for row in rows:
                        yield row
                    offset += batch_size
                    rewritten_query = u'{} LIMIT {} OFFSET {}'.format(query, batch_size, offset)
                    rows = self.select_query(rewritten_query)

    def _get_batch_size(self, query):
        """
        (Private) Method to calculate the appropriate offset count without reading too many rows at once
        :param query:
        :return batch_size:
        """
        # limit 10 because mysql isn't using an index sometimes with a limit of 1
        temp_query = u'{} LIMIT {} OFFSET {}'.format(query, 10, 0)
        with self.conn as cur:
            cur.execute(temp_query)
            row = cur.fetchone()

        if not row:
            # if no rows exit now
            return None

        size_of_one = sys.getsizeof(row)
        # intended to be rounded - can't do anything with floats
        # TODO: cast if run with python3
        batch_size = self.byte_limit / size_of_one
        return batch_size

    def test_if_limit_hit(self, limit, offset):
        if limit is None:
            return True
        elif limit > offset:
            return True
        else:
            return False

    def create_order_by(self, order_by):
        if isinstance(order_by[0], list):
            order_by_string = []
            for order in order_by:
                order_by_string.append(u'{} {}'.format(order[0], order[1]))
            order_by_string = u', '.join(order_by_string)
        else:
            order_by_string = u'{} {}'.format(order_by[0], order_by[1])
        return order_by_string

    def get_table_field_types(self):
        """
        :return: dictionary with fields as keys
        """
        # return cached field info if there
        if self.field_information.get(self.table):
            return self.field_information.get(self.table)

        query = 'DESCRIBE {}'.format(self.table)
        raw_fields = self.select_query(query)
        fields = {}
        for field in raw_fields:
            type_long = field.get('Type').split('(')

            fields[field['Field']] = {'type': type_long[0]}

            if field['Null'] == 'YES':
                null = True
            else:
                null = False
            fields[field['Field']]['null'] = null

            if len(type_long) > 1:
                fields[field['Field']]['length'] = re.sub(self.TYPE_RE, '', type_long[1])

        # cache field info for next time
        self.field_information[self.table] = fields

        return fields

    def insert_update(self, data):
        """
        Insert update mySQL Statement
        :param data: list of data dictionaries
        :return:
        """
        # parse fields and values out of data
        fields = self.get_table_field_types()
        ft, vl = self.create_fields_values_for_query(data, fields)

        # create update list
        update_fields = []
        for field in ft:
            update_fields.append(u"{0}=VALUES({0})".format(field))
        update = u', '.join(update_fields)
        values = u', '.join(vl)
        fields = u'({})'.format(u', '.join(ft))

        query = u"INSERT INTO {} {} VALUES {} ON DUPLICATE KEY UPDATE {}".format(self.table, fields, values, update)
        self.execute_query(query)

    def insert(self, data):
        """
        Insert mySQL Statement
        :param data: list of data dictionaries
        :return:
        """
        # parse fields and values out of data
        fields = self.get_table_field_types()
        ft, vl = self.create_fields_values_for_query(data, fields)

        values = u', '.join(vl)
        fields = u'({})'.format(u', '.join(ft))

        query = u"INSERT INTO {} {} VALUES {}".format(self.table, fields, values)
        self.execute_query(query)

    def create_fields_values_for_query(self, data, field_info):
        """
        :param data: a list of dictionaries
        :param field_info: dictionary of fields
        :return: ft contains tuple of fields; vl are the values in a list (rows) of tuples (row)
        """
        # set fields as fields from the first row
        fields = data[0].keys()
        values = []
        for row in data:
            row_values = []

            # loop through fields because query will break if all rows don't have the same fields
            for field in fields:

                value = row.get(field)
                info = field_info.get(field)

                if value:
                    if isinstance(value, datetime.datetime):
                        value = u'"{}"'.format(value.strftime('%Y-%m-%d %H:%M:%S'))
                    elif info.get('type') in self.STRING_TYPES:
                        value = value.replace('"', "'")
                        value = u'"{}"'.format(value.encode('utf-8'))
                    elif info.get('type') in self.NUMBER_TYPES:
                        value = str(value)
                else:
                    if info.get('null'):
                        value = 'null'
                    else:
                        value = '""'

                row_values.append(value)

            values.append(u'({})'.format(u', '.join(row_values)))

        return fields, values
