from flask import Flask, jsonify, url_for, request, session
from flask_restful import Api
from werkzeug.contrib.fixers import ProxyFix

from resources import adding, add_activity, homepage, user_login


APP = Flask(__name__)
API = Api(APP)


API.add_resource(homepage.Homepage, '/')
API.add_resource(adding.AddNumbers, '/add')
API.add_resource(add_activity.AddActivity, '/add-activity')
API.add_resource(user_login.Login, '/login')
API.add_resource(user_login.Logout, '/logout')


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


@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + url_for('static', filename='images/{}'.format(name)) + '>'


@APP.errorhandler(adding.InvalidNumber)
def handle_invalid_number(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    print "In __main__, running host..."
    APP.secret_key = 'secret_test'
    APP.run(host='0.0.0.0', port=5005, debug=True)

elif __name__ == 'app':
    # when we run using gunicorn
    print "WSGI setup..."
    APP.wsgi_app = ProxyFix(APP.wsgi_app)
