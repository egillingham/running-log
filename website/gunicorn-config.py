import os

bind = "127.0.0.1:8000"
workers = 3
timeout = 1000

#user = 'erin'
#group = 'shared'
accesslog = os.path.join(os.path.dirname(__file__), '../logs/gunicorn_access.log')
errorlog = os.path.join(os.path.dirname(__file__), '../logs/gunicorn_error.log')