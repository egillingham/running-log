from flask import Flask, request, jsonify, render_template, url_for, make_response
from flask_restful import Api
from werkzeug.contrib.fixers import ProxyFix

from resources import adding


APP = Flask(__name__)
API = Api(APP)


API.add_resource(adding.AddNumbers, '/add')


@APP.route('/')
def welcome():
    return render_template('homepage.html')


@APP.route('/hello')
def hello():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>It's <a href="{}">me</a></h1>
        '''.format(url_for('me'))


@APP.route('/me')
def me():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>I'm in <a href="{}">California</a> dreaming</h1>
        '''.format(url_for('california'))


@APP.route('/cali')
def california():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>About who we used to <a href="{}">be</a></h1>
        '''.format(url_for('otherside'))


@APP.route('/otherside')
def otherside():
    return '''
        <!doctype html>
        <title>Add two numbers!</title>
        <h1>Hello from the otherside</h1>
        '''


@APP.route('/patches', methods=['GET', 'POST'])
def patches():
    if request.method == 'GET':
        return "PATCHES"


@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + url_for('static', filename=name) + '>'


@APP.errorhandler(adding.InvalidNumber)
def handle_invalid_number(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    print "In __main__, running host..."
    APP.run(host='0.0.0.0', debug=True)

elif __name__ == 'app':
    # when we run using gunicorn
    print "WSGI setup..."
    APP.wsgi_app = ProxyFix(APP.wsgi_app)
