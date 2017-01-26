from flask import render_template, make_response
from flask_restful import Resource

from website.activity_logs import activities


class Homepage(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        self.activities = activities.Activities()

    def get(self):
        week_graph = self.activities.get_activities()
        template = render_template('homepage.html', week_graph=week_graph)
        return make_response(template, 200, self.header)
