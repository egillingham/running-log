import logging
from flask import render_template, make_response
from flask_restful import Resource

from blog_management import hearts, charting

LOGGER = logging.getLogger("running-log")


class Hearts(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        self.page = 'hearts'

    def get(self):
        groups = hearts.Groups()
        charts = charting.get_charts_for_page(self.page)
        chart_with_data = []
        for chart in charts:
            if chart.get('activity_function_param'):
                chart['data'] = getattr(groups, chart['activity_function'])(chart.get('activity_function_param'))
            else:
                chart['data'] = getattr(groups, chart['activity_function'])()
            chart_with_data.append(chart)
        template = render_template('hearts.html', groups=groups.get_group_info(), charts=charts)
        return make_response(template, 200, self.header)
