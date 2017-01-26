from MySQLdb import connect
from MySQLdb import cursors
from passlib.apps import custom_app_context as pwd_context

from website.utilities.creds import mysql_creds
from website.utilities.mysql_query import Query


class User(object):

    USER_TABLE = 'users'

    def __init__(self, username, password='', name=None):
        self.conn = connect(host=mysql_creds['host'], port=mysql_creds['port'], user=mysql_creds['user'],
                            passwd=mysql_creds['password'], db='blog', cursorclass=cursors.DictCursor)
        self.id = None
        self.hash_pass = pwd_context.encrypt(password)
        self.username = username
        self.name = name

    def validate_username(self):
        valid = False
        if isinstance(self.username, basestring):
            valid = True
        return valid

    def validate_user_info(self, need_name=False):
        if not self.validate_username():
            raise UserException('Invalid Username')
        elif not self.hash_pass:
            raise UserException('Invalid Password')
        elif not self.name and need_name:
            raise UserException('Invalid Name')

    def add_user(self):
        self.validate_user_info(need_name=True)
        data = [{'username': self.username, 'password': self.hash_pass, 'name': self.name}]
        query = Query(self.conn, self.USER_TABLE)
        query.insert_update(data)
        user_info = self.get_user_by_username()
        self.id = user_info.get('id')

    def get_user_by_username(self):
        query = Query(self.conn, self.USER_TABLE)
        rows = query.select(['id', 'password', 'username'], where='username = "{}"'.format(self.username))
        user_info = next(rows, [])
        self.hash_pass = user_info.get('password')
        return user_info

    def check_if_user_exists(self):
        user = self.get_user_by_username()
        if user:
            return True
        return False

    def check_if_authenticated_user(self, password):
        valid = False
        user = self.get_user_by_username()
        if user.get('id'):
            valid_pwd = self.verify_password(password)
            if valid_pwd:
                valid = True
        return valid

    def verify_password(self, password):
        return pwd_context.verify(password, self.hash_pass)


class UserException(Exception):
    def __init__(self, message):
        self.message = message
