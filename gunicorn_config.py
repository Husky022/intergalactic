command = '/home/intergalactic/project/django/env/bin/gunicorn'
pythonpath = '/home/intergalactic/project/django'
bind = '127.0.0.1:8001'
workers = 3
user = 'intergalactic'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=intergalactic.settings'
