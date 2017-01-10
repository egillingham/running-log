from flask_restful import Resource, request
from flask import render_template, make_response


class AddNumbers(Resource):

    def __init__(self):
        self.header = {'Content-Type': 'text/html'}

    def post(self):
        try:
            sum = float(request.form['num1']) + float(request.form['num2'])
            result = "The sum of {} and {} is {}!".format(request.form['num1'], request.form['num2'], sum)
            template = render_template('adding.html', alert=result)
            return make_response(template, 200, self.header)
        except ValueError:
            template = render_template('adding.html', error="You did not enter a valid number idiot")
            return make_response(template, 400, self.header)

    def get(self):
        template = render_template('adding.html')
        return make_response(template, 200, self.header)
