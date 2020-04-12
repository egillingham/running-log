import logging
import os
import json
from logstash_formatter import LogstashFormatterV1
from flask import Flask, url_for, render_template
from flask_restful import Api
# from flask_sitemap_domain import Sitemap
from werkzeug.middleware.proxy_fix import ProxyFix

# resources to load
from resources import adding, add_activity, homepage, user_login, about_me, feedback, activities, hearts_groups


APP = Flask(__name__)
# ext = Sitemap(app=APP, force_domain='eringillingham.com')


class RunningLogApi(Api):
    def handle_error(self, e):
        LOGGER.error('FATAL ERROR: {}'.format(e))
        LOGGER.exception(e)
        code = getattr(e, 'code', 500)
        # if code == 500:      # for HTTP 500 errors return my custom response
        #     error_msg = "Erin did something wrong. Please grab a pitchfork and run her out of town."
        #     return render_template('500.html', error=error_msg), 500
        if code == 404:
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
API.add_resource(hearts_groups.HeartsGroups, '/hearts/group/<string:group_name>')


@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + url_for('static', filename='images/{}'.format(name)) + '>'


APP.config['SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS'] = True


def create_logger():
    log = logging.getLogger('running-log')
    log.setLevel(logging.DEBUG)

    fmt = {'extra': {'type': 'running-log'}}
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(LogstashFormatterV1(fmt=json.dumps(fmt)))
    log.addHandler(ch)
    return log


if __name__ == '__main__':
    LOGGER = create_logger()
    LOGGER.info("In __main__, running host...")
    APP.secret_key = 'secret_test'
    APP.run(host='0.0.0.0', port=5005, debug=True)

elif __name__ == 'app':
    # when we run using gunicorn
    LOGGER = create_logger()
    LOGGER.info("WSGI setup...")
    flask_env = json.loads(os.environ.get("FLASK_SECRET", "{}"))
    APP.secret_key = flask_env.get("secret", "test")
    # might need this for https
    # https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/#deploying-proxy-setups
    APP.wsgi_app = ProxyFix(APP.wsgi_app, x_proto=1, x_host=1)
