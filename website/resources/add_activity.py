from flask import render_template, make_response, request, session
from flask_restful import Resource

from website.activity_logs import activities

ACTIVITY_PLACEHOLDER = "Please Pick an Activity"


class AddActivity(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}
        self.activities = activities.Activities()

    def get(self):
        activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
        template = render_template('add_activity.html', activity_list=activity_list)
        return make_response(template, 200, self.header)

    def post(self):
        test = session.get('logged_in')
        if request.form:
            param = request.form
            # to dict "flattens" the form- may lose a value if duplicate keys. Not really sure how that would happen.
            # (source: http://werkzeug.pocoo.org/docs/0.11/datastructures/#werkzeug.datastructures.MultiDict.to_dict)
            activity_info = param.to_dict()
            if not activity_info:
                activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
                error = 'Error sending activity info'
                template = render_template('add_activity.html', error=[error], activity_list=activity_list)
                return make_response(template, 400, self.header)
        else:
            try:
                activity_info = request.get_json(force=True)
            except Exception as e:
                activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
                template = render_template('add_activity.html', error=[e.message], activity_list=activity_list)
                return make_response(template, 400, self.header)

        if activity_info.get('activity') == ACTIVITY_PLACEHOLDER:
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', activity_list=activity_list)
            return make_response(template, 200, self.header)

        if not activity_info.get('date'):
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            activity = self.activities.activity_lookup.get(activity_info.get('activity'), None)
            if activity == 1:
                general_fields, run_fields = self.activities.get_run_fields()
            elif activity == 2:
                general_fields, run_fields = self.activities.get_swim_fields()
            elif activity == 3:
                general_fields, run_fields = self.activities.get_bike_fields()
            elif activity == 4:
                general_fields, run_fields = self.activities.get_yoga_fields()
            else:
                message = 'No field options exist for {}'.format(activity_info.get('activity'))
                template = render_template('add_activity.html', error=[message], activity_list=activity_list)
                return make_response(template, 400, self.header)

            template = render_template('add_activity.html', activity_list=activity_list,
                                       activity=activity_info.get('activity'),
                                       general_fields=general_fields, activity_fields=run_fields)
            return make_response(template, 200, self.header)

        if not session.get('logged_in'):
            err_msgs = "HA! You aren't Erin! You can't add an activity for her."
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', error=[err_msgs], activity_list=activity_list)
            return make_response(template, 400, self.header)

        success = self.activities.add_activity(activity_info)

        if success:
            message = "Successfully added activity"
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', alert=message, activity_list=activity_list)
            return make_response(template, 400, self.header)

        else:
            err_msgs = "Failed to add activity"
            activity_list = [ACTIVITY_PLACEHOLDER] + self.activities.activity_list
            template = render_template('add_activity.html', error=[err_msgs], activity_list=activity_list)
            return make_response(template, 400, self.header)
