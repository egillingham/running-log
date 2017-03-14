from flask import render_template, make_response
from flask_restful import Resource

from activity_logs import activities


class Homepage(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def get(self):
        template = render_template('homepage.html', welcome=True)
        return make_response(template, 200, self.header)
