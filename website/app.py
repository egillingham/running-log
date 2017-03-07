import os
from flask import Flask, url_for, render_template
from flask_restful import Api
from flask_sitemap_domain import Sitemap
from werkzeug.contrib.fixers import ProxyFix

# resources to load
from resources import adding, add_activity, homepage, user_login, about_me, feedback, activities


APP = Flask(__name__)
ext = Sitemap(app=APP, force_domain='eringillingham.com')


class RunningLogApi(Api):
    def handle_error(self, e):
        code = getattr(e, 'code', 500)
        if code == 500:      # for HTTP 500 errors return my custom response
            error_msg = "Erin did something wrong. Please grab a pitchfork and run her out of town."
            return render_template('500.html', error=error_msg), 500
        elif code == 404:
            error_msg = "This page doesn't exist yet silly. Send Erin a venmo if it's something you really want to see."
            return render_template('404.html', error=error_msg), 404
        return super(RunningLogApi, self).handle_error(e)


API = RunningLogApi(APP, catch_all_404s=True)


API.add_resource(homepage.Homepage, '/')
API.add_resource(adding.AddNumbers, '/add')
API.add_resource(add_activity.AddActivity, '/add-activity')
API.add_resource(activities.Activities, '/activities')
API.add_resource(user_login.Login, '/login')
API.add_resource(user_login.Logout, '/logout')
API.add_resource(about_me.Hello, '/hello')
API.add_resource(feedback.Feedback, '/feedback')


@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + url_for('static', filename='images/{}'.format(name)) + '>'


APP.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True


if __name__ == '__main__':
    print "In __main__, running host..."
    APP.secret_key = 'secret_test'
    APP.run(host='0.0.0.0', port=5005, debug=True)

elif __name__ == 'app':
    # when we run using gunicorn
    print "WSGI setup..."
    APP.secret_key = os.environ.get('FLASK_SECRET')
    APP.wsgi_app = ProxyFix(APP.wsgi_app)
