from MySQLdb import connect, cursors

from utilities.creds import mysql_creds
from utilities.mysql_query import Query


def get_charts_for_page(render_page):
    conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                   passwd=mysql_creds['password'], db='blog', cursorclass=cursors.DictCursor)
    q = Query(conn, table='charts')
    charts = q.select(fields=['*'], where='render_page = "{}"'.format(render_page))
    return charts
