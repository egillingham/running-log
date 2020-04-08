from pymysql import connect, cursors

from utilities.creds import mysql_creds
from utilities.mysql_query import Query


def get_image_cards():
    conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                   passwd=mysql_creds['password'], db='blog', cursorclass=cursors.DictCursor)
    q = Query(conn, table='image_cards')
    cards = q.select(fields=['img_order', 'img', 'img_text'], order_by=['img_order', 'ASC'])
    return cards
