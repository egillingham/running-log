from flask_restful import Resource, request
from flask import Response


def output_html(data, code, headers=None):
    resp = Response(data, mimetype='text/html', headers=headers)
    resp.status_code = code
    return resp


class AddNumbers(Resource):

    def post(self):
        try:
            sum = float(request.form['num1']) + float(request.form['num2'])
            result = "The sum of {} and {} is <b>{}<b>!".format(request.form['num1'], request.form['num2'], sum)
            return output_html(result, 200)
        except ValueError:
            raise InvalidNumber("You did not enter a valid number idiot")

    def get(self):
        html = '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>Add two numbers!</h1>
        <form action="" method=post enctype=application/x-www-form-urlencoded>
            <div><input type="text" name="num1"></div>
            <div><input type="text" name="num2"></div>
            <div><input type=submit value="Add!"></div>
        </form>
        '''
        return output_html(html, 200)


class InvalidNumber(Exception):
    """
    Error handling for raw-data endpoint
    """
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = {'message': self.message}
        return rv
