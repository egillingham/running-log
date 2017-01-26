bind = "0.0.0.0:5050"
workers = 2
timeout = 300

accesslog = '/var/log/gunicorn/company_normalizer_gunicorn_access.log'
errorlog = '/var/log/gunicorn/company_normalizer_gunicorn_error.log'
