from flask import render_template, make_response
from flask_restful import Resource, reqparse
from werkzeug import exceptions

from website.activity_logs import activities

ACTIVITY_PLACEHOLDER = "Please Pick an Activity"


class AddActivity(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        self.activities = activities.Activities()
        self._parser = reqparse.RequestParser(bundle_errors=True)
        self._parser.add_argument('activity', type=str, required=True)
        self._parser.add_argument('date', type=str)
        self._parser.add_argument('activity_time', type=float)

    def get(self):
        activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
        template = render_template('add_activity.html', activity_list=activity_list)
        return make_response(template, 200, self.header)

    def post(self):
        try:
            activity_info = self._parser.parse_args()
        except exceptions.BadRequest as e:
            err_msgs = []
            err_data = e.data
            for field, err in err_data['message'].items():
                err = err.strip()
                err = err.replace(':', '')
                err_msgs.append('Error with {}: {}'.format(field, err))

            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', error=err_msgs, activity_list=activity_list)
            return make_response(template, 400, self.header)

        if activity_info.get('activity') == ACTIVITY_PLACEHOLDER:
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', activity_list=activity_list)
            return make_response(template, 200, self.header)

        if not activity_info.get('date'):
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', activity_list=activity_list,
                                       activity=activity_info.get('activity'))
            return make_response(template, 200, self.header)

        success = self.activities.add_activity(activity_info)

        if success:
            message = "Successfully added activity"
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', alert=message, activity_list=activity_list)
            return make_response(template, 400, self.header)

        else:
            err_msgs = "Failed to add activity"
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', error=err_msgs, activity_list=activity_list)
            return make_response(template, 400, self.header)
