from flask import Flask, url_for
from flask_restful import Api
from werkzeug.contrib.fixers import ProxyFix

from resources import adding, add_activity, homepage, user_login, about_me


APP = Flask(__name__)
API = Api(APP)


API.add_resource(homepage.Homepage, '/')
API.add_resource(adding.AddNumbers, '/add')
API.add_resource(add_activity.AddActivity, '/add-activity')
API.add_resource(user_login.Login, '/login')
API.add_resource(user_login.Logout, '/logout')
API.add_resource(about_me.Hello, '/hello')


@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + url_for('static', filename='images/{}'.format(name)) + '>'


if __name__ == '__main__':
    print "In __main__, running host..."
    APP.secret_key = 'secret_test'
    APP.run(host='0.0.0.0', port=5005, debug=True)

elif __name__ == 'app':
    # when we run using gunicorn
    print "WSGI setup..."
    APP.wsgi_app = ProxyFix(APP.wsgi_app)
