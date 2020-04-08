from pymysql import connect, cursors

from utilities.creds import mysql_creds
from utilities.mysql_query import Query


FEEDBACK_TABLE = 'feedback'


def insert_site_feedback(feedback):
    conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                   passwd=mysql_creds['password'], db='blog', cursorclass=cursors.DictCursor)
    q = Query(conn, table=FEEDBACK_TABLE)

    # make sure all fields exist
    email = feedback.get('email')
    date = feedback.get('date')
    text = feedback.get('feedback')
    if not email or not date or not text:
        return False, 'Did not include all needed information'
    # check to see if feedback already given today
    today_feedback = q.select(['id'], where='email = "{}" and DATE(`date`) = DATE("{}")'.format(email, date))
    first_feedback = next(today_feedback, None)
    if first_feedback:
        return False, 'You can only give feedback once a day'
    # insert feedback
    q.insert([feedback])
    return True, "We've received your feedback"
