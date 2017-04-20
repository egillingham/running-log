from flask import render_template, make_response, request, session
from flask_restful import Resource

from activity_logs import activities
from blog_management import charting


class Activities(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        self.activities = activities.Activities()
        self.page = 'activities'

    def get(self):
        charts = charting.get_charts_for_page(self.page)
        chart_with_data = []
        for chart in charts:
            chart['data'] = getattr(self.activities, chart['activity_function'])()
            chart_with_data.append(chart)
        template = render_template('activities.html', charts=chart_with_data)
        return make_response(template, 200, self.header)
