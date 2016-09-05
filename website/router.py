from flask import Flask, request, jsonify, render_template, url_for, make_response

app = Flask(__name__)


@app.route('/')
def welcome():
    return '''
        <!doctype html>
        <h1>Hello<a href="{}">!</a></h1>
        '''.format(url_for('hello'))


@app.route('/hello')
def hello():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>It's <a href="{}">me</a></h1>
        '''.format(url_for('me'))


@app.route('/me')
def me():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>I'm in <a href="{}">California</a> dreaming</h1>
        '''.format(url_for('california'))


@app.route('/cali')
def california():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>About who we used to <a href="{}">be</a></h1>
        '''.format(url_for('otherside'))


@app.route('/otherside')
def otherside():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>Hello from the otherside</h1>
        '''


@app.route('/patches', methods=['GET', 'POST'])
def patches():
    if request.method == 'GET':
        return "PATCHES"


@app.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + url_for('static',filename=name) + '>'


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            sum = float(request.form['num1']) + float(request.form['num2'])
            return "The sum of {} and {} is <b>{}<b>!".format(request.form['num1'], request.form['num2'], sum)
        except ValueError:
            raise InvalidNumber("You did not enter a valid number idiot")
    else:
        return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>Add two numbers!</h1>
        <form action="" method=post enctype=application/x-www-form-urlencoded>
            <div><input type="text" name="num1"></div>
            <div><input type="text" name="num2"></div>
            <div><input type=submit value="Add!"></div>
        </form>
        '''


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


@app.errorhandler(InvalidNumber)
def handle_invalid_number(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')