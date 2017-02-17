from flask import render_template, make_response, request, session, flash, redirect, url_for
from flask_restful import Resource

from blog_management.User import User, UserException
from utilities import utils


class Login(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        if utils.is_safe_url(request, request.referrer):
            self.redirect_page = request.referrer
        else:
            self.redirect_page = url_for('homepage')

    def get(self):
        template = render_template('login.html')
        return make_response(template, 200, self.header)

    def post(self):
        if not request.form:
            flash('No form data passed in', 'error')
            return redirect(self.redirect_page)

        user_info = request.form
        user = User(user_info.get('username'))
        try:
            user.validate_user_info()
        except UserException as e:
            flash(e.message, 'error')
            return redirect(self.redirect_page)
        match = user.check_if_authenticated_user(user_info.get('password'))
        if not match:
            flash('Could not login, check username and password', 'error')
            return redirect(self.redirect_page)

        session['username'] = user_info.get('username')
        session['logged_in'] = True
        flash('Successful Login')
        return redirect(self.redirect_page)


class Logout(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        if utils.is_safe_url(request, request.referrer):
            self.redirect_page = request.referrer
        else:
            self.redirect_page = url_for('homepage')

    def get(self):
        if session.get('logged_in'):
            session.pop('logged_in', None)
            session.pop('username', None)
            flash('You are logged out')
            return redirect(self.redirect_page)
        else:
            return make_response(render_template('login.html'), 200, self.header)
