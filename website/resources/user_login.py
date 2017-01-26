from flask import render_template, make_response, request, session, flash
from flask_restful import Resource

from website.blog_management.User import User, UserException


class Login(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def get(self):
        template = render_template('login.html')
        return make_response(template, 200, self.header)

    def post(self):
        if not request.form:
            template = render_template('login.html', error='No form data passed in')
            return make_response(template, 400, self.header)

        user_info = request.form
        user = User(user_info.get('username'))
        try:
            user.validate_user_info()
        except UserException as e:
            template = render_template('login.html', error=e.message)
            return make_response(template, 400, self.header)
        match = user.check_if_authenticated_user(user_info.get('password'))
        if not match:
            template = render_template('login.html', error='Could not login, check username and password')
            return make_response(template, 400, self.header)

        session['username'] = user_info.get('username')
        session['logged_in'] = True
        template = render_template('login.html', alert='Successful Login')
        return make_response(template, 200, self.header)


class Logout(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def get(self):
        session.pop('logged_in', None)
        session.pop('username', None)
        flash('You were logged out')
        template = render_template('login.html')
        return make_response(template, 200, self.header)
