from flask import render_template, make_response, request, session
from flask_restful import Resource

from activity_logs import activities


class Activities(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        self.activities = activities.Activities()

    def get(self):
        week_graph = self.activities.get_activities()
        weekly_milage = self.activities.get_weekly_mileage()
        template = render_template('activities.html', week_graph=week_graph, weekly_milage=weekly_milage)
        return make_response(template, 200, self.header)
