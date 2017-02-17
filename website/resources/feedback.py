from flask import render_template, make_response, request, flash, redirect, url_for
from flask_restful import Resource

from blog_management import site_feedback
from utilities import utils


class Feedback(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        if utils.is_safe_url(request, request.referrer):
            self.redirect_page = request.referrer
        else:
            self.redirect_page = url_for('homepage')

    def get(self):
        template = render_template('site_feedback.html')
        return make_response(template, 200, self.header)

    def post(self):
        if not request.form:
            flash('Feedback Failed: No form data passed in', 'error')
            return redirect(self.redirect_page)

        feedback = request.form
        success, msg = site_feedback.insert_site_feedback(feedback)
        if not success:
            flash("Feedback Failed: {}".format(msg), 'error')
        else:
            flash(msg)
        return redirect(self.redirect_page)
