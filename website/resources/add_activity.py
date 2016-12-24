from flask import render_template, make_response
from flask_restful import Resource, reqparse
from werkzeug import exceptions

from website.activity_logs import activities


class AddActivity(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        self.activities = activities.Activities()
        self._parser = reqparse.RequestParser(bundle_errors=True)
        self._parser.add_argument('activity', type=str, required=True)
        self._parser.add_argument('datetime', type=str, required=True)
        self._parser.add_argument('activity_time', type=float, required=True)

    def get(self):
        template = render_template('add_activity.html', activity_list=self.activities.get_activity_list())
        return make_response(template, 200, self.header)

    def post(self):
        try:
            activity = self._parser.parse_args()
        except exceptions.BadRequest as e:
            err_msgs = []
            err_data = e.data
            for field, err in err_data['message'].items():
                err = err.strip()
                err = err.replace(':', '')
                err_msgs.append('Error with {}: {}'.format(field, err))
            template = render_template('add_activity.html', error=err_msgs,
                                       activity_list=self.activities.get_activity_list())
            return make_response(template, 400, self.header)

        return activity

